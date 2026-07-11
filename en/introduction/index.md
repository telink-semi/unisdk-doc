---
title: Introduction
status: STABLE
---

# UniSDK Introduction

## Telink Semiconductor

Telink Semiconductor is a company focused on designing low-power wireless connectivity chips, providing complete chip solutions covering protocols such as BLE, Zigbee, Thread, and Matter. Telink chips are widely used in smart homes, wearable devices, IoT sensors, and other scenarios.

## UniSDK Core Features and Advantages

UniSDK (Unified Software Development Kit) provides a unified software development platform for the full range of Telink chips. The core advantages include:

### Unified Development Experience

- **One Codebase, Multi-Chip Adaptation**: Based on a unified API layer and HAL abstraction, application code can seamlessly migrate between different Telink chips
- **Unified Build System**: All chip families share the same CMake + Kconfig build infrastructure

### Modern Build System

UniSDK integrates industry-proven build toolchains:

| Component | Purpose | Description |
|------|------|------|
| **CMake** | Build system core | Project configuration, dependency management, build rule generation |
| **Ninja** | Build execution engine | High-performance parallel compilation |
| **West** | Project management tool | Zephyr community-standard project management workflow |
| **Kconfig** | Configuration management system | Hierarchical management of compile-time configuration options |
| **Make** | Legacy interface | Frontend interface compatible with traditional Make usage habits |

### Rich Peripheral Drivers

Provides GPIO, UART, I2C, SPI, ADC, DMA, Watchdog, Timer, and other full-range peripheral drivers, encapsulating underlying hardware differences with a unified API.

### Low-Power Design

A comprehensive power management framework supporting multiple low-power modes, delivering excellent energy efficiency for battery-powered devices.

## Architecture Overview

```
┌──────────────────────────────────────────────┐
│               Application Layer              │
│        (User applications in samples/)       │
├──────────────────────────────────────────────┤
│                  API Layer                   │
│   (api/ unified API interface, HW abstraction)│
├──────────────────────────────────────────────┤
│              Subsystem Layer                 │
│    (subsystem/ BLE and other subsystems)     │
├────────────┬────────────┬────────────────────┤
│  Core B92  │ Core TL321X│  Core TL721X ...   │
│  (core/)   │            │                    │
├────────────┴────────────┴────────────────────┤
│              SoC Layer (soc/)                │
│  Chip-specific drivers, Pinmux, register defs│
├──────────────────────────────────────────────┤
│                Hardware                      │
│       (Telink full chip family)              │
└──────────────────────────────────────────────┘
```

## Supported Chip Families

| Chip Family | Core | Key Features | Typical Applications |
|---------|------|-----------|---------|
| **TL321X** | RISC-V | BLE, GPIO, UART, I2C, SPI, ADC, DMA | General IoT |
| **TL721X** | RISC-V | BLE, GPIO, UART, I2C, SPI, ADC, DMA, USB | General IoT |
| **TLSR922X** | RISC-V | BLE, GPIO, UART, I2C, SPI, ADC | General IoT |
| **TLSR952X** | RISC-V | BLE, GPIO, UART, I2C, SPI, ADC, DMA | General IoT |

## License

UniSDK is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Community Resources

- Official Website: [https://www.telink-semi.com](https://www.telink-semi.com)
- Technical Forum: [Telink Developer Forum](https://forum.telink-semi.cn)

## Next Steps

- [Getting Started](../getting_started/index.md) — Set up the development environment
- [Development Guide](../developing/index.md) — Deep dive into the SDK development workflow
- [Samples & Demos](../samples/index.md) — Run code examples directly
