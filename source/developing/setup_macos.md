---
title: macOS Environment Setup
status: STABLE
---

# macOS Environment Setup

This document details the complete steps to set up the UniSDK development environment on macOS.

## System Requirements

- macOS 12 (Monterey) or higher
- Apple Silicon (M1/M2/M3) or Intel processor
- At least 4 GB RAM

## Install System Dependencies

We recommend using the [Homebrew](https://brew.sh) package manager:

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install UniSDK dependencies
brew install cmake ninja python3 python-tk git
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

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Initialize West

```bash
west --version
west init -l
```

## Configure Toolchain

Since UniSDK uses the RISC-V cross-compilation toolchain, you need to obtain the corresponding macOS version of the toolchain from Telink.

1. Contact Telink to obtain the macOS toolchain
2. Extract to a designated directory:
   ```bash
   mkdir -p ~/telink/toolchain
   tar -xzf telink_toolchain_macos_*.tar.gz -C ~/telink/toolchain
   ```
3. Set the environment variable:
   ```bash
   export TELINK_TOOLCHAIN_PATH=$HOME/telink/toolchain
   ```
   It is recommended to add the above command to `~/.zshrc` (the default shell on macOS).

## Verify Environment

```bash
# Test build
west tl-build samples/gpio_demo
```

## Next Steps

- [First Example: Blinky](blinky.md)
- [Linux Environment Setup](setup_linux.md)
- [Getting Started](../getting_started/index.md)
