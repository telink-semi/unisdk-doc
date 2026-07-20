---
title: Windows Environment Setup
status: STABLE
---

# Windows Environment Setup

This document details the complete steps to set up the UniSDK development environment on Windows 10/11.

## System Requirements

- Windows 10 (1709+) or Windows 11
- At least 4 GB RAM, 8 GB+ recommended
- Administrator privileges (recommended)

## Installation Methods

### Method 1: One-Click Setup Script (Recommended)

UniSDK provides an automated deployment script (`windows_setup.ps1`) that simplifies the environment configuration process on Windows systems.

1. Open PowerShell as Administrator
2. Navigate to the scripts directory and run:

```powershell
cd <path_to_unisdk_repository>\scripts
.\windows_setup.ps1
```

#### Script Features in Detail

The script automatically performs the following tasks:

1. **PowerShell Execution Policy Configuration**
   - Checks and sets the execution policy to `RemoteSigned` to allow running local scripts

2. **Tool Installation**
   - Detects if `winget` is installed
   - If winget is available: automatically downloads and installs CMake, Ninja, Python, and Git
   - If winget is not available: provides official download links to guide manual installation

3. **Python Environment Configuration**
   - Creates `.venv` virtual environment in the UniSDK root directory
   - Upgrades pip to the latest version
   - Installs all Python dependencies from `requirements.txt`
   - Ensures west tool is properly installed

4. **Environment Variable Settings**
   - Sets `TELINK_TOOLCHAIN_PATH` pointing to the toolchain directory
   - Adds CMake and Ninja paths to the system PATH

5. **Telink Toolchain Setup**
   - Creates the `toolchain` directory
   - Sets `TELINK_TOOLCHAIN_PATH` environment variable
   - Due to special permissions required for toolchain download, users need to manually download and extract the toolchain

6. **West Workspace Initialization**
   - Initializes the west workspace by executing `west init -l`

#### Logging

The script automatically generates a `setup_log.txt` file in the script directory, recording detailed logs of the entire configuration process for troubleshooting purposes.

!!! note "Toolchain Requires Manual Download"
    Since toolchain download requires special permissions, the script only creates the `toolchain` directory and sets the environment variable.
    Please manually download the toolchain and extract it to the `<unisdk>\toolchain` directory.
    Download link: https://drive.weixin.qq.com/s?k=AKwA0AfNAA8Ox1r0ab

### Method 2: Manual Installation

#### 1. Install System Dependencies

Use winget for one-click installation:

```powershell
winget install Kitware.CMake Ninja-build.Ninja Python Git.Git
```

Or manually download and install if winget is not supported:

- [CMake](https://cmake.org/download/) — Check "Add CMake to PATH"
- [Ninja](https://github.com/ninja-build/ninja/releases) — Manually add to PATH
- [Python](https://www.python.org/downloads/) — Check "Add Python.exe to PATH"
- [Git](https://git-scm.com/downloads)

Verify installation:

```powershell
cmake --version
python --version
git --version
ninja --version
```

#### 2. Set Up Python Virtual Environment

```powershell
# Enter the UniSDK directory
cd <path_to_unisdk>

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate.ps1

# If you encounter a script execution permission error, run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

#### 3. Initialize West

```powershell
west init -l
```

If you encounter the error `already initialized in {where}, aborting.`, temporarily unset `ZEPHYR_BASE`:

```powershell
Remove-Item Env:ZEPHYR_BASE; west init -l
```

#### 4. Configure Toolchain

```powershell
# PowerShell
$env:TELINK_TOOLCHAIN_PATH="path\to\toolchain"

# or CMD
set TELINK_TOOLCHAIN_PATH=path\to\toolchain
```

## Configure BDT Tool (Optional)

```powershell
# Set BDT path
$env:BDT_PATH="C:\BDT"

# Or specify temporarily at runtime
west tl-bdt download --chip TLSR9528A --bdt-path C:\BDT -i build\firmware.bin
```

## Verify Environment

```powershell
# Test build
west tl-build samples\gpio_demo
```

## Common Issues

### PowerShell Script Cannot Execute

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

### Environment Variables Not Taking Effect

- Restart the terminal, VS Code, or the system
- Check system environment variable settings
- If the previous step doesn't solve the problem, manually check if the PATH contains the correct path and add it to the user's PATH

### Arrow Keys Not Working in menuconfig Within VS Code

- Use letter keys instead of arrow keys
- Use Windows 11
- Use CMD instead of PowerShell for menuconfig operations

### winget Installation Failure

- Check Windows version (requires Windows 10 1709 or higher)
- Try installing App Installer from Microsoft Store

### Python Dependencies Installation Failure

- Ensure network connection is working
- Proxy server settings might be needed

### CMake or Ninja Not Found

- Manually check installation paths
- The script will attempt to automatically find common installation locations, but may require manual addition to PATH

## Notes

1. **Administrator Privileges**: While not strictly necessary, it's recommended to run the script as administrator to ensure proper environment variable settings
2. **Environment Variables Effectiveness**: After script completion, open a new PowerShell window to apply all environment variable changes
3. **Virtual Environment Activation**: Use the following command to activate the virtual environment:
   ```powershell
   <path_to_unisdk>\.venv\Scripts\Activate.ps1
   ```

## Next Steps

- [First Example: Blinky](blinky.md)
- [Linux Environment Setup](setup_linux.md)
- [Getting Started](../getting_started/index.md)
