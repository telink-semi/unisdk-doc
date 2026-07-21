---
title: Build Flow
status: STABLE
---

# Build Flow

## Overview

This document details the complete build process flow from configuration to firmware generation.

## Complete Build Flow

```{mermaid}
graph TD
    A[Start Build] --> B{Environment Validation}
    B -->|Success| C[CMake Configuration]
    B -->|Failure| Z[Build Failed]

    subgraph Modules["Module Loading"]
        D[Load CMake Modules]
    end

    subgraph Config["Configuration Generation"]
        E[Generate chip.config]
        F[Generate capabilities.h]
        G[Generate build.config]
        H[Merge into .config]
        I[Generate autoconf.h]
        J[Generate pinmux.h]
    end

    subgraph Build["Compilation"]
        K[Source File Compilation]
        L[Linking]
        M[Generate Firmware .bin]
    end

    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N[Build Complete]
    Z --> N
```

## Getting Started Guide

### Install Dependencies

You'll install some host dependencies using your package manager.

#### Ubuntu

Use apt to install the required dependencies:

```bash
sudo apt install --no-install-recommends git cmake ninja-build python3-dev python3-venv python3-tk make
```

Verify the versions:

```bash
cmake --version
python3 --version
git --version
ninja --version
```

If "command not found" is displayed, the corresponding tool is not installed.

#### MacOS

Use Homebrew to install the required dependencies:

```bash
brew install cmake ninja python3 python-tk
```

Verify the versions:

```bash
cmake --version
python3 --version
git --version
ninja --version
```

#### Windows

You can install using the following two methods:

1. For systems that support winget:

```bash
winget install Kitware.CMake Ninja-build.Ninja Python Git.Git
```

