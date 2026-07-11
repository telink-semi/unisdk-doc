---
title: Samples & Demos
status: STABLE
---

# Samples & Demos

UniSDK provides a rich set of ready-to-compile-and-run sample programs in the `samples/` directory. Each sample demonstrates the usage of one or more SDK features.

## Sample List

### Basic Peripherals

| Sample | Description | Status |
|------|------|------|
| [GPIO Sample](gpio.md) | GPIO input/output, interrupt handling, sleep API | STABLE |
| [UART Sample](uart.md) | UART echo, sleep test, TX/RX protection | STABLE |
| [PM Power Management](pm.md) | Low-power modes, GPIO wake-up, retention variables | STABLE |

### Communication Interfaces

| Sample | Description | Status |
|------|------|------|
| [ADC Sample](adc.md) | ADC analog-to-digital conversion | DRAFT |
| [DMA Sample](dma.md) | DMA direct memory access | DRAFT |
| [I2C Sample](i2c.md) | I2C master-slave communication (DS1307 / Ping-Pong) | DRAFT |
| [SPI Sample](spi.md) | SPI master-slave communication | DRAFT |

### Wireless Connectivity

| Sample | Description | Status |
|------|------|------|
| [BLE Sample](ble.md) | BLE advertising and connection demo | DRAFT |

### System Features

| Sample | Description | Status |
|------|------|------|
| [IRQ Nesting](irq_nesting.md) | Interrupt nesting demo | DRAFT |
| [Timer Sample](stimer.md) | STIMER system timer demo | DRAFT |
| [Watchdog Sample](wdt.md) | Watchdog timer demo | DRAFT |
| [USB CDC Sample](usb_cdc.md) | TinyUSB CDC serial port demo | DRAFT |

## Building Samples

All samples use a unified build approach:

```bash
# West command (recommended)
west tl-build samples/gpio_demo --board TLSR9528A_EVK

# Make command
make build APP=samples/gpio_demo BOARD=TLSR9528A_EVK
```

Each sample directory typically contains:

```
samples/gpio_demo/
├── CMakeLists.txt    # Build entry
├── Kconfig           # Sample-specific configuration options
├── main.c            # Main program
├── main.cpp          # C++ version (optional)
└── README.md         # Sample description
```
