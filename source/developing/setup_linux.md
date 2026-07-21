---
title: Linux Environment Setup
status: STABLE
---

# Linux Environment Setup

This document details the complete steps to set up the UniSDK development environment on a Linux system (using Ubuntu as an example).

## System Requirements

- Ubuntu 20.04 LTS or higher
- At least 4 GB RAM, 8 GB+ recommended
- Sufficient disk space (SDK + toolchain requires approximately 2 GB)

## Install System Dependencies

```bash
sudo apt update
sudo apt install --no-install-recommends git cmake ninja-build \
    python3-dev python3-venv python3-tk make
```

Verify installation:

```bash
cmake --version     # Should be >= 3.20.0
python3 --version   # Should be >= 3.10
git --version
ninja --version
```

## Set Up Python Virtual Environment

```bash
# Enter the UniSDK directory
cd /path/to/unisdk

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

!!! tip "Recommendation"
    Remember to activate the virtual environment before each development session:
    ```bash
    source .venv/bin/activate
    ```

## Initialize West

```bash
# Verify west installation
west --version

# Initialize workspace
west init -l
```

!!! warning "Common Issue: already initialized"
    If you encounter the `already initialized in {path}, aborting.` error:
    ```bash
    unset ZEPHYR_BASE
    west init -l
    ```

## Configure Toolchain

1. Download the Telink RISC-V toolchain (contact the Telink team for access)
2. Extract the toolchain to a designated directory:
   ```bash
   mkdir -p ~/telink/toolchain
   tar -xzf telink_toolchain_*.tar.gz -C ~/telink/toolchain
   ```
3. Set the environment variable (recommend adding to `~/.bashrc` or `~/.zshrc`):
   ```bash
   export TELINK_TOOLCHAIN_PATH=$HOME/telink/toolchain
   ```

## Configure BDT Tool (Optional)

If you need to use the `west tl-bdt` command for flashing and debugging:

```bash
# Set BDT tool path
export BDT_PATH=/path/to/BDT

# Or specify temporarily at runtime
west tl-bdt download --chip TLSR9528A --bdt-path /path/to/BDT -i build/firmware.bin
```

## Verify Environment

```bash
# Test building an example
west tl-build samples/gpio_demo

# If the build succeeds, you will see output similar to:
# [100%] Built target Telink
```

## Next Steps

- [First Example: Blinky](blinky.md)
- [Getting Started](../getting_started/index.md)
