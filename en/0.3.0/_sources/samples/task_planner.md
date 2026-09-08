---
title: Task Planner Sample
status: DRAFT
---

# Task Planner Sample

## Overview

The `task_planner_demo` sample (under `samples/system_demo/`) demonstrates the Task Planner subsystem on the Telink RISC-V MCU platform: basic GPIO output driven through cooperative loop execution, task-scheduler execution, and an optional software timer, depending on which Task Planner mode is enabled.

## Features Demonstrated

- GPIO output configuration and control (`tlk_gpio_configure`, `tlk_gpio_pin_toggle`)
- Cooperative loop execution model (`user_loop()`, `TLK_REGISTER_LOOP`)
- Scheduler-based task execution (`TASK_SPAWN`, `TASK_DELAY`)
- Periodic execution using software timers (`TLK_SW_TIMER_REGISTER`, `tlk_task_sw_timer_start`), when enabled

## How It Works

### Initialization (`user_setup()`)

Called once during system startup. LED0, LED1, and LED2 are configured as GPIO outputs; if `CONFIG_TLK_SOFTWARE_TIMERS` is enabled, the periodic software timer `test_timer1` is also started:

```c
void user_setup(void)
{
    tlk_gpio_configure(PINMUX_LED_0_PORT, PINMUX_LED_0_PIN, TLK_GPIO_OUTPUT);
    tlk_gpio_configure(PINMUX_LED_1_PORT, PINMUX_LED_1_PIN, TLK_GPIO_OUTPUT);
    tlk_gpio_configure(PINMUX_LED_2_PORT, PINMUX_LED_2_PIN, TLK_GPIO_OUTPUT);

#if TLK_IS_ENABLED(CONFIG_TLK_SOFTWARE_TIMERS)
    tlk_task_sw_timer_start(&test_timer1);
#endif
}
```

### Mode 1: Loop Mode (`CONFIG_TLK_TASK_PLANNER_MODE_LOOP`)

`user_loop()` is executed repeatedly by the platform dispatcher (`while (1) { tlk_loop(); }`) and toggles LED0 every second:

```c
void user_loop(void)
{
    tlk_gpio_pin_toggle(PINMUX_LED_0_PORT, PINMUX_LED_0_PIN);
    tlk_api_time_delay(TLK_SEC_TO_US(1));
}

static void loop1(void)
{
    tlk_gpio_pin_toggle(PINMUX_LED_1_PORT, PINMUX_LED_1_PIN);
    tlk_api_time_delay(TLK_SEC_TO_US(2));
}

TLK_REGISTER_LOOP(loop1)
```

`loop1()` is registered as an additional loop handler via `TLK_REGISTER_LOOP` and toggles LED1 every 2 seconds, resembling the Arduino-style `loop()` model.

### Mode 2: Scheduler Mode (`CONFIG_TLK_TASK_PLANNER_MODE_SCHEDULER`)

`user_loop()` is called from the default task (its period set by `CONFIG_TLK_TASK_PLANNER_DEFAULT_TASK_LOOP_PERIOD_MS`) and just toggles LED0. `loop1()` is instead defined as a cooperatively-scheduled task via `TASK_SPAWN`, toggling LED1 and rescheduling itself every 2 seconds:

```c
void user_loop(void)
{
    tlk_gpio_pin_toggle(PINMUX_LED_0_PORT, PINMUX_LED_0_PIN);
}

static void loop1(tTask* t)
{
    tlk_gpio_pin_toggle(PINMUX_LED_1_PORT, PINMUX_LED_1_PIN);
    TASK_DELAY(t, TASK_MS(2000));
}

TASK_SPAWN(test_task1, loop1);
```

### Optional: Software Timer

When `CONFIG_TLK_SOFTWARE_TIMERS` is enabled, a periodic software timer (`test_timer1`) is statically registered via `TLK_SW_TIMER_REGISTER` and toggles LED2 every second, independent of the loop/scheduler mode:

```c
static void sw_timer_loop(void* arg)
{
    (void) arg;
    tlk_gpio_pin_toggle(PINMUX_LED_2_PORT, PINMUX_LED_2_PIN);
}

TLK_SW_TIMER_REGISTER(test_timer1, sw_timer_loop, SW_TIMER_MODE_PERIODIC, TASK_MS(1000));
```

A C++ variant of the same logic (`main.cpp`) is compiled instead of `main.c` when `CONFIG_TLK_ALLOW_CPP_WRAPPERS` is enabled.

:::{note} LED-to-mode mapping
| LED | Controlled by | Mode dependency |
|---|---|---|
| LED0 | `user_loop()` | Loop / Scheduler |
| LED1 | `loop1()` | Loop / Scheduler |
| LED2 | Software timer callback | `CONFIG_TLK_SOFTWARE_TIMERS` |
:::

## Configuration Options

The sample's own `Kconfig` just enables the Task Planner subsystem; execution mode and timing are controlled by the Task Planner subsystem's own options.

| Option | Description |
|------|------|
| `CONFIG_TLK_TASK_PLANNER_DEMO` | Always enabled (`def_bool y`) when this sample is built; selects `TLK_TASK_PLANNER`. |
| `CONFIG_TLK_TASK_PLANNER_MODE_LOOP` | (Task Planner subsystem) Enables cooperative loop-based execution. |
| `CONFIG_TLK_TASK_PLANNER_MODE_SCHEDULER` | (Task Planner subsystem) Enables task scheduler-based execution. |
| `CONFIG_TLK_TASK_PLANNER_DEFAULT_TASK` | (Task Planner subsystem, scheduler mode only) Enables periodic execution of `user_loop()` from the default task. |
| `CONFIG_TLK_TASK_PLANNER_DEFAULT_TASK_LOOP_PERIOD_MS` | (Task Planner subsystem) Execution period (ms) for `user_loop()` in scheduler mode; default `500`. |
| `CONFIG_TLK_SOFTWARE_TIMERS` | (Task Planner subsystem) Enables the periodic software timer that toggles LED2. |

## Build & Run

```bash
west tl-build samples/system_demo/task_planner_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/task_planner_demo.bin
```

Source code: `samples/system_demo/task_planner_demo/main.c`
