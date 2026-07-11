---
title: BDT Burning and Debugging Tool
status: STABLE
---

# BDT Burning and Debugging Tool

BDT (Burning and Debugging Tool) is the flashing and debugging tool for Telink chips, providing a unified cross-platform interface via the `west tl-bdt` command.

## Supported Operations

| Operation | Description |
|------|------|
| `download` | Download firmware to Flash |
| `read` | Read data from Flash |
| `write` | Write data to Flash |
| `erase` | Erase Flash |
| `lock` | Lock Flash region |
| `unlock` | Unlock Flash region |
| `reset` | Reset device |

## Quick Start

```bash
# Download firmware (default from build/ directory)
west tl-bdt download --chip TLSR9528A

# Specify firmware file
west tl-bdt download --chip TLSR9528A -i build/gpio_demo.bin

# Specify flash address
west tl-bdt download --chip TLSR9528A -i build/gpio_demo.bin -a 0x1000

# Use USB mode
west tl-bdt download --chip TLSR9528A --usb -i build/gpio_demo.bin
```

## Flash Operations

### Read Flash

```bash
# Read 16 bytes from address 0x00
west tl-bdt read --chip TLSR9528A -a 0x00 -s 16

# Read 1KB to a file
west tl-bdt read --chip TLSR9528A -a 0x00 -s 1k -o flash_dump.bin
```

### Write Flash

```bash
# Write raw data
west tl-bdt write --chip TLSR9528A -a 0x1000 -s 4 01 02 03 04

# Write from a file
west tl-bdt write --chip TLSR9528A -a 0x1000 -i data.bin

# Erase then write
west tl-bdt write --chip TLSR9528A -a 0x1000 -i data.bin -e
```

### Erase Flash

```bash
# Erase 4KB
west tl-bdt erase --chip TLSR9528A -a 0x00 -s 4k
```

### Flash Lock Operations

```bash
# Lock 512KB
west tl-bdt lock --chip TLSR9528A -a 0x00 -s 512k

# Unlock
west tl-bdt unlock --chip TLSR9528A
```

### Reset

```bash
# Reset device
west tl-bdt reset --chip TLSR9528A

# Reset from Core
west tl-bdt reset --chip TLSR9528A -c
```

## BDT Path Configuration

Priority from high to low:

1. Command line: `--bdt-path /path/to/bdt`
2. Environment variable: `export BDT_PATH=/path/to/BDT`
3. System PATH
4. SDK directory: `${TELINK_BASE}/tools/`

```bash
# Method 1: Specify via command line
west tl-bdt download --bdt-path /path/to/BDT --chip TLSR9528A -i build/firmware.bin

# Method 2: Environment variable
export BDT_PATH=/path/to/BDT  # Linux/macOS
set BDT_PATH=C:\BDT           # Windows CMD
$env:BDT_PATH="C:\BDT"        # Windows PowerShell
```

## Cross-Platform Notes

| Platform | Executable | Notes |
|------|-----------|---------|
| **Windows** | `Cmd_download_tool.exe` | Automatically handles path separator conversion |
| **Linux** | `bdt` | Standard Linux command |

## FAQ

### BDT Tool Not Found

```
Error: BDT tool not found. Please set BDT_PATH or use --bdt-path.
```

**Solution**: Configure the BDT path using the methods described above.

### Chip Type Not Specified

```
Error: Chip type not specified. Please use --chip option.
```

**Solution**: Use the `--chip` argument to specify the chip, or ensure the build configuration includes chip information.

### BDT Command Failed

Check common causes:
- Incorrect chip type
- Invalid address or size
- Device not connected
