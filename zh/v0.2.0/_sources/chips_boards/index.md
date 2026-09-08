---
title: Chips and Boards
status: STABLE
---

# Chips and Boards

## Chip Series Overview

UniSDK supports the following Telink chip series:

| Chip Series | Core | Flash | SRAM | Key Peripherals | Typical Application |
|---------|------|-------|------|---------|---------|
| [TL321X](chips/TL321X.md) | RISC-V | — | — | BLE, GPIO, UART, I2C, SPI, ADC, DMA | General IoT |
| [TL721X](chips/TL721X.md) | RISC-V | — | — | BLE, GPIO, UART, I2C, SPI, ADC, DMA, USB | General IoT |
| [TLSR922X](chips/TLSR922X.md) | RISC-V | — | — | BLE, GPIO, UART, I2C, SPI, ADC | General IoT |
| [TLSR952X](chips/TLSR952X.md) | RISC-V | — | — | BLE, GPIO, UART, I2C, SPI, ADC, DMA | General IoT |

## Selecting a Chip

```bash
# List all supported chips
west tl-socs

# List detailed chip information
west tl-socs -v
```

## Board List

| Board | Chip | Description |
|--------|---------|------|
| [TL3218X_EVK](boards/TL3218X_EVK.md) | TL321X | TL321X Evaluation Kit |
| [TL7218X_EVK](boards/TL7218X_EVK.md) | TL721X | TL721X Evaluation Kit |
| [TLSR9228A_EVK](boards/TLSR9228A_EVK.md) | TLSR922X | TLSR922X Evaluation Kit |
| [TLSR9528A_EVK](boards/TLSR9528A_EVK.md) | TLSR952X | TLSR952X Evaluation Kit |
| [TLSR9528A_DONGLE](boards/TLSR9528A_DONGLE.md) | TLSR952X | TLSR952X USB Dongle |

```bash
# List all supported boards
west tl-boards

# Filter boards by chip
west tl-boards --soc TLSR9528A

# List detailed board information
west tl-boards -v
```

## Chip and Board Pair Validation

```bash
# Validate combination
west tl-config --validate TLSR9528A TLSR9528A_EVK
```

## Specifying at Build Time

```bash
# Specify chip via command line arguments
west tl-build samples/gpio_demo --soc TLSR9528A
# Specify board via command line arguments
west tl-build samples/gpio_demo --board TLSR9528A_EVK

# Specify chip via CMake arguments
cmake -B build -DSOC=TLSR9528A -S .
# Specify board via CMake arguments
cmake -B build -DBOARD=TLSR9528A_EVK -S .
```
