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

### RX Timeout Multiplier

`enum tlk_uart_rx_timeout_mul`

Multiplier for RX timeout duration. The total RX timeout = (one UART frame duration) × multiplier.

| Value | Description |
|---|------|
| `TLK_UART_RX_TIMEOUT_MUL_1` | 1× frame duration |
| `TLK_UART_RX_TIMEOUT_MUL_2` | 2× frame duration |
| `TLK_UART_RX_TIMEOUT_MUL_3` | 3× frame duration |
| `TLK_UART_RX_TIMEOUT_MUL_4` | 4× frame duration |

### UART Configuration Structure

`struct tlk_uart_config`

A structure containing all configuration parameters for initializing a UART module. Used with `tlk_uart_configure` and `tlk_uart_configure_pinmux`.

| Field | Type | Description |
|---|------|------|
| `baudrate` | `uint32_t` | Communication speed in baud |
| `parity` | `enum tlk_uart_parity` | Parity check mode |
| `stop_bit` | `enum tlk_uart_stop_bit` | Number of stop bits |
| `rx_timeout_mul` | `enum tlk_uart_rx_timeout_mul` | RX timeout multiplier |
| `tx_port_pin` | `struct tlk_gpio_port_pin` | TX port and pin |
| `rx_port_pin` | `struct tlk_gpio_port_pin` | RX port and pin |

### Operation Status

`enum tlk_uart_status`

Return codes used by driver functions to indicate the result of an operation.

| Value | Description |
|---|------|
| `TLK_UART_OK` | Operation completed successfully. |
| `TLK_UART_TIMEOUT` | Operation timed out. |
| `TLK_UART_ERROR` | General execution error. |

### Flow Control Modes

:::{info} Requires `CONFIG_TLK_UART_USED_FLOW_CONTROL`
:::

`enum tlk_uart_flow_control`

| Value | Description |
|---|------|
| `TLK_UART_FLOW_NONE` | Flow control disabled. |
| `TLK_UART_FLOW_RTS` | RTS signal only. |
| `TLK_UART_FLOW_CTS` | CTS signal only. |
| `TLK_UART_FLOW_RTS_CTS` | Full RTS/CTS flow control. |

### Flow Control Polarity

:::{info} Requires `CONFIG_TLK_UART_USED_FLOW_CONTROL`
:::

`enum tlk_uart_flow_polarity`

Defines the active level logic for RTS and CTS signals.

| Value | Description |
|---|------|
| `TLK_UART_ACTIVE_LOW` | **Active Low.** UART stops sending when CTS is low, and sets RTS low to stop receiving. |
| `TLK_UART_ACTIVE_HIGH` | **Active High.** UART stops sending when CTS is high, and sets RTS high to stop receiving. |

### Flow Control Configuration Structure

:::{info} Requires `CONFIG_TLK_UART_USED_FLOW_CONTROL`
:::

`struct tlk_uart_flow_control_config`

A structure containing all configuration parameters for UART hardware flow control. Used with `tlk_uart_configure_flow_control` and `tlk_uart_configure_flow_control_pinmux`.

| Field | Type | Description |
|---|------|------|
| `flow_control` | `enum tlk_uart_flow_control` | Flow control mode (RTS/CTS) |
| `flow_polarity` | `enum tlk_uart_flow_polarity` | Active level for RTS/CTS signals |
| `rts_port_pin` | `struct tlk_gpio_port_pin` | RTS port and pin |
| `cts_port_pin` | `struct tlk_gpio_port_pin` | CTS port and pin |

### Transmit Handler Type

`tlk_uart_tx_handler_t`

A function pointer type for the callback invoked when data transmission is complete in interrupt and DMA modes.

```c
typedef void (*tlk_uart_tx_handler_t)(void);
```

### Receive Handler Type

`tlk_uart_rx_handler_t`

A function pointer type for the callback invoked when data reception is complete in interrupt and DMA modes.

```c
typedef void (*tlk_uart_rx_handler_t)(uint32_t rx_count);
```

## Driver API

### `tlk_uart_configure`

