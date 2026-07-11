---
title: GPIO Driver
status: STABLE
---

# GPIO Driver

## Overview

The GPIO (General Purpose Input/Output) driver provides an interface for configuring and using general-purpose microcontroller pins. It supports pin mode configuration (input, output, pull-up, pull-down), pin multiplexing (Pinmux), and direct pin state operations (write, read, toggle). It also supports interrupt handling with configurable trigger conditions and callback registration.

**Key Features:**

- GPIO mode configuration (input, output, pull-up, pull-down)
- Pin multiplexing (Mux)
- Direct pin control (write, read, toggle)
- Interrupt handling (edge/level trigger + callback)

## Data Types and Enums

### Port Identifiers

`enum tlk_gpio_port` — Generated at compile time based on `UNISDK_GPIO_PORT_COUNT` and `CONFIG_TLK_GPIO_PORT_##num##_ENABLED`.

| Value | Description |
|---|------|
| `GPIO_PORT_x` | Generated identifier for each enabled port |

### Pin Definitions

`enum tlk_gpio_pin` — Defines bitmasks for pins within a port.

| Value | Description |
|---|------|
| `TLK_GPIO_PIN_NONE` | No pin selected (value is 0) |
| `GPIO_PIN_x` | Pin index bitmask (x is 0-7), defined as `TLK_BIT(x)` |

### Pin Modes

`enum tlk_gpio_mode`

| Value | Description |
|---|------|
| `TLK_GPIO_OUTPUT` | Digital output (value is -1) |
| `TLK_GPIO_INPUT_NO_PULL` | Floating digital input |
| `TLK_GPIO_INPUT_PULL_UP` | Digital input with pull-up resistor |
| `TLK_GPIO_INPUT_PULL_DOWN` | Digital input with pull-down resistor |

### Interrupt Trigger Types

`enum tlk_gpio_intr_trigger`

| Value | Description |
|---|------|
| `TLK_GPIO_INTR_RISING_EDGE` | Rising edge trigger |
| `TLK_GPIO_INTR_FALLING_EDGE` | Falling edge trigger |
| `TLK_GPIO_INTR_HIGH_LEVEL` | High level trigger |
| `TLK_GPIO_INTR_LOW_LEVEL` | Low level trigger |
| `TLK_GPIO_INTR_BOTH_EDGE` | Both edges trigger |

### Port Pin Struct

```c
struct tlk_gpio_port_pin {
    enum tlk_gpio_port port;
    enum tlk_gpio_pin pin;
};
```

## Driver API

### `tlk_gpio_disable`

Disables the pin function and resets configuration.

```c
void tlk_gpio_disable(enum tlk_gpio_port port, enum tlk_gpio_pin pin);
```

### `tlk_gpio_configure`

Sets the GPIO pin mode (input/output, optional pull-up/pull-down).

```c
void tlk_gpio_configure(enum tlk_gpio_port port, enum tlk_gpio_pin pin,
                        enum tlk_gpio_mode mode);
```

### `tlk_gpio_pin_write`

Sets the pin output level.

```c
void tlk_gpio_pin_write(enum tlk_gpio_port port, enum tlk_gpio_pin pin, bool value);
```

### `tlk_gpio_pin_toggle`

Toggles the current output value of the pin.

```c
void tlk_gpio_pin_toggle(enum tlk_gpio_port port, enum tlk_gpio_pin pin);
```

### `tlk_gpio_pin_read`

Reads the current logic level of the pin.

```c
bool tlk_gpio_pin_read(enum tlk_gpio_port port, enum tlk_gpio_pin pin);
```

### `tlk_gpio_set_mux`

Configures the pin multiplexing function.

```c
void tlk_gpio_set_mux(enum tlk_gpio_port port, enum tlk_gpio_pin pin, uint8_t mux);
```

### `tlk_gpio_irq_configure`

!!! info "Requires `CONFIG_TLK_PLIC` enabled"

Sets the interrupt trigger type.

```c
void tlk_gpio_irq_configure(enum tlk_gpio_port port, enum tlk_gpio_pin pin,
                            enum tlk_gpio_intr_trigger trigger);
```

### `tlk_gpio_irq_add_callback`

!!! info "Requires `CONFIG_TLK_PLIC` enabled"

Registers an interrupt callback function.

```c
void tlk_gpio_irq_add_callback(enum tlk_gpio_port port,
                               struct tlk_gpio_irq_callback *callback);
```

## Kconfig Configuration

```kconfig
CONFIG_TLK_GPIO_PORT_x_ENABLED         # Enable a specific GPIO port
CONFIG_TLK_GPIO_PREVENT_SLEEP     # Prevent sleep when GPIO is outputting
CONFIG_TLK_GPIO_PM_DEVICE         # GPIO power management support
```

## Related Resources

- [GPIO Samples](../samples/gpio.md) — Ready-to-run GPIO sample code
