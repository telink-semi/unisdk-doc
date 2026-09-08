---
title: SPI Sample
status: DRAFT
---

# SPI Sample

:::{note} Document Status: DRAFT — Content is being finalized
:::

## Overview

The `spi_demo` sample demonstrates SPI master/slave communication on `tlk_spi0`, using a command byte to select between a write and a read phase. The role (master or slave) is selected at build time.

## Features Demonstrated

- SPI pinmux configuration (`tlk_spi_pinmux_configure`) for CS/SCK/MOSI/MISO
- SPI master configuration and command-based transfers (`tlk_spi_master_configure`, `tlk_spi_master_xfer` with `struct tlk_spi_xfer`)
- SPI slave configuration with a command handler (`tlk_spi_slave_configure`, `tlk_spi_slave_set_handler`, `tlk_spi_slave_read`/`tlk_spi_slave_write`)
- LED toggling to visualize transfer activity and success

## How It Works

### Initialization

Both roles share pin and mode setup:

```c
struct tlk_spi_config config = {
    .mode    = TLK_SPI_MODE0,
    .io_mode = TLK_SPI_SINGLE_MODE,
    /* lower the frequency in case of errors on the slave side, if the master's div allows it */
    .frequency = 2 * 1000 * 1000,
};

struct tlk_spi_pinmux pinmux = {
    .cs   = {.port = TLK_GPIO_PORT_E, .pin = TLK_GPIO_PIN_0},
    .sck  = {.port = TLK_GPIO_PORT_E, .pin = TLK_GPIO_PIN_1},
    .mosi = {.port = TLK_GPIO_PORT_E, .pin = TLK_GPIO_PIN_2},
    .miso = {.port = TLK_GPIO_PORT_E, .pin = TLK_GPIO_PIN_3},
};

tlk_gpio_configure(PINMUX_LED_0_PORT, PINMUX_LED_0_PIN, TLK_GPIO_OUTPUT);
tlk_gpio_configure(PINMUX_LED_1_PORT, PINMUX_LED_1_PIN, TLK_GPIO_OUTPUT);

tlk_core_interrupt_enable();

tlk_spi_pinmux_configure(dev, &pinmux);
```

SPI runs in mode 0, single-IO mode, at 2 MHz.

### Master Role (`CONFIG_TLK_SPI_DEMO_ROLE_MASTER`)

The master issues two command-tagged transfers per loop using `struct tlk_spi_xfer` with `use_cmd = 1`:

```c
xfer.type = TLK_SPI_DUMMY_TX;
xfer.cmd  = COMMAND_WRITE;
status = tlk_spi_master_xfer(dev, &xfer);
...
xfer.type = TLK_SPI_DUMMY_RX;
xfer.cmd  = COMMAND_READ;
status = tlk_spi_master_xfer(dev, &xfer);
```

`COMMAND_WRITE` (1) sends `tx_data` to the slave; `COMMAND_READ` (2) reads back into `rx_data`. LED0 toggles every cycle; LED1 toggles when the first byte of `tx_data` matches the first byte of `rx_data`, indicating a successful round trip. A 10 ms delay separates the write and read phases, and a 1 second delay separates loop iterations.

### Slave Role (`CONFIG_TLK_SPI_DEMO_ROLE_SLAVE`)

The slave registers a command handler and then idles in an empty `while (1)` loop, relying entirely on the interrupt-driven handler:

```c
void handler(struct tlk_spi_device* dev, tlk_spi_cmd_t cmd)
{
    tlk_gpio_pin_toggle(PINMUX_LED_0_PORT, PINMUX_LED_0_PIN);

    switch (cmd)
    {
    case COMMAND_WRITE:
        tlk_spi_slave_read(dev, rx_data, BUFFER_SIZE);
        break;
    case COMMAND_READ:
        tlk_spi_slave_write(dev, tx_data, BUFFER_SIZE);
        break;
    default:
        break;
    }
}
```

On `COMMAND_WRITE` the slave reads the incoming bytes into `rx_data`; on `COMMAND_READ` it writes `tx_data` back to the master. LED0 toggles on every command received.

## Configuration Options

| Option | Description |
|------|------|
| `TLK_SPI_DEMO_ROLE_MASTER` | Build as SPI master — choice option |
| `TLK_SPI_DEMO_ROLE_SLAVE` | Build as SPI slave — choice option |

The base `TLK_SPI_DEMO` config selects `TLK_SPI`, `TLK_SPI0`, and `TLK_API_TIME` unconditionally; exactly one role must be selected (`choice` block). `TLK_BLE_CONTROLLER` is explicitly disabled (`default n`) for this sample.

## Build & Run

```bash
west tl-build samples/spi_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/Telink.bin
```

Source code: `samples/spi_demo/main.c`
