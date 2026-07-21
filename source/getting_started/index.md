---
title: Getting Started
status: STABLE
---

# Overview

## About This Document

This document guides you through the complete process of getting started with Telink UniSDK (Unified Software Development Kit)  - from setting up the development environment, obtaining the SDK, and compiling and flashing your first project, to successfully running the first example. This guide is designed for embedded software developers who are new to the UniSDK and have a basic understanding of the C programming language and embedded development fundamentals.

## Scope

Telink UniSDK supports the Bluetooth® Low Energy (BLE) protocol stack. It is applicable to the following chip series:

| Chip Series | Core |
|---|---|
| [TL321X](https://doc.telink-semi.cn/doc/hardware/devboard/UM-TL3218X-E_TL3218X_Development_Board_User_Manual.pdf) | RISC-V |
| [TL721X](https://doc.telink-semi.cn/doc/hardware/devboard/UM-TL7218X-E_TL7218X_Development_Board_User_Manual.pdf) | RISC-V |
| [TLSR922X](https://doc.telink-semi.cn/doc/hardware/devboard/UM-TLSR9528A-E_TLSR9528A_Development_Board_User_Manual.pdf) | RISC-V |
| [TLSR952X](https://doc.telink-semi.cn/doc/hardware/devboard/UM-TLSR9528A-E_TLSR9528A_Development_Board_User_Manual.pdf) | RISC-V |

See the [Release Notes](../releases/index.md) for details on supported chips and development boards.

## Hardware and Software Requirements

### Hardware Requirements

- A Telink official evaluation kit (choose one):
  - TL3218X_EVK
  - TL7218X_EVK
  - TLSR9528A_EVK
  - TLSR9228A_EVK
  - TLSR9528A_DONGLE
- A Telink programmer for flashing firmware (choose one):
  - Programmer V1.0 ~ V3.0
  - Programmer V5.0

### Software Requirements

| Component | Description |
|---|---|
| Operating System | Linux (Ubuntu 20.04+), Windows 10/11, macOS 12+ |
| Git | Version control system |
| CMake | Build system generator (>= 3.20.0) |
| Ninja | Build system runner (>= 1.10) |
| Python | Scripting and west tool runtime (>= 3.10) |
| West | Zephyr project management tool (>= 0.14.0) |
| Telink RISC-V Toolchain | Cross-compilation toolchain (RISC-V GCC V5.4.1+) |
| BDT | Telink Burning and Debugging Tool (for flashing) |

### Quick Start Flow

Follow these steps in order:

1. **[Set Up the Development Environment](environment_setup.md)** — Install VS Code Extension and dependencies
2. **[Get and Import the SDK](get_sdk.md)** — Clone the repository and understand the directory layout
3. **[Compile, Flash and Run Your First Example](first_example.md)** — Build and run the gpio_demo

## Next Steps

- [Development Guide](../developing/index.md) — Deep dive into the SDK development workflow
- [Build & Configuration](../build_config/index.md) — Learn the CMake and Kconfig build system
- [Samples & Demos](../samples/index.md) — Explore more example projects
- [Peripherals & Drivers](../peripherals/index.md) — Learn to use GPIO, UART, I2C and other peripheral drivers
