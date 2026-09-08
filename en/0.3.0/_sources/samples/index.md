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
| [PMP Sample](pmp.md) | Physical Memory Protection driver demo | DRAFT |
| [User Mode Sample](umode.md) | RISC-V User Mode / Machine Mode switching | DRAFT |

### Communication Interfaces

| Sample | Description | Status |
|------|------|------|
| [ADC Sample](adc.md) | ADC analog-to-digital conversion | DRAFT |
| [DMA Sample](dma.md) | DMA direct memory access | DRAFT |
| [I2C Sample](i2c.md) | I2C master-slave communication (DS1307 / Ping-Pong) | DRAFT |
| [SPI Sample](spi.md) | SPI master-slave communication | DRAFT |
| [I2S Sample](i2s.md) | I2S master/slave audio streaming | DRAFT |

### Wireless Connectivity

| Sample | Description | Status |
|------|------|------|
| [BLE Sample](ble.md) | Raw RF advertising and BLE Controller HCI demos | DRAFT |
| [BLE Host Sample](ble_host.md) | BLE Host v2 peripheral with GATT services | DRAFT |
| [RF Sample](rf.md) | RF driver ping-pong demo (BLE/Zigbee/Private/Hybee) | DRAFT |

### System Features

| Sample | Description | Status |
|------|------|------|
| [IRQ Nesting](irq_nesting.md) | Interrupt nesting demo | DRAFT |
| [Timer Sample](stimer.md) | STIMER system timer demo | DRAFT |
| [Watchdog Sample](wdt.md) | Watchdog timer demo | DRAFT |
| [USB CDC Sample](usb_cdc.md) | TinyUSB CDC serial port demo | DRAFT |
| [Random Sample](random.md) | Hardware random number generation | DRAFT |
| [NV Storage Sample](nv_storage.md) | Non-volatile storage device read/write/erase | DRAFT |
| [Log Sample](system_log.md) | Debug logging over the console/USB | DRAFT |
| [Task Planner Sample](task_planner.md) | Cooperative loop, scheduler, and software timer execution models | DRAFT |

### Audio & Security

| Sample | Description | Status |
|------|------|------|
| [Audio Sample](audio.md) | Audio input/output capture and playback via I2S/DMA | DRAFT |
| [mbedTLS Sample](mbedtls.md) | PSA Crypto random, ECDSA key generation, sign/verify | DRAFT |
| [MCUboot Bootloader Sample](mcuboot.md) | MCUboot bootloader with optional UART DFU recovery | DRAFT |

## Building Samples

All samples use a unified build approach:

```bash
# West command (recommended)
west tl-build samples/gpio_demo --board TLSR9528A_EVK

# Make command
make build APP=samples/gpio_demo BOARD=TLSR9528A_EVK
```

Each sample directory typically contains:

:::{dropdown} Sample Directory Structure
:summary: Click to expand/collapse

```text
samples/gpio_demo/
├── CMakeLists.txt    # Build entry
├── Kconfig           # Sample-specific configuration options
├── main.c            # Main program
├── main.cpp          # C++ version (optional)
└── README.md         # Sample description
```
:::
