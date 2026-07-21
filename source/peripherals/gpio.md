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
- Ability to disable pin functionality

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
| `TLK_GPIO_INPUT_PULL_UP_{name}` | *Generated based on config `UNISDK_GPIO_PULL_DOWN_OPTIONS_COUNT`* Input with a specific pull-up value. |
| `TLK_GPIO_INPUT_PULL_DOWN_{name}` | *Generated based on config `UNISDK_GPIO_PULL_DOWN_OPTIONS_COUNT`* Input with a specific pull-down value. |

### Interrupt Trigger Types

`enum tlk_gpio_intr_trigger`

| Value | Description |
|---|------|
| `TLK_GPIO_INTR_RISING_EDGE` | Rising edge trigger |
| `TLK_GPIO_INTR_FALLING_EDGE` | Falling edge trigger |
| `TLK_GPIO_INTR_HIGH_LEVEL` | High level trigger |
| `TLK_GPIO_INTR_LOW_LEVEL` | Low level trigger |
| `TLK_GPIO_INTR_BOTH_EDGE` | Both edges trigger |

### Interrupt Callback Types

Types used for handling GPIO interrupts via user-registered callbacks.

**Callback Handler Type**

Function pointer type for a GPIO interrupt callback.

```c
typedef void (*tlk_gpio_irq_callback_handler)(enum tlk_gpio_port port,
                                          enum tlk_gpio_pin pin);
```

| Parameter | Description |
|---|------|
| `port` | GPIO port on which the interrupt occurred. |
| `pin` | GPIO pin that triggered the interrupt. |

**Callback Registration Structure**

Structure used to register a GPIO interrupt callback in the internal callback list.

```c
struct tlk_gpio_irq_callback {
    struct tlk_list_node node;
    tlk_gpio_irq_callback_handler handler;
    enum tlk_gpio_pin pin;
};
```

| Field | Description |
|---|------|
| `node` | Internal list node used to link callbacks. |
| `handler` | User-defined interrupt callback function. |
| `pin` | GPIO pin associated with this callback. |

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

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `port` | `enum tlk_gpio_port` | GPIO port. |
| `pin` | `enum tlk_gpio_pin` | GPIO pin. |

**Return value:** None

### `tlk_gpio_configure`

Sets the GPIO pin mode (input/output, optional pull-up/pull-down).

```c
void tlk_gpio_configure(enum tlk_gpio_port port, enum tlk_gpio_pin pin,
                        enum tlk_gpio_mode mode);
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `port` | `enum tlk_gpio_port` | GPIO port. |
| `pin` | `enum tlk_gpio_pin` | GPIO pin. |
| `mode` | `enum tlk_gpio_mode` | GPIO mode (output / input pull-up / pull-down). |

**Return value:** None

### `tlk_gpio_pin_write`

Sets the pin output level.

```c
void tlk_gpio_pin_write(enum tlk_gpio_port port, enum tlk_gpio_pin pin, bool value);
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `port` | `enum tlk_gpio_port` | GPIO port. |
| `pin` | `enum tlk_gpio_pin` | GPIO pin. |
| `value` | `bool` | Logic level (`true` = high, `false` = low). |

**Return value:** None

### `tlk_gpio_pin_toggle`

Toggles the current output value of the pin.

```c
void tlk_gpio_pin_toggle(enum tlk_gpio_port port, enum tlk_gpio_pin pin);
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `port` | `enum tlk_gpio_port` | GPIO port. |
| `pin` | `enum tlk_gpio_pin` | GPIO pin. |

**Return value:** None

### `tlk_gpio_pin_read`

Reads the current logic level of the pin.

```c
bool tlk_gpio_pin_read(enum tlk_gpio_port port, enum tlk_gpio_pin pin);
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `port` | `enum tlk_gpio_port` | GPIO port. |
| `pin` | `enum tlk_gpio_pin` | GPIO pin. |

**Return value:** Returns `true` if the pin level is high, and `false` if low.

### `tlk_gpio_set_mux`

Configures the pin multiplexing function.

```c
void tlk_gpio_set_mux(enum tlk_gpio_port port, enum tlk_gpio_pin pin, uint8_t mux);
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `port` | `enum tlk_gpio_port` | GPIO port. |
| `pin` | `enum tlk_gpio_pin` | GPIO pin. |
| `mux` | `uint8_t` | Multiplexer index for the selected function. |

**Return value:** None

### `tlk_gpio_irq_configure`

:::{info} Requires `CONFIG_TLK_PLIC` enabled
:::

Sets the interrupt trigger type.

```c
void tlk_gpio_irq_configure(enum tlk_gpio_port port, enum tlk_gpio_pin pin,
                            enum tlk_gpio_intr_trigger trigger);
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `port` | `enum tlk_gpio_port` | GPIO port. |
| `pin` | `enum tlk_gpio_pin` | GPIO pin. |
| `trigger` | `enum tlk_gpio_intr_trigger` | Interrupt trigger mode (edge or level). |

**Return value:** None

### `tlk_gpio_irq_add_callback`

:::{info} Requires `CONFIG_TLK_PLIC` enabled
:::

Registers an interrupt callback function.

```c
void tlk_gpio_irq_add_callback(enum tlk_gpio_port port,
                               struct tlk_gpio_irq_callback *callback);
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `port` | `enum tlk_gpio_port` | GPIO port. |
| `callback` | `struct tlk_gpio_irq_callback *` | Pointer to GPIO interrupt callback structure. |

**Return value:** None

## Kconfig Configuration

```text
GPIO_PORT_{name}_ENABLED
│   Enables the specific GPIO port instance (where {name} is the port name, e.g., A, B, etc.).
│   Automatically selects the corresponding internal port index.
│   Default: `y`

TLK_GPIO_PREVENT_SLEEP
│   Indicates that the system should not enter sleep mode if any GPIO configured as an output is enabled.
│   Default: `y` if `PM` is enabled, otherwise `n`.

TLK_GPIO_PM_DEVICE
│   Indicates that Power Management support is enabled for the GPIO driver.
│   Default: `y` if `PM` is enabled, otherwise `n`.
```

### View in the menuconfig

![alt text](pics/gpio_1.png)
*Figure 1. GPIO driver configurations*

![alt text](pics/gpio_2.png)
*Figure 2. GPIO driver ports configurations*

## Related Resources

- [GPIO Samples](../samples/gpio.md) — Ready-to-run GPIO sample code
