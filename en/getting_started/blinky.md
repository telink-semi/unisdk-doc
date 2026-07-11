---
title: First Example — Blinky
status: STABLE
---

# First Example: Blinky (LED Blinking)

This document details how to compile, flash, and run the first UniSDK example program — the GPIO demo (Blinky LED blinking).

## Prerequisites

- [Environment setup](index.md) is complete
- Toolchain `TELINK_TOOLCHAIN_PATH` is configured
- You have a Telink development board on hand (this example uses TLSR9528A_EVK)

## Example Overview

The `gpio_demo` example demonstrates basic GPIO input/output functionality and interrupt handling:

- Configures a GPIO pin as output mode, periodically toggling to achieve LED blinking
- Configures interrupt handling to respond to button input
- Demonstrates the use of sleep APIs

Source code location: `samples/gpio_demo/main.c`

## Step 1: Configure Chip Type

```bash
# Method 1: Interactive configuration (recommended for first use)
west tl-config

# Method 2: Using Make (with SOC/BOARD preset)
make config SOC=TLSR9528A BOARD=TLSR9528A_EVK
```

!!! tip "Available Chips and Boards"
    List all supported options:
    ```bash
    west tl-socs      # View all chips
    west tl-boards    # View all boards
    ```

## Step 2: Compilation

```bash
# West command (recommended)
west tl-build samples/gpio_demo --board TLSR9528A_EVK

# Or using Make
make build APP=samples/gpio_demo BOARD=TLSR9528A_EVK
```

After a successful build, the output files are located in the `build/` directory:

```
build/
├── gpio_demo.bin     # Firmware binary file
├── gpio_demo.elf     # ELF executable (contains debug information)
└── gpio_demo.map     # Memory map file
```

## Step 3: Flashing

```bash
# Flash using BDT tool
west tl-bdt download --chip TLSR9528A -i build/gpio_demo.bin

# Specify flash address
west tl-bdt download --chip TLSR9528A -i build/gpio_demo.bin -a 0x00
```

## Step 4: Verification

After flashing is complete, the LED on the development board will blink at a fixed frequency, indicating that the program is running normally.

## Custom Modifications

Open `samples/gpio_demo/main.c` to modify parameters such as the LED blinking frequency:

```c
// Modify the delay time to change the blinking frequency
tlk_sleep_ms(500);  // 500ms = blinks once per second
```

After making changes, recompile and flash:

```bash
west tl-build samples/gpio_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/gpio_demo.bin
```

## Next Steps

- [GPIO Driver Documentation](../peripherals/gpio.md)
- [Build System Details](../build_config/index.md)
- [More Examples](../samples/index.md)
