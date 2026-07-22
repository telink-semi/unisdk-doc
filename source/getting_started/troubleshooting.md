---
title: Troubleshooting
status: STABLE
---

# Troubleshooting

## Environment Issues

### TELINK_TOOLCHAIN_PATH Not Found

**Error**: `Error: TELINK_TOOLCHAIN_PATH environment variable not set`

**Solution**:

```bash
# Linux/macOS
export TELINK_TOOLCHAIN_PATH=/path/to/toolchain

# Windows CMD
set TELINK_TOOLCHAIN_PATH=path\to\toolchain

# Windows PowerShell
$env:TELINK_TOOLCHAIN_PATH="path\to\toolchain"
```

### west init -l Reports "already initialized"

**Cause**: The `ZEPHYR_BASE` environment variable points to a Zephyr workspace containing a `.west` directory.

**Solution**:

```bash
# Linux/macOS
unset ZEPHYR_BASE && west init -l

# Windows PowerShell
Remove-Item Env:ZEPHYR_BASE; west init -l
```

### CMake Configuration Failed

**Solution**:

1. Verify the CMake version (requires >= 3.20.0).
2. Clear old build cache and retry:
   ```bash
   west tl-build --clean
   ```
3. Verify that all required dependencies are installed correctly.

### Python Dependency Installation Failed

**Solution**:

- Check your network connection.
- Verify that the virtual environment is activated (the terminal prompt should have a `(.venv)` prefix).
- If required, configure a proxy:
  ```bash
  pip install --proxy http://proxy:port -r requirements.txt
  ```

## Build Issues

### Compilation Error

**Solution**:

1. Check the source code for syntax errors.
2. Verify that the chip and board are configured correctly.
3. Perform a full clean and retry:
   ```bash
   west tl-build --pristine always
   ```

### Cannot Find pinmux.h

**Solution**:

```bash
# Manually generate pinmux configuration
make pinmux
# or
python -m scripts.pinmux
```

## Menuconfig Issues

### Arrow Keys Not Working in menuconfig Within VS Code (Windows)

**Solution**:

- Use the letter keys instead of the arrow keys.
- Use Windows 11.
- Use Command Prompt (CMD) instead of PowerShell for menuconfig operations.

## Getting Help

- [Technical Support](../support/index.md)
- [Submit an Issue](../contribute/index.md)
