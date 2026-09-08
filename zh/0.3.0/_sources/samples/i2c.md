---
title: I2C Sample
status: DRAFT
---

# I2C Sample

:::{note} Document Status: DRAFT — Content is being finalized
:::

## Overview

The `i2c_demo` sample includes two independent sub-samples that both configure `tlk_i2c0` on GPIO port C pins 6/7 (SCL/SDA):

- **`ds1307`** — I2C master driving a DS1307 real-time-clock chip: periodically reads the current time and, on a button press, writes a new time.
- **`ping_pong`** — a minimal I2C master/slave loopback demo (role selected at build time) that exchanges a fixed 8-byte buffer and toggles LEDs on activity.

## Features Demonstrated

- I2C pinmux and master configuration (`tlk_i2c_pinmux_configure`, `tlk_i2c_master_configure`)
- Single-buffer master writes/reads (`tlk_i2c_master_write`, `tlk_i2c_master_read`)
- Combined write+read transactions using `tlk_i2c_master_xfer` with a `struct tlk_i2c_message` array (DS1307 register-pointer + burst read pattern)
- I2C slave mode configuration and event-driven handler (`tlk_i2c_slave_configure`, `tlk_i2c_slave_set_handler`, `TLK_I2C_EVENT_WRITE_REQUEST` / `TLK_I2C_EVENT_READ_REQUEST` / `TLK_I2C_EVENT_STOP`)
- GPIO interrupt integration: the DS1307 sample sets the time from a button-press callback (`tlk_gpio_irq_add_callback`)

## How It Works

### ds1307 sub-sample

`main.c` configures the I2C pinmux and master mode, then arms a GPIO interrupt on `KEY_0` (rising edge) whose callback writes a new fixed time to the RTC via `ds1307_set_time`:

```c
struct tlk_i2c_pinmux_config pinmux = {
    .scl_port_pin = {.port = TLK_GPIO_PORT_C, .pin = TLK_GPIO_PIN_6},
    .sda_port_pin = {.port = TLK_GPIO_PORT_C, .pin = TLK_GPIO_PIN_7},
};

tlk_i2c_pinmux_configure(dev, &pinmux);

struct tlk_i2c_master_config config = {
    .clock_speed = 100000,
    .stretch_en  = 1,
};

tlk_i2c_master_configure(dev, &config);
```

The main loop reads the current time every second via `ds1307_read_time` and logs it. The DS1307 driver (`ds1307.c`) implements the register protocol on top of the I2C API:

- `ds1307_set_time` writes an 8-byte buffer (start register `0x00` followed by BCD-encoded sec/min/hour/day/date/month/year) with a single `tlk_i2c_master_write`.
- `ds1307_read_time` issues a combined transaction with `tlk_i2c_master_xfer`: a 1-byte write of the register pointer followed by a 7-byte read, using two `struct tlk_i2c_message` entries (`is_read = 0` then `is_read = 1`).

### ping_pong sub-sample

Depending on `CONFIG_TLK_I2C_DEMO_ROLE_MASTER` / `CONFIG_TLK_I2C_DEMO_ROLE_SLAVE`, `main.c` builds one of two roles against slave address `0x5a`:

- **Master**: repeatedly writes an 8-byte buffer (`"i2c_demo"`) with `tlk_i2c_master_write`, then reads it back with `tlk_i2c_master_read`, and logs whether the round-tripped data matches. Delays between operations via `tlk_api_time_delay`, or `tlk_api_sleep` if `CONFIG_TLK_I2C_DEMO_PM` is enabled.
- **Slave**: configures slave mode with `tlk_i2c_slave_configure`, registers an event handler with `tlk_i2c_slave_set_handler`, and sets its TX/RX buffers with `tlk_i2c_slave_set_tx` / `tlk_i2c_slave_set_rx`. The handler toggles LED0 on a write request, toggles LED1 and echoes the received buffer back into the TX buffer on a read request, and logs on a stop condition:

```c
void handler(struct tlk_i2c_device* dev, enum tlk_i2c_event event)
{
    switch (event)
    {
    case TLK_I2C_EVENT_WRITE_REQUEST:
        tlk_gpio_pin_toggle(PINMUX_LED_0_PORT, PINMUX_LED_0_PIN);
        break;
    case TLK_I2C_EVENT_READ_REQUEST:
        tlk_gpio_pin_toggle(PINMUX_LED_1_PORT, PINMUX_LED_1_PIN);
        memcpy(tx_buffer, rx_buffer, BUFFER_SIZE);
        break;
    case TLK_I2C_EVENT_STOP:
        TLK_LOG_INFO(i2c_demo, "Stop received.");
        break;
    default:
        break;
    }
}
```

## Configuration Options

### ds1307

The `TLK_I2C_DEMO` config for this sub-sample selects `TLK_I2C`, `TLK_I2C0`, `TLK_I2C0_MASTER`, `TLK_GPIO`, and `TLK_PLIC` unconditionally (no sub-options exposed).

### ping_pong

| Option | Description |
|------|------|
| `TLK_I2C_DEMO_ROLE_MASTER` | Build as I2C master (selects `TLK_I2C0_MASTER`) — choice option, default role |
| `TLK_I2C_DEMO_ROLE_SLAVE` | Build as I2C slave (selects `TLK_I2C0_SLAVE`) — choice option |
| `CONFIG_TLK_I2C_DEMO_PM` | Master role only: use `tlk_api_sleep` for the end-of-loop delay; selects `TLK_API_SLEEP` and implies `TLK_I2C0_PM_DEVICE` |

The base `TLK_I2C_DEMO` config selects `TLK_I2C` and `TLK_I2C0` unconditionally; exactly one of the two role options must be selected (`choice` block).

## Build & Run

```bash
# ds1307
west tl-build samples/i2c_demo/ds1307 --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/Telink.bin

# ping_pong
west tl-build samples/i2c_demo/ping_pong --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/Telink.bin
```

Source code: `samples/i2c_demo/ds1307/main.c`, `samples/i2c_demo/ds1307/ds1307.c`, `samples/i2c_demo/ping_pong/main.c`
