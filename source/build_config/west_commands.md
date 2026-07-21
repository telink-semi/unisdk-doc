---
title: West Commands
status: STABLE
---

# West Commands

West is the unified command-line entry point for UniSDK. UniSDK registers multiple custom command extensions through `scripts/west-commands.yml`.

## Command Registration

```yaml
west-commands:
  - file: scripts/west_commands/build.py
    commands:
      - name: tl-build
        class: Build
        help: compile a Telink application
  - file: scripts/west_commands/boards.py
    commands:
      - name: tl-boards
        class: Boards
        help: display information about supported Telink boards
  - file: scripts/west_commands/socs.py
    commands:
      - name: tl-socs
        class: Socs
        help: display information about supported Telink socs
  - file: scripts/west_commands/config.py
    commands:
      - name: tl-config
        class: Config
        help: configure a Telink application
  - file: scripts/west_commands/bdt.py
    commands:
      - name: tl-bdt
        class: Bdt
        help: use BDT tool to configure and flash a Telink chip
```

## `west tl-build` — Build

Build a Telink application. The build directory defaults to `build/` in the current working directory.

```bash
# Basic usage
west tl-build [source_dir] [-d build_dir] [options]

# Specify source directory
west tl-build samples/gpio_demo

# Specify build directory
west tl-build -d build_tl3218

# Specify SOC during build
west tl-build --soc TLSR9528A

# Specify BOARD during build
west tl-build --board TLSR9528A_EVK

# Build after interactive configuration
west tl-build --kconfig

# Clean build
west tl-build --clean
west tl-build --pristine always

# Build and flash
west tl-build --flash

# Build specific target
west tl-build -t flash

# CMake configuration only, no compilation
west tl-build --cmake-only

# Pass additional CMake options
west tl-build -- -DCONFIG_DEBUG=y
```

### Execution Flow

1. Check the `TELINK_TOOLCHAIN_PATH` environment variable
2. Validate the SOC/BOARD combination
3. Set source and build directories
4. Run Kconfig configuration if needed
5. Invoke CMake to generate the build system
6. Execute compilation and linking
7. Output build results

## `west tl-config` — Configuration

Independently configure a Telink application.

```bash
# Basic usage
west tl-config [source_dir] [-d build_dir]

# CMake-only configuration (skip interactive GUI)
west tl-config -c

# List available SOCs
west tl-config --list-socs

# List available boards
west tl-config --list-boards

# Validate SOC/BOARD combination
west tl-config --validate TLSR9528A TLSR9528A_EVK
```

## `west tl-bdt` — Burning & Debugging

BDT (Burning and Debugging Tool) command interface.

### Subcommands

| Subcommand | Description |
|------------|-------------|
| `download` | Download firmware to Flash |
| `read` | Read Flash data |
| `write` | Write Flash data |
| `erase` | Erase Flash |
| `lock` | Lock Flash region |
| `unlock` | Unlock Flash |
| `reset` | Reset device |

### Common Examples

```bash
# Download firmware
west tl-bdt download --chip TLSR9528A -i build/gpio_demo.bin

# Read 16 bytes from Flash
west tl-bdt read --chip TLSR9528A -a 0x00 -s 16

# Erase Flash
west tl-bdt erase --chip TLSR9528A -a 0x00 -s 4k

# Lock Flash
west tl-bdt lock --chip TLSR9528A -a 0x00 -s 512k

# Reset device
west tl-bdt reset --chip TLSR9528A

# Specify BDT tool path
west tl-bdt download --bdt-path /path/to/BDT --chip TLSR9528A -i build/firmware.bin
```

### BDT Path Configuration (Priority from high to low)

1. Command line: `--bdt-path /path/to/bdt`
2. Environment variable: `BDT_PATH=/path/to/bdt`
3. System PATH
4. SDK directory: `${TELINK_BASE}/tools/`

### Cross-Platform

| Platform | Executable |
|----------|-----------|
| Windows | `Cmd_download_tool.exe` |
| Linux | `bdt` |

## `west tl-boards` — Board Information

```bash
west tl-boards              # List all supported boards
west tl-boards -v           # Show detailed information
west tl-boards --soc TLSR9528A  # Filter by chip
```

## `west tl-socs` — Chip Information

```bash
west tl-socs                # List all supported chips
west tl-socs -v             # Show detailed information
```
