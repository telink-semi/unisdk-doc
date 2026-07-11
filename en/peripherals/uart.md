---
title: UART Driver
status: STABLE
---

# UART Driver

## Overview

The UART driver provides an interface for configuring and using asynchronous serial ports. It supports communication parameter configuration (baud rate, parity, stop bits), pin multiplexing (Pinmux), data transmission (blocking mode), and data reception (blocking and non-blocking interrupt modes). It also supports hardware flow control (RTS/CTS).

**Key Features:**

- UART parameter configuration (baud rate, parity, stop bits)
- TX/RX and RTS/CTS pin multiplexing
- Data transmission (Blocking / PLIC / DMA modes)
- Data reception (Blocking / PLIC / DMA modes + callback)
- Hardware flow control (RTS/CTS)

## Data Types and Enums

### UART Module Identifiers

`enum tlk_uart_module` — Automatically generated based on `UNISDK_UART_COUNT` and enabled instances. Values include `UART0`, `UART1`, etc.

### Parity

`enum tlk_uart_parity`

| Value | Description |
|---|------|
| `TLK_UART_PARITY_NONE` | No parity |
| `TLK_UART_PARITY_EVEN` | Even parity |
| `TLK_UART_PARITY_ODD` | Odd parity |

### Stop Bits

`enum tlk_uart_stop_bit`

| Value | Description |
|---|------|
| `TLK_UART_STOP_BIT_ONE` | 1 stop bit |
| `TLK_UART_STOP_BIT_ONE_DOT_FIVE` | 1.5 stop bits |
| `TLK_UART_STOP_BIT_TWO` | 2 stop bits |

## Driver API

### `tlk_uart_configure`

Initializes the UART module.

```c
void tlk_uart_configure(enum tlk_uart_module uart_num, uint32_t baudrate,
                        enum tlk_uart_parity parity, enum tlk_uart_stop_bit stop_bit);
```

### `tlk_uart_configure_pinmux`

Configures UART TX/RX pin multiplexing.

```c
void tlk_uart_configure_pinmux(enum tlk_uart_module uart_num,
                               struct tlk_gpio_port_pin tx_port_pin,
                               struct tlk_gpio_port_pin rx_port_pin);
```

### `tlk_uart_send_bytes`

Sends a data buffer.

```c
enum tlk_uart_status tlk_uart_send_bytes(enum tlk_uart_module uart_num,
    const uint8_t *buff, uint32_t buff_size,
    tlk_uart_tx_handler_t tx_handler, uint32_t timeout_us);
```

### `tlk_uart_receive_bytes`

Receives a data buffer.

```c
enum tlk_uart_status tlk_uart_receive_bytes(enum tlk_uart_module uart_num,
    uint8_t *buff, uint32_t buff_size,
    tlk_uart_rx_handler_t rx_handler, uint32_t timeout_us);
```

### `tlk_uart_flow_configure`

!!! info "Requires `CONFIG_TLK_UART_FLOW_CONTROL`"

Configures hardware flow control.

```c
void tlk_uart_flow_configure(enum tlk_uart_module uart_num,
    enum tlk_uart_flow_control flow_control, enum tlk_uart_flow_polarity flow_polarity);
```

## Transfer Modes

Each UART instance can independently configure its transfer mode:

| Mode | Kconfig Value | Description |
|------|-----------|------|
| Blocking | `TLK_UART_XFER_BLOCKING` | Synchronous wait, with timeout |
| Interrupt | `TLK_UART_XFER_PLIC` | Interrupt-driven, auto-fill FIFO |
| DMA | `TLK_UART_XFER_DMA` | DMA driven, zero CPU load |

## Kconfig Configuration

Each UART instance (i = 0, 1, 2...) supports the following configuration:

```kconfig
CONFIG_UART{i}_ENABLED              # Enable UART instance
CONFIG_UART{i}_AUTO_CONFIG          # Auto configuration
CONFIG_UART{i}_BAUDRATE             # Baud rate (default 115200)
CONFIG_UART{i}_TX_MODE              # TX mode
CONFIG_UART{i}_RX_MODE              # RX mode
CONFIG_UART{i}_FLOW_CONTROL_TYPE    # Flow control type
```

## Related Resources

- [UART Samples](../samples/uart.md)