Initializes the UART module with the provided configuration.

```c
void tlk_uart_configure(enum tlk_uart_module uart_num,
                        struct tlk_uart_config *config);
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `uart_num` | `enum tlk_uart_module` | UART module index. |
| `config` | `struct tlk_uart_config *` | Pointer to the configuration structure containing baudrate, parity, stop bits, and pin assignments. |

**Return value:** None

### `tlk_uart_configure_pinmux`

Configures UART TX/RX pin multiplexing.

```c
void tlk_uart_configure_pinmux(enum tlk_uart_module uart_num,
                               struct tlk_uart_config *config);
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `uart_num` | `enum tlk_uart_module` | UART module index. |
| `config` | `struct tlk_uart_config *` | Pointer to the configuration structure containing TX and RX pin assignments. |

**Return value:** None

### `tlk_uart_send_bytes`

Sends a data buffer.

```c
enum tlk_uart_status tlk_uart_send_bytes(enum tlk_uart_module uart_num,
    const uint8_t *buff, uint32_t buff_size,
    tlk_uart_tx_handler_t tx_handler, uint32_t timeout_us);
```

### `tlk_uart_receive_bytes`

Receives a data buffer. The provided handler is called when reception is complete.

```c
enum tlk_uart_status tlk_uart_receive_bytes(enum tlk_uart_module uart_num,
    uint8_t *buff, uint32_t buff_size,
    tlk_uart_rx_handler_t rx_handler);
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `uart_num` | `enum tlk_uart_module` | UART module index. |
| `buff` | `uint8_t *` | Pointer to the receive buffer. |
| `buff_size` | `uint32_t` | Number of bytes to receive. |
| `rx_handler` | `tlk_uart_rx_handler_t` | Callback function invoked after reception completes. |

**Return value:** `enum tlk_uart_status` — Returns `TLK_UART_OK`.

### `tlk_uart_configure_flow_control`

:::{info} Requires `CONFIG_TLK_UART_USED_FLOW_CONTROL`
:::

Configure the flow control for the specified UART module. Disabled by default. Should be called after `tlk_uart_configure`.

```c
void tlk_uart_configure_flow_control(enum tlk_uart_module uart_num,
                         struct tlk_uart_flow_control_config *config);
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `uart_num` | `enum tlk_uart_module` | UART module index. |
| `config` | `struct tlk_uart_flow_control_config *` | Pointer to the flow control configuration structure. |

**Return value:** None

### `tlk_uart_configure_flow_control_pinmux`

:::{info} Requires `CONFIG_TLK_UART_USED_FLOW_CONTROL`
:::

Configure UART RTS and CTS pin multiplexing.

```c
void tlk_uart_configure_flow_control_pinmux(enum tlk_uart_module uart_num,
                                struct tlk_uart_flow_control_config *config);
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `uart_num` | `enum tlk_uart_module` | UART module index. |
| `config` | `struct tlk_uart_flow_control_config *` | Pointer to the flow control configuration structure containing RTS and CTS pin assignments. |

**Return value:** None

## Transfer Modes

Each UART instance can independently configure its transfer mode:

| Mode | Kconfig Value | Description |
|------|-----------|------|
| Blocking | `TLK_UART_XFER_BLOCKING` | Synchronous wait, with timeout |
| Interrupt | `TLK_UART_XFER_PLIC` | Interrupt-driven, auto-fill FIFO |
| DMA | `TLK_UART_XFER_DMA` | DMA driven, zero CPU load |

## Kconfig Configuration

### Global options

**`TLK_UART_SELECTED**  
Indicates that at least one UART instance is enabled in the system. This option is automatically selected when any `UART{i}_ENABLED` option is enabled.

**`TLK_UART_USED_AUTO_CONFIG`**  
Indicates that automatic UART configuration is enabled in the system. This option is automatically selected when `UART{i}_AUTO_CONFIG` is enabled for any UART instance.

**`TLK_UART_USED_IRQ`**  
Indicates that at least one UART instance needs a PLIC functionality. This option is automatically selected when `UART{i}_USED_IRQ` or `UART{i}_USED_DMA` are enabled for any UART instance.

