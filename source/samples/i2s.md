---
title: I2S Sample
status: DRAFT
---

# I2S Sample

## Overview

The `i2s_demo` sample demonstrates the I2S driver by continuously transmitting a fixed test pattern out over I2S while simultaneously receiving on the same bus, and using an LED to indicate whether the transmitted and received data match.

## Features Demonstrated

- I2S pinmux configuration (`tlk_i2s_pinmux_configure`) for BCLK, ADC (RX) LR clock/data, and DAC (TX) LR clock/data pins
- I2S device configuration (`tlk_i2s_configure`) with 16-bit data width and I2S mode
- Master/Slave role selection (`CONFIG_TLK_I2S_DEMO_ROLE_MASTER` / `CONFIG_TLK_I2S_DEMO_ROLE_SLAVE`)
- Simultaneous DMA-driven output and input paths (`tlk_i2s_configure_output`, `tlk_i2s_input_configure`) using circular DMA linked-list nodes (`struct tlk_dma_ll_node`, self-referencing `next` for continuous looping)
- Starting the I2S device with `tlk_i2s_start`

## How It Works

### Initialization

1. **Pinmux** — BCLK, ADC LR clock/data, and DAC LR clock/data pins are assigned (`struct tlk_i2s_pinmux`).
2. **Role Selection** — At compile time, if `CONFIG_TLK_I2S_DEMO_ROLE_MASTER` is enabled, the device is configured as `TLK_I2S_MASTER` with an explicit sample-rate divider (`{8, 625, 0, 64, 64}`); if `CONFIG_TLK_I2S_DEMO_ROLE_SLAVE` is enabled, it is configured as `TLK_I2S_SLAVE` (sample rate is driven externally).
3. **Circular DMA Buffers** — `rx_buff0` and `tx_buff0` are each set up as a single-node circular linked list (`next` points back to itself), so RX and TX run continuously without needing new nodes queued.
4. **I2S Configuration** — `tlk_i2s_configure`, `tlk_i2s_pinmux_configure`, `tlk_i2s_configure_output`, and `tlk_i2s_input_configure` are called on the `tlk_i2s0` device, wiring DMA channels from `tlk_dma_chn_request()` to FIFO0 on the left I2S channel for both TX and RX.
5. **Start** — `tlk_i2s_start(dev)` begins continuous transmit/receive.

### Main Loop

```c
while (1)
{
    // Mark the successful transmission with the enabled LED
    // I2S has a known issue that the rx buffer has 3 dummy elements at the beginning
    tlk_gpio_pin_write(PINMUX_LED_0_PORT, PINMUX_LED_0_PIN, tx_buffer[0] == rx_buffer[3]);
}
```

The loop continuously compares `tx_buffer[0]` (the first transmitted sample) against `rx_buffer[3]` (offset by 3 to account for a known driver quirk where the RX buffer starts with 3 dummy elements) and drives the board LED accordingly — the LED lights up once transmitted data is correctly looped back into the receive buffer.

:::{note} Loopback Wiring
This sample transmits and receives at the same time on the same I2S device. To see the LED light up, the DAC output pins must be physically wired to the ADC input pins on the board (or an external I2S codec must loop the signal back).
:::

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_I2S_DEMO` | Enables the sample; selects `TLK_I2S` and `TLK_I2S0` (default `y`, not user-facing) |
| `CONFIG_TLK_I2S_DEMO_ROLE_MASTER` | Configure the I2S device as bus master, driving BCLK/LRCLK with an explicit sample-rate divider |
| `CONFIG_TLK_I2S_DEMO_ROLE_SLAVE` | Configure the I2S device as bus slave, following an externally supplied clock |

## Build & Run

```bash
west tl-build samples/i2s_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/i2s_demo.bin
```

Source code: `samples/i2s_demo/main.c`