2. For systems that don't support winget, download and install from official websites:
   - [CMake](https://cmake.org/download/) (check "Add CMake to the PATH")
   - [Ninja](https://github.com/ninja-build/ninja/releases) (manually add to PATH)
   - [Python](https://www.python.org/downloads/) (check "Add Python.exe to PATH")
   - [Git](https://git-scm.com/downloads)

After installation, verify:

```bash
cmake --version
python --version
git --version
ninja --version
```

### Install Python Dependencies

#### Python Virtual Environment

```bash
# Create virtual environment
python -m venv .venv          # Windows
python3 -m venv .venv         # Linux/MacOS
```

```bash
# Activate virtual environment
source .venv/bin/activate           # Linux/Mac
.venv\Scripts\activate.bat          # Windows Batchfile
.venv\Scripts\activate.ps1          # Windows PowerShell
```

When using PowerShell, you might encounter:

```
Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

Resolve by:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then install Python dependencies:

```bash
pip install -r requirements.txt
```

#### West Tool Setup

```bash
# Verify west installation
west --version

# Initialize west workspace
west init -l
```

**Potential Issue with west init -l:**

If you encounter the error `already initialized in {where}, aborting.`, this is likely due to the `ZEPHYR_BASE` environment variable being set to a Zephyr workspace with an existing `.west` directory.

**Solution:** Temporarily unset `ZEPHYR_BASE`:

- **Windows (PowerShell):**
  ```powershell
  Remove-Item Env:ZEPHYR_BASE; west init -l
  ```

- **Linux/macOS:**
  ```bash
  unset ZEPHYR_BASE; west init -l
  ```

#### Toolchain Configuration

Download and extract the toolchain (only available for Telink):
[Toolchain_V5.4.1](https://drive.weixin.qq.com/s?k=AKwA0AfNAA8Ox1r0ab)

Set the `TELINK_TOOLCHAIN_PATH` environment variable and ensure toolchain binaries are accessible in PATH.

## Six Phases

### 1. Environment Validation

- Verify that the Python virtual environment is activated
- Verify that West is available and version >= 0.14.0
- Verify that `TELINK_TOOLCHAIN_PATH` is set
- Verify that the toolchain executables are accessible

### 2. CMake Configuration

```bash
cmake -B build -G Ninja -S samples/gpio_demo
```

Load and execute all CMake modules (python -> extensions -> west -> compiler -> kconfig -> pinmux -> linker).

### 3. Configuration Generation (Config Target)

```bash
cmake --build build --target config
```

Executed in order:
1. Clean old config -> 2. Generate `chip.config` -> 3. Generate `capabilities.h` -> 4. Generate `build.config` -> 5. Merge `.config` -> 6. Generate pinmux configuration

### 4. Source File Compilation

Ninja compiles all source files concurrently according to `build.ninja` rules.

### 5. Linking

Link object files into an ELF executable, outputting `.elf`, `.bin`, `.map`.

### 6. Firmware Generation

- Use `objcopy` to convert ELF to binary `.bin` file
- Use `objdump` to generate disassembly for debugging
- Run `tl_check_fw.sh` to verify firmware

## Configuration Commands

### Basic Configuration

```bash
west tl-config
```

This command configures the application in the current directory using default settings.

**Process:**
1. Sets up environment variables (TELINK_BASE)
2. Creates build directory if needed
3. Runs initial CMake configuration if required
4. Executes the unified `config` target which:
   - Generates `chip.config` from `Kconfig.chip`
   - Generates `capabilities.h` from chip configuration
   - Generates `build.config` from `Kconfig.build`
   - Merges configurations into final `.config`
   - Generates pinmux configuration files

### Common Configuration Examples

```bash
# Specify build directory
west tl-config -d build_custom

# Using different source directory
west tl-config path/to/application -d build_custom

# Configure and build in one command
west tl-build -k
```

## Basic Build Commands

```bash
# Simple build (current directory)
west tl-build
```

This command builds the application in the current directory. If it's the first build, it will automatically configure and build.

**Pre-build Checks:**
- Checks for existing `.config`, `build.config`, `chip.config`, `pinmux.h`, and `capabilities.h` files
- Invokes CMake to generate the build system
- Compiles source code using the selected toolchain
- Generates firmware binaries in the `build/` directory

### Common Build Command Examples

```bash
# Specify build directory
west tl-build -d build_tl3218

# Specify source directory
west tl-build path/to/application

# Run CMake after configuration
west tl-build -c

# Clean build directory and rebuild
west tl-build --clean

# Pristine build
west tl-build --pristine=always
```

## Configuration File Generation Logic

### File Hierarchy

Configuration files are loaded in order of increasing priority:

1. **chip.config** -- Chip default configuration (lowest priority)
2. **build.config** -- User-defined build options
3. **.config** -- Final merged configuration (highest priority)

### Configuration Generation Flow

When executing `west tl-config`, the flow is:

1. **Parameter Processing Phase**: Parses source directory and build directory options
2. **CMake Configuration Phase**: Checks for existing `CMakeCache.txt`, runs CMake configuration with Ninja generator
3. **Configuration Target Execution**: Executes `cmake --build <build_dir> --target config`

When executing `west tl-build` (with `-k/--kconfig`), the flow is:

1. **Parameter Processing**: Checks for `--board` or `--soc` parameters
2. **Default Configuration Generation**: Runs `scripts/kconfig.py` to generate `chip.config` and `build.config`, merges into `.config`
3. **CMake Configuration**: Passes `BOARD` and `SOC` parameters to CMake

### Dependencies

- `.config` depends on `chip.config` and `build.config` (when automatically generated)
- The CMake build system depends on `.config` to determine compilation options
- CMake monitors changes to `.config` and reconfigures the project when the file is modified

## Build Results

:::{dropdown} Build Results
:summary: Click to expand/collapse

```text
build/
├── gpio_demo.bin         # Firmware binary (for flashing)
├── gpio_demo.elf         # ELF executable (for debugging)
├── gpio_demo.map         # Memory map file
└── gpio_demo.lst         # Disassembly file
```
:::

## Building Without West

This section explains how to build without using the west tool.

### CMake Configuration

```bash
cmake -B path/to/build -G Ninja -DTelink_DIR='path/to/telink-package' -S path/to/source
```

Parameters:
- **`-B path/to/build`**: Specifies the build directory
- **`-G Ninja`**: Specifies Ninja as the generator
- **`-DTelink_DIR='path/to/telink-package'`**: Points to the TelinkConfig.cmake file (not needed if `TELINK_BASE` is set)
- **`-S path/to/source`**: Specifies the source code directory

### CMake Build

```bash
# Build the project
cmake --build path/to/build

# Or use Ninja directly
ninja -C path/to/build

# Clean the build directory
cmake --build path/to/build --target clean
```

## Troubleshooting

### Environment Issues

**Problem: TELINK_TOOLCHAIN_PATH not found**

```bash
# Windows
set TELINK_TOOLCHAIN_PATH=path/to/toolchain           # CMD
$env:TELINK_TOOLCHAIN_PATH=path/to/toolchain           # PowerShell

# Linux/macOS
export TELINK_TOOLCHAIN_PATH=path/to/toolchain
```

**Problem: CMake configuration fails**

- Ensure all dependencies are installed
- Check CMake version compatibility
- Clear old build cache with `--clean`

### Build Issues

**Problem: Compilation errors**

- Check application code for syntax errors
- Ensure correct board and chip configurations are used
- Try a clean build with `--pristine=always`

### menuconfig Issues

**Problem: Arrow icons not working in VSCode PowerShell**

- Roll back to an earlier VSCode version or use the test ConPty library
- Use Windows 11
- Use letter keys instead of arrow icons
- Use Command Prompt instead of PowerShell

### Environment Variable Issues

**Problem: Environment variables not taking effect**

- Restart the terminal, VS Code, or the system
- Manually check if PATH contains the correct path and add to user PATH

### Other Issues

1. Ensure you're using the latest version of UniSDK
2. Clear the build directory and rebuild:
   ```bash
   west tl-build --clean
   ```
3. Check system logs for more detailed error information
