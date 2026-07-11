---
title: Glossary
status: STABLE
---

# UniSDK Glossary

This document defines the core terminology used in UniSDK to ensure consistency across documentation and community communication.

## Build System

| Term | Description |
|------|-------------|
| Build System | CMake + Ninja based compilation framework |
| Configuration System | Kconfig-based compile-time configuration management |
| Target | CMake build target, can be an executable or library |
| Generator | CMake build backend; UniSDK uses Ninja |
| Pre-build Check | Validation scripts that run automatically before compilation |

## West Tool

| Term | Description |
|------|-------------|
| West | Zephyr project management tool, the unified build entry point in UniSDK |
| Workspace | The project directory managed by West, containing `.west` configuration |
| tl-build | UniSDK custom West command for building projects |
| tl-config | UniSDK custom West command for configuring projects |
| tl-bdt | UniSDK custom West command for flashing and debugging |

## Hardware Abstraction

| Term | Description |
|------|-------------|
| Chip / SoC | Telink System-on-Chip |
| Board / EVK | Telink official Evaluation Kit |
| Pinmux | Programmable chip pin function configuration |
| Core Layer | Chip core driver code (`core/`) |
| SoC Layer | Chip-specific functionality code (`soc/`) |

## Kconfig Configuration

| Term | Description |
|------|-------------|
| Kconfig | Linux kernel configuration system |
| chip.config | Chip-specific configuration |
| build.config | Build option configuration |
| .config | Final merged configuration |
| autoconf.h | C language configuration macro definition header file |
| capabilities.h | Chip capability declaration header file |
| Menuconfig | Terminal-based interactive configuration interface |

## Peripherals & Drivers

| Term | Description |
|------|-------------|
| GPIO | General Purpose Input/Output |
| UART | Universal Asynchronous Receiver/Transmitter |
| I2C | Inter-Integrated Circuit |
| SPI | Serial Peripheral Interface |
| ADC | Analog-to-Digital Converter |
| DMA | Direct Memory Access |
| PM | Power Management |
| PLIC | Platform-Level Interrupt Controller |

## Document Status Markers

| Marker | Description |
|--------|-------------|
| STABLE | Content is complete and ready to use |
| DRAFT | Content is being written, may be incomplete |
| DEPRECATED | Will be deprecated soon; migration to new solution is recommended |
| PLANNED | Planned but not yet started |
