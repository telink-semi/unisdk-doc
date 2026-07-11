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

1. **LED0 Configuration** — Configured as output mode, toggled once per second in the main loop
2. **Interrupt Configuration (optional)** — When `CONFIG_TLK_GPIO_DEMO_INTERRUPT` is enabled:
   - LED1 is configured as output (toggled in the interrupt callback)
   - KEY0 is configured as input with pull-down
   - Registers a GPIO interrupt callback (`gpio_cb`)
   - Sets rising-edge trigger
   - Enables global interrupts

### Main Loop

```c
while (1) {
    tlk_gpio_pin_toggle(GPIO_PORT_B, GPIO_PIN_4);  // Toggle LED0
    tlk_sleep_ms(1000);                             // Delay 1 second
}
```

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_GPIO_DEMO_INTERRUPT` | Enable interrupt demo: KEY0 rising-edge trigger, LED1 toggled in callback |

## Build & Run

```bash
west tl-build samples/gpio_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/gpio_demo.bin
```

Source code: [samples/gpio_demo/main.c](file:///home/test/SDK/unisdk_trae/unisdk/samples/gpio_demo/main.c)
