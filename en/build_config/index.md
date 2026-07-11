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

```
  West / Make / CMake
        │
        ▼
  ┌─────────────┐
  │ CMakeLists.txt │ (entry point)
  └──────┬──────┘
         │ find_package(Telink)
         ▼
  ┌──────────────────┐
  │ TelinkConfig.cmake │
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────────┐
  │ telink_default.cmake  │──► python, extensions, version
  │ (module loading)      │──► west, compiler, kconfig
  └──────────────────────┘──► pinmux, linker
         │
         ▼
  ┌──────────┐    ┌──────────────┐
  │ Kconfig  │───►│ chip.config   │
  │ (config) │───►│ build.config  │
  └──────────┘───►│ → .config     │
                  └──────────────┘
         │
         ▼
  ┌──────────┐
  │ Ninja    │ (compile)
  └──────────┘
         │
         ▼
  ┌──────────────┐
  │ Firmware .bin │
  └──────────────┘
```
