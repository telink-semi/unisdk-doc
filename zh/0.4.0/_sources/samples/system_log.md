---
title: System Log Sample
status: DRAFT
---

# System Log Sample

## Overview

The `log_demo` sample (under `samples/system_demo/`) demonstrates the debug logging subsystem, emitting a log message roughly once per second. Its behavior adapts to whether the Task Planner is enabled and, if so, which execution mode it runs in.

:::{note} README/sample mismatch
The `README.md` shipped alongside this sample currently describes the **Task Planner** demo (GPIO/LED toggling, software timers), not this log sample. This page is based directly on `main.c` and `Kconfig` instead — see {doc}`task_planner` for the sample that README actually documents.
:::

## Features Demonstrated

- Logging via `TLK_LOG_CREATE` / `TLK_LOG_INFO` / `tlk_log`
- Log rotation and the log interface loop (`tlk_logrotate`, `tlk_log_iface_loop`) when running without the Task Planner
- Integration with the Task Planner's Loop mode (`user_setup` / `user_loop`) and Scheduler mode

## How It Works

### Without Task Planner

If `CONFIG_TLK_TASK_PLANNER` is disabled, the sample owns its own `main()` and drives the logging pump directly:

```c
#if TLK_IS_DISABLED(CONFIG_TLK_TASK_PLANNER)

static uint32_t last = 0;
int             main(void)
{
    while (1)
    {
        tlk_log_iface_loop();
        tlk_logrotate();
        uint32_t now = tlk_api_time_get_micros();
        if (now - last >= 1000000)
        {
            last = now;
            tlk_log(demo_log, TLK_LOG_LEVEL_ERROR, "Test log USB");
        }
    }
}

#endif
```

`tlk_log_iface_loop()` and `tlk_logrotate()` are called on every iteration to service the log transport and rotate log storage; the actual message is only emitted once a second.

### With Task Planner — Loop Mode

When `CONFIG_TLK_TASK_PLANNER_MODE_LOOP` is enabled, the sample instead defines `user_setup()`/`user_loop()`, which the platform dispatcher calls repeatedly:

```c
#elif TLK_IS_ENABLED(CONFIG_TLK_TASK_PLANNER_MODE_LOOP)
void user_setup(void) {}

void user_loop(void)
{
    static uint32_t last = 0;
    uint32_t        now  = tlk_api_time_get_micros();
    if (now - last >= 1000000)
    {
        last = now;
        tlk_log(demo_log, TLK_LOG_LEVEL_ERROR, "Test log USB from Telink Loop");
    }
}
```

### With Task Planner — Scheduler Mode

When `CONFIG_TLK_TASK_PLANNER_MODE_SCHEDULER` is enabled, `user_loop()` is invoked periodically by the default task and simply logs on every call (the periodic interval is controlled by the Task Planner's own configuration, not by the sample):

```c
#elif TLK_IS_ENABLED(CONFIG_TLK_TASK_PLANNER_MODE_SCHEDULER)
void user_setup(void) {}

void user_loop(void)
{
    tlk_log(demo_log, TLK_LOG_LEVEL_ERROR, "Test log USB with Telink Scheduler");
}
#endif
```

A C++ variant of the same logic (`main.cpp`) is compiled instead of `main.c` when `CONFIG_TLK_ALLOW_CPP_WRAPPERS` is enabled.

## Configuration Options

The sample's own `Kconfig` only pulls in the modules it needs; the execution-mode behavior above is controlled by the Task Planner subsystem's own options.

| Option | Description |
|------|------|
| `CONFIG_TLK_GPIO` | Always enabled (`def_bool y`) — required by the shared board pinout headers. |
| `CONFIG_TLK_DEBUG_LOG_CONSOLE` | Always enabled (`def_bool y`) — routes log output to the console/log interface. |
| `CONFIG_TLK_BLE_CONTROLLER` | Defaults to `n` for this sample. |
| `CONFIG_TLK_TASK_PLANNER` | (Task Planner subsystem) When disabled, the sample runs its own `main()` loop; when enabled, behavior depends on the mode below. |
| `CONFIG_TLK_TASK_PLANNER_MODE_LOOP` | (Task Planner subsystem) Cooperative loop execution — logs once per second, gated in `user_loop()`. |
| `CONFIG_TLK_TASK_PLANNER_MODE_SCHEDULER` | (Task Planner subsystem) Task scheduler execution — logs unconditionally on each `user_loop()` invocation, at the scheduler's configured period. |

## Build & Run

```bash
west tl-build samples/system_demo/log_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/log_demo.bin
```

Source code: `samples/system_demo/log_demo/main.c`
