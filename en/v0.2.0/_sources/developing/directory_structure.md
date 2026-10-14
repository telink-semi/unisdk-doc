---
title: SDK Directory Structure
status: STABLE
---

# SDK Directory Structure

This document details the directory organization of the UniSDK code repository to help developers quickly locate various resources.

## Overall Structure

:::{dropdown} UniSDK Directory Tree
:summary: Click to expand/collapse the full SDK directory structure

```text
unisdk/
├── CMakeLists.txt              # CMake main entry point (root directory mode)
├── Makefile                    # Make command interface
├── west.yml                    # West workspace configuration
├── Kconfig.chip               # Chip Kconfig entry point
├── Kconfig.build              # Build Kconfig entry point
├── readme.md                   # Project overview
│
├── api/                        # Public API layer
│   ├── include/                # API header files
│   ├── src/                    # API implementations
│   ├── CMakeLists.txt
│   └── Kconfig
│
├── core/                       # Chip core drivers
│   ├── B92/
│   ├── TL321X/
│   ├── TL721X/
│   ├── common/
│   ├── configs/
│   ├── cpp_wrappers/
│   ├── include/
│   └── CMakeLists.txt
│
├── soc/                        # SoC layer
│   ├── TL321X/
│   ├── TL721X/
│   ├── TLSR922X/
│   └── TLSR952X/
│
├── boards/                     # Board configurations
│   ├── TL3218X_EVK/
│   ├── TL7218X_EVK/
│   ├── TLSR9228A_EVK/
│   ├── TLSR9528A_EVK/
│   └── TLSR9528A_DONGLE/
│
├── common/
│   ├── include/
│   └── src/
│
├── subsystem/
│   └── ble/
│       └── controller/
│
├── modules/
│   └── tinyUSB/
│
├── samples/
│   ├── gpio_demo/
│   ├── uart_demo/
│   ├── pm_demo/
│   ├── adc_demo/
│   ├── dma_demo/
│   ├── i2c_demo/
│   ├── spi_demo/
│   ├── adv_demo/
│   └── ...
│
├── cmake/
│   ├── modules/
│   └── TelinkConfig.cmake
│
└── scripts/
    ├── west_commands/
    ├── pinmux/
    ├── kconfig.py
    ├── menuconfig.py
    └── ...
```
:::

## Key Directory Responsibilities

### `api/` — Public API Layer

Provides the most commonly used unified API interfaces for application development. All example applications should be developed using the APIs in `api/`. Main contents include:

- `tlk_sleep.h` / `tlk_time.h` — Sleep delay and time management

### `core/` — Core Driver Layer

Organized by chip family, includes:

- **drivers/** — Peripheral driver implementations (GPIO, UART, I2C, SPI, ADC, DMA, etc.)
- **properties/** — YAML-format device property descriptions
- **registers/** — YAML-format register definitions
- **configs/** — Kconfig configuration options

### `soc/` — SoC-Specific Layer

Contains chip-specific features:

- **drivers/** — Platform-specific drivers (MSPI, OTP, etc.)
- **pinmux/** — Pin multiplexing definitions (yaml files for each package variant)
- **registers/** — Chip-specific register definitions

### `boards/` — Development Board Configurations

Contains only board-specific pin mapping configurations (`board_pinout.yaml`).

## Code Organization Principles

1. **Public APIs go in `api/`** — Interfaces shared by all chips
2. **Core drivers go in `core/`** — Peripheral drivers for each chip family
3. **Chip-specific code goes in `soc/`** — Features unique to a particular chip
4. **Application code goes anywhere** — Not limited to the `samples/` directory
5. **Use Kconfig for configuration** — Manage compile-time options with Kconfig
