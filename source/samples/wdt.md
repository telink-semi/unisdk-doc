---
title: Watchdog Sample
status: DRAFT
---

# Watchdog Sample

:::{note} Document Status: DRAFT — Content is being finalized
:::

## Overview

The `wdt_demo` sample demonstrates the usage of the Watchdog Timer (WDT) driver, including
detecting a watchdog-triggered reboot, feeding the watchdog to pass its window, and letting it
expire to force a reset.

## Features Demonstrated

- Detecting the previous reboot's cause via `tlk_sys_get_reboot_reason` (`TLK_SYS_REBOOT_REASON_WDT`)
- Starting the watchdog with a timeout (`tlk_wdt_start`) and feeding it (`tlk_wdt_feed`)
- Optional GPIO indication of demo progress (LED0/LED1)
- Optional low-power sleep while the watchdog is running (`CONFIG_TLK_WDT_DEMO_PM`)
- Optional watchdog auto-start from startup code (`CONFIG_TLK_WDT_DEMO_STARTUP`)

## How It Works

On each boot:

1. **Reboot Reason Check** — Reads `tlk_sys_get_reboot_reason()` and logs whether the reset was
   caused by the watchdog or by another source.
2. **GPIO Indication (optional)** — If `CONFIG_TLK_WDT_DEMO_GPIO_INDICATION` is enabled, LED0 is
   configured as output and driven high, and LED1 is configured as output and driven low.
3. **Initial Delay** — Blocks for 2 seconds (`tlk_api_time_delay`).
4. **Watchdog Start** — If `CONFIG_TLK_WDT_DEMO_STARTUP` is enabled, the watchdog is assumed to
   already be running (started from startup code via `TLK_WDT_STARTUP_ENABLE`), so the sample
   just feeds it (`tlk_wdt_feed()`). Otherwise it starts the watchdog itself with a 5-second
   timeout (`tlk_wdt_start(TLK_SEC_TO_MS(5))`).
5. **Pass the WDT Window** — Waits 2 seconds, either via blocking delay
   (`tlk_api_time_delay`) or, if `CONFIG_TLK_WDT_DEMO_PM` is enabled, via low-power sleep
   (`tlk_api_sleep`) — demonstrating that the watchdog configuration survives a sleep cycle.
6. **LED1 On (optional)** — If GPIO indication is enabled, LED1 is driven high to show that the
   WDT window was passed successfully without a reset.
7. **Final Feed & Expire** — Feeds the watchdog one last time, then enters an infinite empty loop.
   Because nothing feeds the watchdog again, it eventually expires and resets the chip, and on
   the next boot `tlk_sys_get_reboot_reason()` reports `TLK_SYS_REBOOT_REASON_WDT`.

```c
// Feed the WDT and wait until it fires.
tlk_wdt_feed();

while (1)
{
}
```

## Configuration Options

All options are exposed via **Kconfig** under *WDT Sample configuration*.

| Option | Description |
|------|------|
| `CONFIG_TLK_WDT_DEMO_GPIO_INDICATION` | Enable LED0/LED1 GPIO indication of demo progress (selects `TLK_GPIO`) |
| `CONFIG_TLK_WDT_DEMO_PM` | Use `tlk_api_sleep` instead of a blocking delay to pass the WDT window, exercising PM (selects `TLK_API_SLEEP`, `TLK_PM`) |
| `CONFIG_TLK_WDT_DEMO_STARTUP` | Start the watchdog from startup code instead of from `main()` (selects `TLK_WDT_STARTUP_ENABLE`) |

## Build & Run

```bash
west tl-build samples/wdt_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/wdt_demo.bin
```

Source code: `samples/wdt_demo/main.c`