**`TLK_UART_USED_DMA`**  
Indicates that at least one UART instance needs a DMA functionality. This option is automatically selected when `UART{i}_USED_DMA` is enabled for any UART instance.

**`TLK_UART_USED_PM_DEVICE`**  
Indicates that UART power management support is enabled in the system. This option is automatically selected when `UART{i}_PM_DEVICE` is enabled for any UART instance.

**`TLK_UART_USED_FLOW_CONTROL`**  
Indicates that hardware flow control (RTS/CTS) is enabled in the system. This option is automatically selected when `UART{i}_FLOW_CONTROL` is enabled for any UART instance.

### Per-instance Configuration

Each UART instance (i = 0, 1, 2...) supports the following hierarchical configuration:

```{mermaid}
graph TD
    UART["UART{i}_ENABLED<br/>Enables UART module"] --> AUTO["UART{i}_AUTO_CONFIG<br/>Auto configuration"]
    UART --> TX["UART{i}_TX_MODE<br/>Transmission mode"]
    UART --> RX["UART{i}_RX_MODE<br/>Reception mode"]
    UART --> PM["UART{i}_PM_DEVICE<br/>Power management support"]
    UART --> SLEEP["UART{i}_PREVENT_SLEEP<br/>Prevent sleep during RX"]
    UART --> DEBUG["TLK_DEBUG_PRINT<br/>Debug output"]

    AUTO --> BAUD["UART{i}_BAUDRATE<br/>Default: 115200"]
    AUTO --> PARITY["UART{i}_PARITY<br/>Parity mode"]
    AUTO --> STOP["UART{i}_STOP_BIT<br/>Stop bits"]
    AUTO --> FLOW["UART{i}_FLOW_CONTROL_TYPE<br/>Flow control"]
    AUTO --> FPOL["UART{i}_FLOW_POLARITY<br/>Flow polarity"]

    PARITY --> NONE["TLK_UART_PARITY_NONE"]
    PARITY --> EVEN["TLK_UART_PARITY_EVEN"]
    PARITY --> ODD["TLK_UART_PARITY_ODD"]

    STOP --> SB1["TLK_UART_STOP_BIT_ONE"]
    STOP --> SB15["TLK_UART_STOP_BIT_ONE_DOT_FIVE"]
    STOP --> SB2["TLK_UART_STOP_BIT_TWO"]

    FLOW --> FNONE["TLK_UART_FLOW_NONE"]
    FLOW --> FRTS["TLK_UART_FLOW_RTS"]
    FLOW --> FCTS["TLK_UART_FLOW_CTS"]
    FLOW --> FRTSCTS["TLK_UART_FLOW_RTS_CTS"]

    FPOL --> ALOW["TLK_UART_ACTIVE_LOW (Default)"]
    FPOL --> AHIGH["TLK_UART_ACTIVE_HIGH"]

    TX --> TXB["TLK_UART_XFER_BLOCKING"]
    TX --> TXI["TLK_UART_XFER_IRQ"]
    TX --> TXD["TLK_UART_XFER_DMA"]

    RX --> RXB["TLK_UART_XFER_BLOCKING"]
    RX --> RXI["TLK_UART_XFER_IRQ"]
    RX --> RXD["TLK_UART_XFER_DMA"]

    DEBUG --> DBG_UART["TLK_DEBUG_PRINT_UART<br/>Which UART instances"]
    DEBUG --> DBG_BUF["TLK_DEBUG_PRINT_BUFFER_SIZE<br/>Default: 256 bytes"]
```

### View in the menuconfig

![alt text](pics/uart_1.png)
*Figure 1. UART driver configurations*

![alt text](pics/uart_2.png)
*Figure 2. UART instance configurations*

![alt text](pics/uart_3.png)
*Figure 3. UART instance auto-config options*

![alt text](pics/uart_4.png)
*Figure 4. UART debug configurations*

## Related Resources

- [UART Samples](../samples/uart.md)
