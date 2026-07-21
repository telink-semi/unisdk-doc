---
title: Build & Configuration
status: STABLE
---

# Build & Configuration

UniSDK adopts a modular and extensible build system architecture, integrating tools such as CMake, Ninja, West, Kconfig, and Make to form a complete compilation and build workflow.

## Core Components

| Component | Purpose | Description |
|-----------|---------|-------------|
| **CMake** | Build system core | Project configuration, dependency management, build rule generation |
| **Ninja** | Build execution engine | High-performance parallel compilation, CMake's default backend |
| **West** | Project management tool | Unified command-line entry point, simplified build workflow |
| **Kconfig** | Configuration management system | Hierarchical management of compile-time configuration options |
| **Make** | Traditional interface | Frontend interface compatible with traditional Make conventions |

## Three Build Methods

UniSDK supports three build entry points, adapting to different scenarios:

```bash
# Method 1: West command (recommended, simplest)
west tl-build samples/gpio_demo --board TLSR9528A_EVK

# Method 2: Make command (compatible with traditional conventions)
make build APP=samples/gpio_demo BOARD=TLSR9528A_EVK

# Method 3: Direct CMake invocation (most flexible)
cmake -B build -G Ninja -S samples/gpio_demo -DBOARD=TLSR9528A_EVK
cmake --build build
```

## Documentation Navigation

| Section | Description | Status |
|---------|-------------|--------|
| [CMake Build System](cmake_system.md) | CMake core flow, module loading, configuration phase details | STABLE |
| [Kconfig Configuration System](kconfig_system.md) | Configuration hierarchy, processing flow, key scripts | STABLE |
| [West Commands](west_commands.md) | tl-build / tl-config / tl-bdt and other command details | STABLE |
| [Make Support](make_support.md) | Makefile frontend interface, targets and variable descriptions | STABLE |
| [Build Flow](build_flow.md) | Environment validation, config generation, compile & link full flow | STABLE |
| [Extensions & Customization](extensions.md) | Add new modules, extend West commands, Kconfig customization | STABLE |
| [File & Script Reference](reference.md) | Config files, CMake modules, script inventory | STABLE |

## Build System Architecture

```{mermaid}
graph TD
    A["West / Make / CMake"] --> B["CMakeLists.txt<br/>(entry point)"]
    B -->|find_package Telink| C["TelinkConfig.cmake"]
    C --> D["telink_default.cmake<br/>(module loading)"]
    D --> E1["python"]
    D --> E2["extensions"]
    D --> E3["west"]
    D --> E4["compiler"]
    D --> E5["kconfig"]
    D --> E6["pinmux"]
    D --> E7["linker"]
    D -.->|"Includes"| E1 & E2 & E3 & E4 & E5 & E6 & E7
    E5 --> F["Kconfig<br/>(config)"]
    F --> G1["chip.config"]
    F --> G2["build.config"]
    F --> G3[".config"]
    G1 & G2 --> G3
    G3 --> H["Ninja<br/>(compile)"]
    H --> I["Firmware .bin"]
```
