---
title: RF Sample
status: DRAFT
---

# RF Sample

## Overview

The `rf_demo` sample demonstrates the RF driver capabilities by implementing a ping-pong application. It requires two devices for communication:

- **Transmitter** — sends a **ping** packet to the **Receiver**, then listens for the **pong** response. To avoid deadlocking, it has a timeout to resend the **ping** if no **pong** is received.
- **Receiver** — waits indefinitely for a **ping** packet, then sends a **pong** response once received.

```{.text}
Transmitter ---ping--> Receiver
Transmitter <--pong--- Receiver
```

LED1 indicates whether the chip is on or off (mainly useful with PM enabled). LED2 is toggled each time the Receiver sends a **pong**, or once the Transmitter's receive attempt ends (regardless of the result).

## Features Demonstrated

- RF configuration for BLE, Zigbee, Private, and Hybee modes (`tlk_rf_configure`)
- Multiple exchange APIs: Manual, STX/SRX, STR/SRT, BTX/BRX, PTX/PRX
- Transmitter and receiver roles (`CONFIG_TLK_RF_DEMO_ROLE_TRANSMITTER` / `_RECEIVER`)
- IRQ-driven and polling-mode packet handling
- Optional pipe switching and SB packet format (Private mode, PTX/PRX only)
- Optional power management integration (`CONFIG_TLK_RF_DEMO_PM`)

## How It Works

### Initialization

```c
int main(void)
{
    tlk_core_interrupt_enable();

    tlk_gpio_configure(PINMUX_LED_2_PORT, PINMUX_LED_2_PIN, TLK_GPIO_OUTPUT);
    tlk_gpio_configure(PINMUX_LED_1_PORT, PINMUX_LED_1_PIN, TLK_GPIO_OUTPUT);

    tlk_gpio_pin_write(PINMUX_LED_1_PORT, PINMUX_LED_1_PIN, 1);

    rf_configure(CONFIG_TLK_RF_DEMO_MODE, CONFIG_TLK_RF_DEMO_BITRATE);

#if TLK_IS_ENABLED(CONFIG_TLK_RF_DEMO_ROLE_TRANSMITTER)
    transmitter_loop();
#elif TLK_IS_ENABLED(CONFIG_TLK_RF_DEMO_ROLE_RECEIVER)
    receiver_loop();
#endif

    return 0;
}
```

`rf_configure()` builds a `struct tlk_rf_config` based on the selected mode (BLE, Zigbee, Private, Hybee), setting the RF channel, handling mode (IRQ or polling, per `CONFIG_TLK_RF_DEMO_POLLING_MODE`), and mode-specific parameters such as the BLE/Private access code and, for Private mode, the preamble length (derived from the selected bitrate) and optional SB packet format/length.

### Exchange APIs

`main.h`/`main.c` are shared across five `demo_*.c` files, each compiled only when its matching `CONFIG_TLK_RF_DEMO_EXCHANGE_*` option is selected, and each implementing `transmitter_loop()`/`receiver_loop()`:

- **Manual** (`demo_manual.c`) — Drives the RF state machine directly with `tlk_rf_set_tx_state`/`tlk_rf_start_tx_state`, polling `tlk_rf_instance.tx_end`/`rx_end`. Also supports optional mode switching between two configured modes each iteration, and BLE channel switching with fast-settle calibration.
- **STX & SRX** (`demo_stx_srx.c`) — Uses `tlk_rf_start_stx()` to transmit and `tlk_rf_start_srx()` to receive, as two separate blocking calls.
- **STR & SRT** (`demo_str_srt.c`) — Uses `tlk_rf_start_stx2rx()` on the transmitter (send then auto-switch to receive) and `tlk_rf_start_srx2tx()` on the receiver (receive then auto-switch to send).
- **BTX & BRX** (`demo_btx_brx.c`) — Uses `tlk_rf_start_btx()` / `tlk_rf_start_brx()`, the "block" variant of send-then-receive / receive-then-send.
- **PTX & PRX** (`demo_ptx_prx.c`) — Uses `tlk_rf_start_ptx()` / (implicit PRX receive), and is the only mode that supports pipe switching (`CONFIG_TLK_RF_DEMO_PIPE_SWITCHING`) across `UNISDK_RF_PIPE_COUNT` logical pipes, each with its own access code, and the SB packet format (`CONFIG_TLK_RF_DEMO_SB_FORMAT`).

