---
title: DMA Sample
status: DRAFT
---

# DMA Sample

:::{note} Document Status: DRAFT — Content is being finalized
:::

## Overview

The `dma_demo` sample demonstrates memory-to-memory transfers using the DMA driver: requesting and configuring a DMA channel, starting a transfer, aborting a transfer mid-flight, and completing a transfer — optionally driven by interrupt callbacks and/or combined with sleep/PM-prevent logic.

## Features Demonstrated

- DMA channel request and configuration (`tlk_dma_chn_request`, `tlk_dma_chn_configure`)
- Memory-to-memory transfer setup, start, and abort (`tlk_dma_chn_transfer_configure`, `tlk_dma_chn_transfer_start`, `tlk_dma_chn_transfer_abort`)
- Optional DMA interrupt callback registration (`tlk_dma_chn_add_callback`, requires `CONFIG_TLK_DMA_DEMO_INTERRUPT`)
- Optional sleep between transfer cycles (requires `CONFIG_TLK_DMA_DEMO_SLEEP`)
- Optional PM-suspend-with-prevent-sleep pattern around an active transfer (requires `CONFIG_TLK_DMA_DEMO_PREVENT`)

## How It Works

### Initialization

```c
demo_chn = tlk_dma_chn_request();
tlk_dma_chn_configure(demo_chn, &chn_config);

#if TLK_IS_ENABLED(CONFIG_TLK_DMA_DEMO_INTERRUPT)
tlk_dma_chn_add_callback(demo_chn, chn_handler);
#endif
```

`chn_config` is a `struct tlk_dma_config` configured for a normal-mode, byte-width, incrementing-address transfer on both source and destination, with a single-transfer burst size:

```c
struct tlk_dma_config chn_config = {
    .dst_req_sel    = 0,
    .src_req_sel    = 0,
    .dst_addr_ctrl  = TLK_DMA_ADDR_INCREMENT,
    .src_addr_ctrl  = TLK_DMA_ADDR_INCREMENT,
    .dstmode        = TLK_DMA_NORMAL_MODE,
    .srcmode        = TLK_DMA_NORMAL_MODE,
    .dstwidth       = TLK_DMA_BYTE_WIDTH,
    .srcwidth       = TLK_DMA_BYTE_WIDTH,
    .src_burst_size = TLK_DMA_BURST_1_TRANSFER,
    .read_num_en    = 0,
    .priority       = 0,
    .write_num_en   = 0,
    .auto_en        = 0,
};
```

When `CONFIG_TLK_DMA_DEMO_INTERRUPT` is enabled, `chn_handler` sets a `dma_complete` or `dma_abort` flag depending on the IRQ type (`TLK_DMA_IRQ_TC` / `TLK_DMA_IRQ_ABT`), which the main loop then polls.

:::{note} Minimum Stack Size
The sample enforces a minimum 2KB stack at compile time via `#if CONFIG_TLK_MEMORY_STACK_SIZE < 2` / `#error`.
:::

### Main Loop

Each iteration of the loop:

1. (Optional, `CONFIG_TLK_DMA_DEMO_PREVENT`) Starts a transfer of the full `src`/`dst` arrays (`ARRAY_LEN` = 300 bytes), then calls `TLK_PM_SLEEP_MS(TLK_PM_SLEEP_MODE_SUSPEND, 10)` — if the DMA transfer is still active, sleep entry is denied and the demo logs `"The sleep was prevented due to active receiving"`.
2. Fills `src` with incrementing values and clears `dst` for `TRANSFER_SIZE` (32) bytes, then logs both buffers.
3. Starts a `TRANSFER_SIZE`-byte transfer and immediately calls `tlk_dma_chn_transfer_abort`, demonstrating mid-transfer abort. With `CONFIG_TLK_DMA_DEMO_INTERRUPT` enabled, the loop spins on `dma_abort` before logging `"DMA IRQ: abort"`. Buffers are logged again afterward.
4. Clears `dst`, starts a fresh `TRANSFER_SIZE`-byte transfer and lets it run to completion. With interrupts enabled, the loop spins on `dma_complete` before logging `"DMA IRQ: complete"`. Buffers are logged again to show the completed copy.
5. Delays 5 seconds — via `tlk_api_sleep` (if `CONFIG_TLK_DMA_DEMO_SLEEP`) or `tlk_api_time_delay` otherwise — before repeating.

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_DMA_DEMO_INTERRUPT` | Use DMA interrupts (`TLK_PLIC`, `TLK_DMA_IRQ_HANDLER`) to detect transfer completion/abort instead of polling registers directly |
| `CONFIG_TLK_DMA_DEMO_SLEEP` | Use `tlk_api_sleep` for the end-of-loop delay; selects `TLK_API_SLEEP` and implies `TLK_DMA_PM_DEVICE` |
| `CONFIG_TLK_DMA_DEMO_PREVENT` | Demonstrate PM sleep prevention while a DMA transfer is active; selects `TLK_PM`, `TLK_PM_SUSPEND`, and `TLK_DMA_PREVENT_SLEEP` |

The sample's base `TLK_DMA_DEMO` config selects `TLK_DMA`, `TLK_API_PRINT`, and `TLK_API_TIME` unconditionally.

## Build & Run

```bash
west tl-build samples/dma_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/Telink.bin
```

Source code: `samples/dma_demo/main.c`
