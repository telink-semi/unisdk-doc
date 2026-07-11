---
title: UART Sample
status: STABLE
---

# UART Sample

## Overview

The `uart_demo` sample demonstrates the UART driver's echo functionality: receiving data and sending it back as-is.

## Features Demonstrated

- Manual UART configuration (when `CONFIG_TLK_UART_AUTO_CONFIG` is disabled)
- Callback-based data reception (`tlk_uart_receive_bytes`)
- Data transmission (`tlk_uart_send_bytes`)
- Power management and sleep prevention (optional)

## How It Works

### Initialization

1. **Manual Configuration** — If automatic configuration is not enabled, manually set UART1 parameters
2. **Power Management Test** — If `CONFIG_TLK_UART_DEMO_SLEEP` is enabled, first print "Before sleep", sleep for 2 seconds, then print "After sleep" upon wake-up
3. **Interrupt Enable** — Call `tlk_core_interrupt_enable()` to enable asynchronous callbacks

### Main Loop (Echo Flow)

1. Call `tlk_uart_receive_bytes` to listen for data
2. Wait for the `rx_handler` callback to set the `rx_done` flag
3. Send received data back to the serial port (`tlk_uart_send_bytes`)
4. Reset the flag and repeat

### Sleep Prevention Test

When `CONFIG_TLK_UART_DEMO_PREVENT` is enabled, the sample attempts to sleep during reception to verify that `tlk_pm_sleep` returns `TLK_PM_SLEEP_DENIED`.

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_UART_DEMO_SLEEP` | Test whether UART works correctly after wake-up |
| `CONFIG_TLK_UART_DEMO_PREVENT` | Test whether sleep is correctly prevented during reception |

## Build & Run

```bash
west tl-build samples/uart_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/uart_demo.bin
```
