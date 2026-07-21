---
title: Peripherals and Drivers
status: STABLE
---

# Peripherals and Drivers

UniSDK provides a unified peripheral driver API for the entire Telink chip family. All drivers follow a consistent programming model and naming convention.

## Driver Overview

| Driver | API Prefix | Transfer Mode | Description |
|------|---------|---------|------|
| [GPIO](gpio.md) | `tlk_gpio_*` | Direct Register | General-purpose input/output, interrupt handling |
| [UART](uart.md) | `tlk_uart_*` | Blocking / PLIC / DMA | Universal asynchronous receiver/transmitter, flow control |
| [Power Management PM](pm.md) | `tlk_pm_*` | — | Low-power mode management |
| [Analog](analog.md) | `tlk_analog_*` | Direct Register | Analog register access |
| [PLIC](plic.md) | `tlk_plic_*` | — | Platform-level interrupt controller |
| [I2C](i2c.md) | `tlk_i2c_*` | Blocking / DMA | I2C master/slave communication |
| [SPI](spi.md) | `tlk_spi_*` | Blocking / DMA | SPI master/slave communication |
| [ADC](adc.md) | `tlk_adc_*` | Blocking | Analog-to-digital conversion |
| [DMA](dma.md) | `tlk_dma_*` | DMA | Direct memory access |
| [Watchdog](wdt.md) | `tlk_wdt_*` | — | Watchdog timer |
| [Timer](timer.md) | `tlk_stimer_*` / `tlk_mtimer_*` | — | System/machine timer |
| [USB](usb.md) | `tlk_usb_*` + TinyUSB | — | USB CDC, etc. |

## Driver Programming Model

All UniSDK drivers follow a unified programming model:

### Configure → Use → Deinitialize

```c
// 1. Configure (via menuconfig or code)
tlk_gpio_configure(GPIO_PORT_A, GPIO_PIN_0, TLK_GPIO_OUTPUT);

// 2. Use
tlk_gpio_pin_write(GPIO_PORT_A, GPIO_PIN_0, true);

// 3. Optional: Disable
tlk_gpio_disable(GPIO_PORT_A, GPIO_PIN_0);
```

### Transfer Modes

Some communication peripherals support multiple transfer modes:

- **Blocking** — Synchronously waits for transfer completion, suitable for simple scenarios
- **PLIC (Interrupt)** — Non-blocking transfer based on interrupts, no CPU polling required
- **DMA** — Most efficient bulk data transfer, zero CPU load

Configure transfer mode independently for each peripheral instance via Kconfig.

## Kconfig Configuration

All peripheral drivers are configured at compile time via Kconfig. See [Kconfig Reference](../kconfig_reference/index.md) for all configuration options.

Quick configuration entry:

```bash
# Interactive configuration
west tl-config

# or directly use
make config
```
