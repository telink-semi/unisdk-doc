---
title: IRQ Nesting Sample
status: DRAFT
---

# IRQ Nesting Sample

:::{note} Document Status: DRAFT — Content is being finalized
:::

## Overview

The `irq_demo` sample (source directory `samples/irq_demo`) demonstrates interrupt management,
prioritization, and nesting using the PLIC (Platform-Level Interrupt Controller), Machine
Software Interrupts (PLIC SW / MSI), and Machine Timer Interrupts (MTIMER / MTI).

:::{note} Source directory name
The sample's source directory is `samples/irq_demo` (project name `IRQ_Demo`), not
`irq_nesting_demo`. Build and download paths below use the actual directory name.
:::

## Features Demonstrated

- PLIC software interrupt (MSI) setup and callback registration (`tlk_plic_sw_register_callback`)
- Machine timer interrupt (MTI) setup and callback registration (`tlk_mtimer_irq_register_callback`)
- PLIC external interrupt (MEI) priority configuration across three tiers (`tlk_plic_set_priority`)
- Optional nested/preemptive interrupt handling via `tlk_plic_enable_preempt()`
- Cross-triggering of interrupts from within handlers to visualize nesting depth

## How It Works

### Initialization

1. **MSI Configuration** — Enables the PLIC_SW subsystem and registers `tlk_sample_msi_handler`
   as its callback.
2. **MTI Configuration** — Registers `tlk_sample_mti_handler` as the machine timer interrupt
   callback.
3. **MEI Configuration** — Sets PLIC priorities for three sources:
   - `TLK_SAMPLE_PLIC_SRC_LOW` (vector 12) → `TLK_IRQ_PRI_LEV1`
   - `TLK_SAMPLE_PLIC_SRC_HIGH` (vector 13) → `TLK_IRQ_PRI_LEV2`
   - `UNISDK_PLIC_IRQ_NUM_UART0` → `TLK_IRQ_PRI_LEV3` (used for debug logging output)
4. **Preemption** — If both `CONFIG_TLK_IRQ_DEMO_IRQ_BASE_PLIC` and
   `CONFIG_TLK_IRQ_DEMO_PLIC_PREEMPT` are enabled, `tlk_plic_enable_preempt()` is called to allow
   nested PLIC interrupt execution.
5. **Global Enable** — Enables the MSIE, MTIE and MEIE bits in `mie`, then calls
   `tlk_core_interrupt_enable()`.

### Cascading Nesting Cycle

Based on the `TLK_IRQ_DEMO_IRQ_BASE` choice, `main()` triggers one of the primary interrupt
sources to kick off the cascade:

```c
#if TLK_IS_ENABLED(CONFIG_TLK_IRQ_DEMO_IRQ_BASE_PLIC_SW)
    tlk_plic_sw_set_pending();
#elif TLK_IS_ENABLED(CONFIG_TLK_IRQ_DEMO_IRQ_BASE_MTIMER)
    tlk_mtimer_set_mtime_compare(tlk_mtimer_get_mtime());
#elif TLK_IS_ENABLED(CONFIG_TLK_IRQ_DEMO_IRQ_BASE_PLIC)
    tlk_plic_set_pending(TLK_SAMPLE_PLIC_SRC_LOW);
#endif
```

Once inside a handler, it purposely cross-triggers the other interrupt sources by setting their
pending registers (`tlk_plic_set_pending`, `tlk_plic_sw_set_pending`, or writing `mtimecmp`). To
make the nesting visible over UART, each handler:

- increments a shared `tlk_log_depth` counter and indents its log output accordingly,
- logs the current `mie` bits via `tlk_sample_log_mie()`,
- uses a local `static volatile uint8_t processed` guard (in the PLIC handlers) to avoid
  re-triggering itself indefinitely, and
- decrements `tlk_log_depth` before returning.

The PLIC low/high handlers additionally call `tlk_api_time_delay(100)` before returning, giving
the newly-pended higher/lower-priority interrupt time to become pending before the current
handler exits.

## Configuration Options

All options are exposed via **Kconfig** under *IRQ Sample configuration*.

| Option | Description |
|------|------|
| `CONFIG_TLK_IRQ_DEMO_IRQ_BASE_PLIC_SW` | Use the PLIC software interrupt (MSI) as the cascade's starting trigger (default choice) |
| `CONFIG_TLK_IRQ_DEMO_IRQ_BASE_MTIMER` | Use the machine timer interrupt (MTI) as the cascade's starting trigger |
| `CONFIG_TLK_IRQ_DEMO_IRQ_BASE_PLIC` | Use the PLIC external low-priority interrupt (MEI) as the cascade's starting trigger |
| `CONFIG_TLK_IRQ_DEMO_PLIC_PREEMPT` | Enable PLIC preemption (nested execution) of external interrupts; only selectable when `TLK_IRQ_DEMO_IRQ_BASE_PLIC` is chosen |

`TLK_IRQ_DEMO_IRQ_BASE_PLIC_SW`, `_MTIMER`, and `_PLIC` form a single-choice group (exactly one
is active at a time); PLIC_SW is the default.

## Build & Run

```bash
west tl-build samples/irq_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/irq_demo.bin
```

Source code: `samples/irq_demo/main.c`
