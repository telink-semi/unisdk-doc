---
title: CMake Build System
status: STABLE
---

# CMake Build System

CMake is the core of the UniSDK build system, responsible for project configuration, dependency resolution, and build rule generation.

## Entry Point Modes

UniSDK supports two CMake entry point modes:

| Mode | Entry | Purpose | Command Example |
|------|-------|---------|-----------------|
| **Root entry** | `CMakeLists.txt` (repo root) | SDK development/testing | `cmake -B build -G Ninja .` |
| **Application entry** | App's `CMakeLists.txt` | Build specific application | `cmake -B build -G Ninja samples/gpio_demo` |

### Application-Level CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.20.0)
find_package(Telink REQUIRED HINTS $ENV{TELINK_BASE})
project(GPIO_Demo LANGUAGES C CXX)

file(GLOB C_SOURCES "*.c")
target_sources(Telink PRIVATE ${C_SOURCES})

if(CONFIG_TLK_ALLOW_CPP_WRAPPERS)
    file(GLOB CPP_SOURCES "*.cpp")
    target_sources(Telink PRIVATE ${CPP_SOURCES})
endif()
```

## Module Loading Order

`telink_default.cmake` loads CMake modules in the following order:

1. **`python.cmake`** — Python environment detection (Python 3.10+)
2. **`extensions.cmake`** — CMake extension functions (conditional variables, JSON processing)
3. **`version.cmake`** — Version information processing
4. **`west.cmake`** — West tool integration (version >= 0.14.0)
5. **`compiler.cmake`** — RISC-V compiler configuration
6. **`kconfig.cmake`** — Kconfig configuration integration
7. **`pinmux.cmake`** — Pin multiplexing configuration generation
8. **`linker.cmake`** — Linker script processing

## Core Module Details

### compiler.cmake

- Detects the `TELINK_TOOLCHAIN_PATH` environment variable
- Configures the RISC-V GCC cross-compilation toolchain
- Provides the `telink_apply_compiler_options()` function
- Dynamically loads compilation options from `build_settings.json`

### linker.cmake

- Sets the RISC-V link command template
- Reads linker options from `build_settings.json`
- Preprocesses linker scripts (`flash_boot.link` → `flash_boot.ld`)
- Post-processing: generates `.bin` + `.map` + firmware verification

### kconfig.cmake

- Manages the generation flow of `chip.config` → `build.config` → `.config`
- Generates `capabilities.h` and `autoconf.h`
- Defines CMake targets such as `config` / `parse_config`
- SOC/BOARD parameter processing and combination validation

### pinmux.cmake

- Generates `.pinmux` and `pinmux.h`
- Depends on the `.config` file
- Build directory is automatically added to the include path

### extensions.cmake

```cmake
# Conditional variable setting
set_ifndef(variable value [PARENT_SCOPE])

# Conditional source file addition
add_sources_ifdef(config src)

# JSON array to CMake list
json_to_list(JSON_ARRAY_STRING OUTPUT_LIST)
```

## Configuration Flow

```{mermaid}
graph TD
    A[CMakeLists.txt] --> B[find_package Telink]
    B --> C[TelinkConfig.cmake]
    C --> D[telink_default.cmake]
    D --> E[Load CMake modules]
    E --> F[Kconfig generates config]
    F --> G[Generate .config]
    G --> H[Generate autoconf.h]
    H --> I[Generate pinmux.h]
    I --> J[Compiler/Linker configuration]
    J --> K[Build preparation complete]
```

## Include Guard Mechanism

| Guard | Set Location | Purpose |
|-------|-------------|---------|
| `TELINK_ROOT_INCLUDED` | Root `CMakeLists.txt` | Prevent duplicate root inclusion |
| `TELINK_PACKAGE_INCLUDED` | `TelinkConfig.cmake` | Prevent duplicate package loading |

## Build Directory Structure

:::{dropdown} Build Directory Structure
:summary: Click to expand/collapse

```text
build/
├── .config              # Merged final configuration
├── chip.config          # Chip configuration
├── build.config         # Build configuration
├── autoconf.h           # C configuration macros
├── capabilities.h       # Chip capability declarations
├── pinmux.h             # Pin multiplexing configuration
├── flash_boot.ld        # Linker script
├── build.ninja          # Ninja build file
├── CMakeCache.txt       # CMake cache
└── Kconfig/             # Chip-specific Kconfig fragments
```
:::
