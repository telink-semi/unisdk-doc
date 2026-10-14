---
title: Audio Sample
status: DRAFT
---

# Audio Sample

## Overview

The `audio_demo` sample demonstrates the Audio driver's record-and-playback pipeline: it records audio from a digital microphone (DMIC) into flash-backed storage using DMA linked-list buffers, then plays the recorded audio back out through the audio output path.

## Features Demonstrated

- Audio input (recording) configuration via `tlk_audio_input_configure` / `tlk_audio_input_enable` / `tlk_audio_input_disable`
- Audio output (playback) configuration via `tlk_audio_output_configure` / `tlk_audio_output_enable` / `tlk_audio_output_disable`
- Double-buffered DMA linked-list transfers (`struct tlk_dma_ll_node`) for both RX and TX
- DMA interrupt callbacks (`tlk_dma_chn_add_callback`) that feed/drain the buffers to/from storage on every DMA transfer-complete interrupt
- Chip-specific audio pinmux configuration for AMIC bias, DMIC data/clock, and SDM (sigma-delta modulator) pins, selected per SoC (`CONFIG_TLK_CORE_TL321X`, `CONFIG_TLK_CORE_TL721X`, `CONFIG_TLK_CORE_B92`)
- Non-volatile storage read/write/erase (`tlk_storage_write`, `tlk_storage_read`, `tlk_storage_erase`) used as the recording buffer
- Benchmarking of erase/record/playback timing via `tlk_benchmark_begin` / `tlk_benchmark_end` / `tlk_benchmark_elapsed`

## How It Works

### Initialization

1. **Storage Setup** — A storage region is reserved at the top of ROM (`storage_addr`, sized `BUFFER_COUNT * BUFFER_SIZE` = 256 KiB) and located with `tlk_storage_find_device`.
2. **Pinmux Configuration** — Depending on the target core, AMIC bias, DMIC data/clock pins, and SDM P/N pins are set up (e.g. for `CONFIG_TLK_CORE_B92`, only DMIC pins are configured; the AMIC/SDM structs are left empty).
3. **DMA Linked Lists** — Two double-buffered linked lists are built: `tx_buffer0`/`tx_buffer1` for playback and `rx_buffer0`/`rx_buffer1` for recording, each node covering one 1024-byte `audio_buffer` slot.
4. **Audio Input/Output Configuration** — `tlk_audio_input_configure` and `tlk_audio_output_configure` are called with `TLK_AUDIO_48K` sample rate, 16-bit data width, and the left I2S channel, wired to DMA channels obtained from `tlk_dma_chn_request()`.
5. **DMA Callbacks** — `on_rx_buffer_fill` and `on_tx_buffer_sent` are registered as DMA transfer-complete callbacks; they call `save_buffer()` / `fill_buffer()` to move data between the DMA buffer and flash storage on each completed block.

### Main Loop

```c
while (1)
{
    audio_tx_buffer_index = 0;
    audio_rx_buffer_index = 0;

    is_rx_done = 0;
    is_tx_done = 0;

    tlk_benchmark_begin(&span);
    tlk_storage_erase(storage_addr, STORAGE_SIZE);
    tlk_benchmark_end(&span);

    tlk_gpio_pin_toggle(PINMUX_LED_1_PORT, PINMUX_LED_1_PIN);
    tlk_benchmark_begin(&span);

    tlk_audio_input_enable();
    while (!is_rx_done) { }
    tlk_benchmark_end(&span);

    tlk_gpio_pin_toggle(PINMUX_LED_1_PORT, PINMUX_LED_1_PIN);
    tlk_benchmark_begin(&span);

    fill_buffer();
    tlk_audio_output_enable();
    while (!is_tx_done) { }
    tlk_benchmark_end(&span);
}
```

Each cycle: erase the storage region, record `BUFFER_COUNT` (256) blocks of `BUFFER_SIZE` (1024) bytes from the DMIC into storage (recording stops automatically once `audio_rx_buffer_index == BUFFER_COUNT`, disabling audio input), then play the recorded blocks back out (stopping once `audio_tx_buffer_index == BUFFER_COUNT`, disabling audio output). LED1 is toggled between the record and playback phases as a visual marker, and elapsed erase/record/playback time is logged via the benchmark span.

:::{note} Per-Core Pinmux
The sample selects its AMIC/DMIC/SDM pin assignments at compile time based on which core config (`CONFIG_TLK_CORE_TL321X`, `CONFIG_TLK_CORE_TL721X`, or `CONFIG_TLK_CORE_B92`) is active, since the audio pin layout differs between chips.
:::

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_AUDIO_DEMO` | Enables the sample; selects `TLK_AUDIO`, `TLK_NV_STORAGE`, and `TLK_DMA_IRQ_HANDLER` (default `y`, not user-facing) |

:::{note}
This sample has no user-selectable Kconfig choices beyond the auto-selected dependencies above — behavior is fixed at record-then-playback, with pin assignments chosen automatically based on the target core.
:::

## Build & Run

```bash
west tl-build samples/audio_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/audio_demo.bin
```

Source code: `samples/audio_demo/main.c`
