---
title: UART Sample
status: STABLE
---

# UART Sample

## Overview

The `uart_demo` sample demonstrates the UART driver's echo functionality: receiving data and sending it back as-is.

## Features Demonstrated

- Manual UART configuration using `tlk_uart_configure` (when `CONFIG_TLK_UART_DEMO_AUTO_CONFIG` is disabled) — TX/RX pins are supplied directly in the `struct tlk_uart_config` passed to `tlk_uart_configure`
  - Manual UART flow control configuration using `tlk_uart_flow_control_configure` if `CONFIG_TLK_UART0_FLOW_CONTROL` is enabled
- Callback-based data reception (`tlk_uart_receive_bytes`)
- Data transmission (`tlk_uart_send_bytes`)
- Power management and sleep prevention (optional)

## How It Works

### Initialization

1. **Interrupt Enable** — Call `tlk_core_interrupt_enable()` to enable asynchronous callbacks
2. **Manual Configuration** — If `CONFIG_TLK_UART_DEMO_AUTO_CONFIG` is disabled, manually configure the selected UART (`CONFIG_TLK_UART_DEMO_UART`) using `tlk_uart_configure`, with TX on port C pin 4 and RX on port C pin 5. If `CONFIG_TLK_UART0_FLOW_CONTROL` is enabled, also configure flow control using `tlk_uart_flow_control_configure` (RTS on port C pin 6, CTS on port C pin 7)

### Main Loop (Echo Flow)

1. **Power Management Test** — If `CONFIG_TLK_UART_DEMO_SLEEP` is enabled, first print "Before sleep", sleep for 2 seconds, then print "After sleep" upon wake-up
2. Call `tlk_uart_receive_bytes` to listen for data, using the `rx_handler` callback
3. Wait for `rx_handler` to set the `rx_count` variable to the number of bytes received
4. Send the received data back to the serial port (`tlk_uart_send_bytes`)
5. Reset `rx_count` and repeat

### Sleep Prevention Test

When `CONFIG_TLK_UART_DEMO_PREVENT` is enabled, the sample attempts to sleep for 10 ms during reception (`TLK_PM_SLEEP_MS(TLK_PM_SLEEP_MODE_SUSPEND, 10)`) to verify that `tlk_pm_sleep` returns `TLK_PM_SLEEP_DENIED`.

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_UART_DEMO_UART{i}` | Selects which UART instance (`UART0`, `UART1`, ...) the sample uses |
| `CONFIG_TLK_UART_DEMO_BUFFER_SIZE` | Size of the receive buffer (default 15) |
| `CONFIG_TLK_UART_DEMO_SLEEP` | Test whether UART works correctly after wake-up |
| `CONFIG_TLK_UART_DEMO_PREVENT` | Test whether sleep is correctly prevented during reception |

:::{note} Auto-Configuration
`CONFIG_TLK_UART_DEMO_AUTO_CONFIG` is not a user-selectable option in this sample's Kconfig — it is automatically set based on whether the selected UART's own `TLK_UART{i}_AUTO_CONFIG` option is enabled.
:::

## Build & Run

```bash
west tl-build samples/uart_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/Telink.bin
```
