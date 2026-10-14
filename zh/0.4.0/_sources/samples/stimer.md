---
title: STIMER Sample
status: DRAFT
---

# STIMER Sample

:::{note} Document Status: DRAFT — Content is being finalized
:::

## Overview

The `stimer_demo` sample demonstrates the usage of the System Timer (STIMER) driver on Telink
RISC-V MCUs: timer initialization, interrupt configuration, periodic callbacks, and integration
with GPIO and the sleep API.

## Features Demonstrated

- System timer configuration and start (`tlk_stimer_enable`, `tlk_stimer_set_tick`,
  `tlk_stimer_set_auto_mode`)
- Timer interrupt setup and callback registration (`tlk_stimer_register_callback`)
- Periodic interrupt generation using capture-compare (`tlk_stimer_irq_set_capture`)
- GPIO control from both the main loop and interrupt context
- Low-power sleep usage in the main loop while the timer interrupt continues in the background

## How It Works

### Initialization

1. **GPIO Configuration** — LED0 and LED1 are both configured as outputs. LED0 is toggled in the
   main loop; LED1 is toggled inside the timer interrupt callback.
2. **System Timer Setup** — The timer is enabled (`tlk_stimer_enable()`), its tick counter reset
   to 0 (`tlk_stimer_set_tick(0)`), and auto mode enabled (`tlk_stimer_set_auto_mode(true)`) for
   continuous free-running operation.
3. **Interrupt Configuration** — A callback (`timer_cb`) is registered via
   `tlk_stimer_register_callback()`. The first capture-compare event is scheduled 500 ms out,
   the STIMER IRQ mask is enabled, the STIMER PLIC interrupt is enabled, and global interrupts
   are enabled with `tlk_core_interrupt_enable()`.

```c
tlk_stimer_enable();
tlk_stimer_set_tick(0);
tlk_stimer_set_auto_mode(true);
tlk_stimer_register_callback(timer_cb);

tlk_stimer_irq_set_capture(tlk_stimer_get_tick() + TLK_SYSTEM_TIMER_TICK_1MS * 500);
tlk_stimer_irq_set_mask(TLK_STIMER_IRQ_MASK_TIMER_IRQ_EN);
tlk_plic_interrupt_enable(UNISDK_PLIC_IRQ_NUM_STIMER);

tlk_core_interrupt_enable();
```

### Main Loop

The main loop toggles LED0 and sleeps for 1 second between toggles:

```c
while (1)
{
    tlk_gpio_pin_toggle(PINMUX_LED_0_PORT, PINMUX_LED_0_PIN);
    tlk_api_sleep(TLK_SEC_TO_MS(1));
}
```

### Timer Callback

`timer_cb()` runs on every STIMER interrupt (every 500 ms): it reschedules the next capture
compare event, clears the interrupt status, and toggles LED1.

```c
void timer_cb(void)
{
    tlk_stimer_irq_set_capture(tlk_stimer_get_tick() + TLK_SYSTEM_TIMER_TICK_1MS * 500);
    tlk_stimer_irq_clr_status(TLK_STIMER_IRQ_STATUS_TIMER_IRQ);
    tlk_gpio_pin_toggle(PINMUX_LED_1_PORT, PINMUX_LED_1_PIN);
}
```

Because the main loop toggles LED0 once per second while the timer interrupt toggles LED1 twice
per second (500 ms period), LED0 and LED1 blink at visibly different rates, demonstrating that the
STIMER interrupt keeps firing independently of the main loop's sleep/wake cycle.

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_STIMER_INTERRUPT` | Enable the STIMER interrupt demo: registers `timer_cb`, schedules periodic capture-compare events, and toggles LED1 from interrupt context. Enabled by default (`def_bool y`) and selects `TLK_SYSTEM_TIMER_IRQ_ENABLE`. |

## Build & Run

```bash
west tl-build samples/stimer_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/stimer_demo.bin
```

Source code: `samples/stimer_demo/main.c`
