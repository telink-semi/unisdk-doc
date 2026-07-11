---
title: Power Management (PM)
status: STABLE
---

# Power Management (PM) Driver

## Overview

The PM (Power Management) driver provides an interface for controlling microcontroller power states. It supports the system entering various low-power modes to save energy, and defines system wakeup mechanisms. The driver also manages retention memory and sleep duration validation.

**Key Features:**

- Multiple sleep modes (Suspend, Deep Sleep, Deep Retention)
- Wakeup source management (GPIO Pad, Timer, Core, Comparator)
- Configurable sleep duration limits (minimum time)
- Retention memory size configuration
- Error handling for invalid sleep requests

## Sleep Modes

`enum tlk_pm_sleep_mode`

| Mode | Power | Wakeup Speed | Description |
|------|------|---------|------|
| `TLK_PM_SLEEP_MODE_SUSPEND` | Medium | Fast | SRAM retained, peripherals partially powered |
| `TLK_PM_SLEEP_MODE_DEEP_SLEEP` | Very low | Slow | SRAM not retained, most peripherals powered off |
| `TLK_PM_SLEEP_MODE_DEEP_RETENTION` | Low | Medium | SRAM partially retained |

## Wakeup Sources

`enum tlk_pm_wakeup_source` (bitmask)

| Value | Description |
|---|------|
| `TLK_PM_WAKEUP_SOURCE_PAD` | GPIO pin wakeup |
| `TLK_PM_WAKEUP_SOURCE_TIMER` | System timer wakeup |
| `TLK_PM_WAKEUP_SOURCE_CORE` | Core event wakeup |
| `TLK_PM_WAKEUP_SOURCE_COMPARATOR` | Comparator wakeup |

## Driver API

### `tlk_pm_sleep`

Requests the system to enter a low-power mode.

```c
enum tlk_pm_sleep_status tlk_pm_sleep(enum tlk_pm_sleep_mode mode,
                                      uint32_t duration_us);
```

Return values:

| Value | Description |
|---|------|
| `TLK_PM_SLEEP_OK` | Successfully entered and exited sleep |
| `TLK_PM_SLEEP_TOO_SHORT` | Requested duration is less than the configured minimum |
| `TLK_PM_SLEEP_DENIED` | Sleep denied (e.g., blocked by a peripheral) |

### `tlk_pm_set_gpio_wakeup`

Configures a GPIO pin as a wakeup source.

```c
enum tlk_pm_sleep_status tlk_pm_set_gpio_wakeup(
    enum tlk_gpio_port port, enum tlk_gpio_pin pin,
    enum tlk_pm_gpio_wakeup_level polarity);
```

### `tlk_pm_get_wakeup_reason`

Gets the last wakeup reason.

```c
enum tlk_pm_wakeup_source tlk_pm_get_wakeup_reason(void);
```

### `tlk_pm_clear_wakeup_sources`

Clears wakeup source flags in preparation for the next sleep.

```c
void tlk_pm_clear_wakeup_sources(void);
```

## Typical Usage

```c
#include <tlk_api.h>

void sleep_example(void) {
    // Set GPIO A0 high level wakeup
    tlk_pm_set_gpio_wakeup(GPIO_PORT_A, GPIO_PIN_0,
                           TLK_PM_GPIO_WAKEUP_LEVEL_HIGH);

    // Enter Deep Sleep for 5 seconds
    enum tlk_pm_sleep_status status =
        tlk_pm_sleep(TLK_PM_SLEEP_MODE_DEEP_SLEEP, 5000000);

    if (status == TLK_PM_SLEEP_OK) {
        // Check wakeup reason
        enum tlk_pm_wakeup_source src = tlk_pm_get_wakeup_reason();
        if (src & TLK_PM_WAKEUP_SOURCE_PAD) {
            // GPIO wakeup
        }
        tlk_pm_clear_wakeup_sources();
    }
}
```

## Kconfig Configuration

```kconfig
CONFIG_TLK_PM_SUSPEND_MIN_DURATION_MS         # Suspend minimum duration (default 2ms)
CONFIG_TLK_PM_DEEP_SLEEP_MIN_DURATION_MS      # Deep Sleep minimum duration (default 3ms)
CONFIG_TLK_PM_DEEP_RETENTION_MIN_DURATION_MS  # Deep Retention minimum duration (default 3ms)
CONFIG_TLK_PM_RETENTION_MEMORY_SIZE           # Retention memory size
```

## Related Resources

- [PM Samples](../samples/pm.md)