Each variant times the round trip via `tlk_api_time_get_micros()` and reports it, together with RSSI, through `on_pong_received()`.

### Callbacks

```c
void on_pong_received(void)
{
    ...
    if (ping >= TLK_MS_TO_US(PING_TIMEOUT_MS) || tlk_rf_instance.rx_timeout_error)
    {
        TLK_LOG_INFO(rf_demo, "Error: Ping timeout.");
    }
    else if (tx_payload[0] == rx_payload[0])
    {
        TLK_LOG_INFO(rf_demo, "[%u] Received!", rx_payload[0]);
        TLK_LOG_INFO(rf_demo, "Time: %-4u us | RSSI: %i", ping, tlk_rf_instance.rx_rssi);
        success_packets++;
    }
    else
    {
        TLK_LOG_INFO(rf_demo, "Error: Diff in packets. Expected [%u], but got [%u].", tx_payload[0], rx_payload[0]);
    }

    TLK_LOG_INFO(rf_demo, "Count: %-6u | Success count: %u", sent_packets, success_packets);
    tlk_gpio_pin_toggle(PINMUX_LED_2_PORT, PINMUX_LED_2_PIN);
}
```

`on_ping_sent()`, `on_ping_received()`, `on_pong_sent()`, and `on_pong_received()` log each stage of the exchange; `on_pong_sent()` and `on_pong_received()` also toggle LED2.

:::{note} Power management
When `CONFIG_TLK_RF_DEMO_PM` is enabled, most exchange variants replace the fixed post-exchange delay with `tlk_api_sleep(1000 + 500)` (a 1.5 s low-power sleep, preceded by a short visible delay), and the sample implies `TLK_RF_PM_DEVICE`.
:::

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_RF_DEMO_PM` | Enable PM integration: sleeps between exchange iterations instead of delaying; selects `TLK_API_SLEEP` and implies `TLK_RF_PM_DEVICE`. |
| `CONFIG_TLK_RF_DEMO_MODE_{BLE,ZIGBEE,PRIVATE,HYBEE}` | Selects the RF protocol mode (choice). |
| `CONFIG_TLK_RF_DEMO_BITRATE_{125K,250K,500K,1M,2M}` | Selects the bitrate (choice); available options depend on the selected mode. |
| `CONFIG_TLK_RF_DEMO_ROLE_{TRANSMITTER,RECEIVER}` | Selects the device role (choice). |
| `CONFIG_TLK_RF_DEMO_EXCHANGE_{MANUAL,STX_SRX,STR_SRT,BTX_BRX,PTX_PRX}` | Selects the exchange API used for the ping-pong loop (choice). |
| `CONFIG_TLK_RF_DEMO_POLLING_MODE` | (Manual exchange only) Use polling mode instead of IRQ-driven handling. |
| `CONFIG_TLK_RF_DEMO_MODE_SWITCHING` | (Manual exchange only) Switch between the primary mode and a second configured mode each iteration. |
| `CONFIG_TLK_RF_DEMO_SECOND_MODE_*` / `CONFIG_TLK_RF_DEMO_SECOND_BITRATE_*` | (Manual + mode switching only) Mode/bitrate of the secondary configuration used when switching. |
| `CONFIG_TLK_RF_DEMO_CHANNEL_SWITCHING` | (Manual exchange, BLE mode, not combined with mode switching) Alternate between BLE channels 17 and 25 each iteration, using fast-settle calibration. |
| `CONFIG_TLK_RF_DEMO_SB_FORMAT` | (Private mode, PTX/PRX exchange) Use the SB packet format. |
| `CONFIG_TLK_RF_DEMO_PIPE_SWITCHING` | (Private mode, PTX/PRX exchange) Cycle transmissions across the device's logical pipes, each with a distinct access code. |

## Build & Run

```bash
west tl-build samples/rf_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/rf_demo.bin
```

:::{note}
Two boards are required to observe the ping-pong exchange: flash one with `CONFIG_TLK_RF_DEMO_ROLE_TRANSMITTER` and the other with `CONFIG_TLK_RF_DEMO_ROLE_RECEIVER`, using matching mode/bitrate/exchange-API configuration.
:::

Source code: `samples/rf_demo/main.c`
