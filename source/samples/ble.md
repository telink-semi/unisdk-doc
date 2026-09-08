---
title: BLE Sample
status: DRAFT
---

# BLE Sample

:::{note} Document Status: DRAFT — Content is being finalized
:::

## Overview

This page covers two low-level BLE radio/controller samples:

- **`samples/adv_demo`** — a minimal example that drives the RF driver directly to transmit raw
  BLE advertising packets, without using the BLE Controller stack.
- **`samples/ble_controller_demo`** — a full BLE Controller demo that exposes the standard HCI
  interface over a UART transport, for use with an external Host.

For the newer SAL-based BLE Host stack sample, see the [BLE Host Sample](ble_host.md).

## Features Demonstrated

### adv_demo

- Direct `tlk_rf_*` API usage to configure the radio for BLE (`tlk_rf_configure`)
- Manual construction of a raw BLE advertising PDU (flags, complete local name, appearance)
- Packet transmission via `tlk_rf_tx_prepare_packet` / `tlk_rf_start_stx`
- GPIO toggling to visually indicate each transmitted packet

### ble_controller_demo

- BLE Controller stack initialization (`tlk_ble_controller_initial`)
- Standard HCI transport carried over UART1 (`tlk_uart_send_bytes` / `tlk_uart_receive_bytes`)
- HCI command/event dispatch via `tlk_ble_controller_hci_handler` and
  `tlk_ble_controller_hci_registerEventHandler`
- Kconfig-selectable BLE Controller capabilities: accept list, resolving list, legacy
  advertising/scanning, and ACL central/peripheral roles

## How It Works

### adv_demo

1. **RF Configuration** — `rf_configure()` sets up the radio in `TLK_RF_MODE_BLE` mode, 1M
   bitrate, channel 37, TX power 4, with the standard BLE advertising access code
   `0xd6be898e`.
2. **PDU Setup** — A fixed-content advertising PDU is prepared in `tx_buffer`: advertiser address
   `3c:cf:b4:03:e3:23`, AD flags, complete local name `"adv_demo"`, and an appearance field.
3. **Main Loop** — Repeatedly prepares and transmits the packet, toggles LED2 on each iteration,
   waits for the transmission to complete, then delays 100 ms before repeating:

```c
while (1)
{
    tlk_rf_tx_prepare_packet(tx_packet, TX_PDU_SIZE);

    tlk_gpio_pin_toggle(PINMUX_LED_2_PORT, PINMUX_LED_2_PIN);

    tlk_rf_start_stx(tlk_rf_get_tick());

    while (!tlk_rf_instance.tx_end)
    {
    }

    tlk_sys_delay(TLK_MS_TO_US(TX_DELAY_MS));
}
```

### ble_controller_demo

1. **UART Configuration** — Configures UART1 at 115200-8N1, with TX on GPIO port B pin 3 and RX
   on GPIO port B pin 2, used as the HCI transport.
2. **Controller Initialization** — Calls `tlk_ble_controller_initial()` and registers
   `app_ble_controller_hci_send_data` (via `tlk_ble_controller_hci_registerEventHandler`) so
   that outgoing HCI events are written back to the UART.
3. **Main Loop** — Receives HCI command bytes from the UART into `hci_rx_buffer` and, once a full
   receive completes, forwards them to `tlk_ble_controller_hci_handler`. The controller stack
   processes the command and emits HCI events through the registered callback, which sends them
   back out over the same UART.

This models a standard UART HCI transport for driving the Telink BLE Controller from an external
Host implementation (e.g. a PC-based Host stack or a Host running on another MCU).

## Configuration Options

`ble_controller_demo` exposes the BLE Controller stack sizing/feature options directly (there is
no dedicated demo submenu):

| Option | Description |
|------|------|
| `CONFIG_TLK_BLE_CONTROLLER_HCI_ACL_DATA_SIZE` | Maximum HCI ACL data payload size (default `50`) |
| `CONFIG_TLK_BLE_CONTROLLER_HCI_ACL_BUFFER_COUNT` | Number of HCI ACL buffers (default `10`) |
| `CONFIG_TLK_BLE_CONTROLLER_ACCEPT_LIST_ENABLE` | Enable the controller accept (white) list (default `y`) |
| `CONFIG_TLK_BLE_CONTROLLER_RESOLVING_LIST_ENABLE` | Enable the resolving list for address resolution (default `y`) |
| `CONFIG_TLK_BLE_CONTROLLER_LEGACY_ADV_ENABLE` | Enable legacy advertising (default `y`) |
| `CONFIG_TLK_BLE_CONTROLLER_LEGACY_SCAN_ENABLE` | Enable legacy scanning (default `y`) |
| `CONFIG_TLK_BLE_CONTROLLER_ACL_PERIPHERAL_ENABLE` | Enable the ACL peripheral (slave) role (default `y`) |
| `CONFIG_TLK_BLE_CONTROLLER_ACL_PERIPHERAL_MAX_NUM` | Maximum concurrent peripheral connections (default `1`) |
| `CONFIG_TLK_BLE_CONTROLLER_ACL_CENTRAL_ENABLE` | Enable the ACL central (master) role (default `y`) |
| `CONFIG_TLK_BLE_CONTROLLER_ACL_CENTRAL_MAX_NUM` | Maximum concurrent central connections (default `1`) |
| `CONFIG_TLK_BLE_CONTROLLER_ACL_RX_MAX_LENGTH` | Maximum ACL RX payload length (default `27`) |

`adv_demo` has no demo-specific Kconfig options; it only selects `TLK_RF` and `TLK_GPIO`.

## Build & Run

```bash
# adv_demo — raw advertising over the RF driver
west tl-build samples/adv_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/adv_demo.bin
```

```bash
# ble_controller_demo — full BLE Controller with UART HCI transport
west tl-build samples/ble_controller_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/ble_controller_demo.bin
```

## Related Resources

- [BLE Controller Documentation](../connectivity/ble/controller.md)
- [BLE Host Sample](ble_host.md) — newer SAL-based BLE Host stack sample (`samples/ble_host_demo`)

Source code: `samples/adv_demo/main.c`, `samples/ble_controller_demo/main.c`
