---
title: Getting Started
status: STABLE
---

# Getting Started

This chapter helps new developers set up the UniSDK development environment in 5–10 minutes and compile and run their first example program.

## Prerequisites

Before starting, make sure you have the following ready:

- **Hardware**: At least one Telink official development board (e.g., TLSR9528A_EVK)
- **Operating System**: Linux (Ubuntu 20.04+) / Windows 10+ / macOS 12+
- **Network**: Access to GitHub and PyPI

## Quick Steps

### Step 1: Install System Dependencies

=== "Linux (Ubuntu)"

    ```bash
    sudo apt install --no-install-recommends git cmake ninja-build \
        python3-dev python3-venv python3-tk make
    ```

=== "Windows"

    ```powershell
    # One-click install using winget
    winget install Kitware.CMake Ninja-build.Ninja Python Git.Git
    ```

=== "macOS"

    ```bash
    brew install cmake ninja python3 python-tk
    ```

### Step 2: Create Python Virtual Environment

```bash
# Enter the UniSDK repository root directory
cd unisdk

# Create virtual environment
python3 -m venv .venv    # Linux/macOS
python -m venv .venv     # Windows

# Activate virtual environment
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\activate.ps1      # Windows PowerShell

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Initialize West Workspace

```bash
west init -l
```

!!! tip "Encountering `already initialized` error?"
    If the `ZEPHYR_BASE` environment variable points to another Zephyr workspace, temporarily unset it:
    ```bash
    unset ZEPHYR_BASE && west init -l    # Linux/macOS
    ```

### Step 4: Configure Toolchain

1. Download the Telink RISC-V toolchain (contact Telink for the download link)
2. Extract to a local directory
3. Set the environment variable:

```bash
export TELINK_TOOLCHAIN_PATH=/path/to/toolchain   # Linux/macOS
set TELINK_TOOLCHAIN_PATH=path\to\toolchain        # Windows CMD
$env:TELINK_TOOLCHAIN_PATH="path\to\toolchain"     # Windows PowerShell
```

### Step 5: Build the First Example

```bash
# Method 1: West command (recommended)
west tl-build samples/gpio_demo

# Method 2: Make command
make build APP=samples/gpio_demo
```

### Step 6: Flash and Run

```bash
# Flash using BDT tool
west tl-bdt download --chip TLSR9528A -i build/gpio_demo.bin
```

---

## Detailed Guides

- [Linux Environment Setup](setup_linux.md)
- [Windows Environment Setup](setup_windows.md)
- [macOS Environment Setup](setup_macos.md)
- [First Example: Blinky](blinky.md) — Detailed step-by-step instructions
- [Troubleshooting](troubleshooting.md)

## Next Steps

- [Development Guide](../developing/index.md) — Deep dive into the SDK development workflow
- [Build & Configuration](../build_config/index.md) — Learn the build system in detail
- [Samples & Demos](../samples/index.md) — Explore more examples
