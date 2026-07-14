---
title: GPIO Sample
status: STABLE
---

# GPIO Sample

## Overview

The `gpio_demo` sample demonstrates the basic usage of the GPIO driver, including input/output operations, interrupt handling, and sleep APIs.

## Features Demonstrated

- Basic GPIO configuration and pin control (`tlk_gpio_configure`, `tlk_gpio_pin_write`, `tlk_gpio_pin_toggle`)
- GPIO interrupt usage and callback registration (requires `CONFIG_TLK_GPIO_DEMO_INTERRUPT` enabled)

## How It Works

### Initialization

1. **LED0 Configuration** — Configured as output mode, toggled every 2 seconds in the main loop
2. **Interrupt Configuration (optional)** — When `CONFIG_TLK_GPIO_DEMO_INTERRUPT` is enabled:
   - LED1 is configured as output (toggled in the interrupt callback)
   - KEY0 is configured as input with pull-down
   - Registers a GPIO interrupt callback (`gpio_cb`)
   - Sets rising-edge trigger
   - Enables global interrupts

### Main Loop

```c
while (1)
{
    tlk_gpio_pin_toggle(UNISDK_BOARD_LED_0_PORT, UNISDK_BOARD_LED_0_PIN);
    tlk_api_delay(TLK_SEC_TO_US(2));
    tlk_api_sleep(TLK_SEC_TO_MS(2));
}
```

!!! note "Board-Specific Macros"
    The `UNISDK_BOARD_LED_0_PORT` and `UNISDK_BOARD_LED_0_PIN` macros are defined in the board-specific `tlk_board_pinout.h` header. These resolve to the correct port and pin for the target board's LED.

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_GPIO_DEMO_INTERRUPT` | Enable interrupt demo: KEY0 rising-edge trigger, LED1 toggled in callback |

## Build & Run

```bash
west tl-build samples/gpio_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/gpio_demo.bin
```

Source code: `samples/gpio_demo/main.c`
