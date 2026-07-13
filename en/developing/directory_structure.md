---
title: SDK Directory Structure
status: STABLE
---

# SDK Directory Structure

This document details the directory organization of the UniSDK code repository to help developers quickly locate various resources.

## Overall Structure

```
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
│   │   ├── tlk_sleep.h         #   Sleep/delay API
│   │   └── tlk_time.h          #   Time-related API
│   ├── src/                    # API implementations
│   ├── CMakeLists.txt
│   └── Kconfig
│
├── core/                       # Chip core drivers (organized by chip family)
│   ├── B92/                    # B92 series (TLSR952X)
│   │   ├── drivers/            #   Core driver implementations
│   │   ├── properties/         #   YAML device property descriptions
│   │   └── registers/          #   YAML register descriptions
│   ├── TL321X/                 # TL321X series
│   ├── TL721X/                 # TL721X series
│   ├── common/                 # Core common code
│   │   ├── startup/            #   Startup files
│   │   │   ├── cstartup_flash.S #      Assembly startup code
│   │   │   ├── flash_boot.link #      Linker script
│   │   │   └── tl_context.S    #      Context switch
│   │   └── src/
│   ├── configs/                # Core Kconfig configuration
│   ├── cpp_wrappers/           # C++ wrappers
│   ├── include/                # Core common header files
│   └── CMakeLists.txt
│
├── soc/                        # SoC layer (chip-specific features)
│   ├── TL321X/
│   │   ├── drivers/            #   SoC-specific drivers
│   │   ├── pinmux/             #   Pin multiplexing configuration (yaml)
│   │   ├── properties/         #   SoC properties (yaml)
│   │   └── registers/          #   Register definitions (yaml)
│   ├── TL721X/
│   ├── TLSR922X/
│   └── TLSR952X/
│
├── boards/                     # Development board configurations
│   ├── TL3218X_EVK/            # Pinmux configurations for each dev board
│   ├── TL7218X_EVK/
│   ├── TLSR9228A_EVK/
│   ├── TLSR9528A_EVK/
│   └── TLSR9528A_DONGLE/
│
├── common/                     # Common libraries
│   ├── include/                #   Common headers (linked lists, bit operations, etc.)
│   └── src/
│
├── subsystem/                  # Functional subsystems
│   └── ble/
│       └── controller/         #   BLE Controller
│
├── modules/                    # Third-party modules
│   └── tinyUSB/                #   TinyUSB integration
│
├── samples/                    # Example code
│   ├── gpio_demo/              # GPIO example
│   ├── uart_demo/              # UART example
│   ├── pm_demo/                # Power management example
│   ├── adc_demo/               # ADC example
│   ├── dma_demo/               # DMA example
│   ├── i2c_demo/               # I2C example
│   ├── spi_demo/               # SPI example
│   ├── adv_demo/               # BLE advertising example
│   └── ...                     # More examples
│
├── cmake/                      # CMake modules
│   ├── modules/                #   Core CMake modules
│   │   ├── compiler.cmake      #      Compiler configuration
│   │   ├── kconfig.cmake       #      Kconfig integration
│   │   ├── linker.cmake        #      Linker configuration
│   │   ├── pinmux.cmake        #      Pin multiplexing
│   │   └── ...
│   └── TelinkConfig.cmake      #   Telink package configuration
│
├── scripts/                    # Build scripts and tools
│   ├── west_commands/          #   West command extensions
│   ├── pinmux/                 #   Pinmux visual tool
│   ├── kconfig.py              #   Kconfig processing
│   ├── menuconfig.py           #   Interactive configuration
│   └── ...
│
└── docs/                       # Documentation
    ├── en/                     #   English documentation
    ├── images/                 #   Image assets
    └── ...
```

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
