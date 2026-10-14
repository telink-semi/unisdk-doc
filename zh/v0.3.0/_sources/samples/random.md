---
title: Random Sample
status: DRAFT
---

# Random Sample

## Overview

The `random_demo` sample demonstrates the usage of the TLK Random API. It generates a configurable sequence of random numbers and logs them to the console in a loop.

## Features Demonstrated

- Software random number generation (`tlk_random()`)
- Optional hardware TERO-based random source (`tlk_random_tero()`, TL721X only)
- Delay vs. sleep between iterations (`tlk_api_delay` / `tlk_api_sleep`)

## How It Works

### Main Loop

On every loop iteration the sample generates `CONFIG_TLK_RANDOM_DEMO_NUMBERS_COUNT` random values in the range `[0, CONFIG_TLK_RANDOM_DEMO_MAX_NUMBER]` using `tlk_random()` and logs each one:

```c
int main(void)
{
    while (1)
    {
        TLK_LOG_INFO(random_demo, "Random numbers:\n");

        for (uint8_t i = 0; i < CONFIG_TLK_RANDOM_DEMO_NUMBERS_COUNT; i++)
        {
            TLK_LOG_INFO(random_demo,
                         "\t%u: %u\n",
                         (i + 1),
                         tlk_random() % (CONFIG_TLK_RANDOM_DEMO_MAX_NUMBER + 1));
        }

        TLK_LOG_INFO(random_demo, "\n");

#ifndef CONFIG_TLK_RANDOM_DEMO_SLEEP
        tlk_api_delay(TLK_SEC_TO_US(4));
#else
        tlk_api_sleep(TLK_SEC_TO_MS(4));
#endif
    }
}
```

Between iterations, the sample either busy-delays for 4 seconds via `tlk_api_delay`, or — if `CONFIG_TLK_RANDOM_DEMO_SLEEP` is enabled — enters low-power sleep for 4 seconds via `tlk_api_sleep`.

:::{note} TERO Module (TL721X only)
The sample can optionally repeat the same sequence using `tlk_random_tero()`, a hardware TERO-based random source available only on **TL721X**. It is disabled by default; to enable it, edit `main.c` and set `#define USE_TERO_MODULE 1`. This is a source-level toggle, not a Kconfig option.
:::

## Configuration Options

| Option | Type | Default | Description |
|------|------|------|------|
| `CONFIG_TLK_RANDOM_DEMO_NUMBERS_COUNT` | int | `10` | How many numbers to generate per iteration. Range: 1–100. |
| `CONFIG_TLK_RANDOM_DEMO_MAX_NUMBER` | int | `10` | Upper bound (inclusive) of the generated values. |
| `CONFIG_TLK_RANDOM_DEMO_SLEEP` | bool | `n` | Use sleep instead of delay between iterations. Automatically selects `TLK_API_SLEEP` and implies `TLK_RANDOM_PM`. |

`TLK_RANDOM_DEMO` itself auto-selects `TLK_RANDOM` and `TLK_API_TIME`, so no manual selection of those is required.

## Build & Run

```bash
west tl-build samples/random_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/random_demo.bin
```

Source code: `samples/random_demo/main.c`
