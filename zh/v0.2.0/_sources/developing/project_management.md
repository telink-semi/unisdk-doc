---
title: Project Creation & Management
status: STABLE
---

# Project Creation & Management

## Application Project Location

UniSDK application projects **can be located in any directory**, not limited to the `samples/` directory. Each application project needs to provide its own `CMakeLists.txt` and source code.

## Creating a New Project

### Minimum Project Structure

:::{dropdown} Minimum Project Structure
:summary: Click to expand/collapse

```text
my_project/
├── CMakeLists.txt    # Build entry point
├── main.c            # Main program
└── Kconfig           # Optional: project-level Kconfig configuration
```
:::

### CMakeLists.txt Template

```cmake
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

# Load Telink SDK
find_package(Telink REQUIRED HINTS $ENV{TELINK_BASE})

# Define project
project(MyProject LANGUAGES C CXX)

# Add C source files
file(GLOB C_SOURCES "*.c")
target_sources(Telink PRIVATE ${C_SOURCES})

# Optional: conditionally add C++ source files
if(CONFIG_TLK_ALLOW_CPP_WRAPPERS)
    file(GLOB CPP_SOURCES "*.cpp")
    target_sources(Telink PRIVATE ${CPP_SOURCES})
endif()
```

### Key Notes

1. **`find_package(Telink)`** — Locates the SDK path via the `TELINK_BASE` environment variable
2. **`project()`** — The project name will be used as the output firmware name
3. **`target_sources(Telink ...)`** — Application source files are added to the SDK's main target `Telink`
4. **`CONFIG_TLK_ALLOW_CPP_WRAPPERS`** — Checks whether C++ wrappers are enabled

## Building the Project

### West Command (Recommended)

```bash
# Run in the project directory (must be within a west workspace when using west)
west tl-build . --board TLSR9528A_EVK

# Specify build directory
west tl-build -d build_custom . --board TLSR9528A_EVK
```

### CMake Command

```bash
# Configure
cmake -B build -G Ninja -S . -DBOARD=TLSR9528A_EVK

# Build
cmake --build build
```

### Make Command

```bash
make cmake build APP=. BOARD=TLSR9528A_EVK
```

## Configuration Management

### Using Project Kconfig

Create a `Kconfig` file in the project directory to define project-specific configuration options:

```kconfig
menu "My Project Configuration"

config MY_FEATURE_ENABLED
    bool "Enable my feature"
    default y
    help
        Enable custom project feature.

endmenu
```

The `Kconfig` file is automatically integrated into the build system via `KCONFIG_APPLICATION_DIR` in `kconfig.cmake`.

### Interactive Configuration

```bash
west tl-config .
```

## Cleaning

```bash
# Clean build artifacts
west tl-build . --clean

# Or manually delete
rm -rf build/
```

## Development Workflow Recommendations

1. **Start from a sample** — Copy the most similar `samples/` example as a starting point
2. **Kconfig isolation** — Place project-specific configuration in the project-level `Kconfig`
3. **Version management** — Manage application projects and the SDK separately, linking them via `TELINK_BASE`
