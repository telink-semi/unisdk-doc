---
title: PM Power Management Sample
status: STABLE
---

# PM Power Management Sample

## Overview

The `pm_demo` sample demonstrates the usage of the Power Management (PM) subsystem. It shows how to enter low-power modes, configure GPIO wake-up, and preserve application state across low-power transitions.

## Features Demonstrated

- Entering Deep/Suspend sleep using `tlk_api_sleep`
- GPIO wake-up configuration (optional)
- Before/After sleep hook functions
- Variable retention across Deep Sleep Retention mode

## How It Works

### Initialization

1. **LED State Initialization** — When `CONFIG_TLK_PM_DEMO_ENABLE_LED` is enabled:
   - LED state variables are stored in the **retention section**
   - Initial state: LED0 ON, LED1 OFF

2. **Hook Registration** — Registers pre-sleep and post-sleep callbacks:
   - `flip_led()` → Flips LED state before sleep
   - `init_led()` → Re-initializes GPIO after wake-up

### Main Loop

1. Delay 1 second
2. Optionally configure GPIO wake-up source
3. Enter low-power mode for 1 second

### GPIO Wake-up (Optional)

When `CONFIG_TLK_PM_DEMO_ENABLE_GPIO_INPUT` is enabled:

- GPIO C4 is configured as a wake-up source (high-level wake-up)
- Suspend mode is used instead of Deep Sleep when GPIO wake-up is enabled

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_PM_DEMO_ENABLE_LED` | LED demo: state preserved in retention area |
| `CONFIG_TLK_PM_DEMO_ENABLE_GPIO_INPUT` | GPIO wake-up demo |
| `CONFIG_TLK_PM_DEMO_DISABLE_LED_BEFORE_SLEEP` | Turn off LED before sleep (visual sleep entry indicator) |

## Build & Run

```bash
west tl-build samples/pm_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/pm_demo.bin
```
