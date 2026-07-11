---
title: PLIC Interrupt Controller
status: STABLE
---

# PLIC Interrupt Controller

## Overview

The PLIC (Platform-Level Interrupt Controller) driver provides a system interrupt management interface. It allows developers to configure interrupt priorities, enable or disable specific interrupt sources, and manage interrupt preemption (nesting).

The interrupt handling mode (General vs. Vector) is determined at compile time via system configuration (`.config`).

**Key Features:**

- Compile-time selection of global interrupt mode (General / Vector)
- Interrupt priority and threshold management
- Interrupt source enable/disable
- Interrupt nesting support
- Optional software interrupt support (Trigger, Enable, Disable)

## Data Types and Enums

### Interrupt Priorities

`enum tlk_irq_priority`

| Value | Description |
|---|------|
| `TLK_IRQ_PRI_LEV0` | Priority 0 — no interrupt generated (effectively disabled) |
| `TLK_IRQ_PRI_LEV1` | Priority Level 1 (Lowest) |
| `TLK_IRQ_PRI_LEV2` | Priority Level 2 |
| `TLK_IRQ_PRI_LEV3` | Priority Level 3 (Highest) |

## API Reference

### `TLK_PLIC_ISR_REGISTER` (Macro)

A helper macro to define and register an Interrupt Service Routine (ISR) for a specific interrupt number. It automatically generates the correct function attributes for Vector or General mode.

```c
TLK_PLIC_ISR_REGISTER(my_uart_handler, IRQ_UART0);
```

| Parameter | Description |
|---|------|
| `isr` | The C function name to be called as the handler |
| `irq_num` | The interrupt number (e.g., `IRQ_UART0`) |

### `tlk_plic_interrupt_enable`

Enables a specific interrupt source.

```c
void tlk_plic_interrupt_enable(uint32_t src);
```

### `tlk_plic_interrupt_disable`

Disables a specific interrupt source.

```c
void tlk_plic_interrupt_disable(uint32_t src);
```

### `tlk_plic_set_priority`

Sets the priority level for a specific interrupt source.

```c
void tlk_plic_set_priority(uint32_t src, enum tlk_irq_priority priority);
```

### `tlk_plic_set_threshold`

Sets the global interrupt threshold. Only interrupts with a priority strictly higher than this threshold will be serviced.

```c
void tlk_plic_set_threshold(enum tlk_irq_priority threshold);
```

### `tlk_plic_set_pending`

Manually sets an interrupt source as pending.

```c
void tlk_plic_set_pending(uint32_t src);
```

### `tlk_plic_clr_all_request`

Clears all pending interrupt requests.

```c
int32_t tlk_plic_clr_all_request(void);
```

### `tlk_plic_preempt_enable`

Enables interrupt preemption (nested interrupts) for priorities higher than the specified level.

```c
void tlk_plic_preempt_enable(tlk_core_preempt_pri_e preempt_pri);
```

### `tlk_plic_preempt_disable`

Disables interrupt preemption.

```c
void tlk_plic_preempt_disable(void);
```

### `tlk_plic_irqs_preprocess_for_wfi`

Prepares the PLIC controller before the system enters a "Wait For Interrupt" (WFI) or sleep state.

```c
void tlk_plic_irqs_preprocess_for_wfi(uint8_t flag, tlk_mie_e mie);
```

### `tlk_plic_irqs_postprocess_for_wfi`

Restores the PLIC state after the system wakes up from WFI or sleep.

```c
void tlk_plic_irqs_postprocess_for_wfi(void);
```

### Software Interrupt APIs

!!! info "Requires `CONFIG_TLK_PLIC_SW` enabled"

| Function | Description |
|---|------|
| `tlk_plic_sw_set_pending()` | Manually triggers a software interrupt |
| `tlk_plic_sw_interrupt_enable()` | Enables the software interrupt source |
| `tlk_plic_sw_interrupt_disable()` | Disables the software interrupt source |

## Interrupt Handling Modes

| Mode | Description |
|------|------|
| **General** | All interrupts share a single entry point; query the interrupt source in the ISR |
| **Vector** | Each interrupt source has an independent vector address; direct jump |

## Interrupt Nesting

PLIC supports priority-based interrupt preemption:

- High-priority interrupts can preempt low-priority interrupts
- Control the minimum response priority via `tlk_plic_set_threshold`

## Integration with GPIO Interrupts

GPIO interrupts are routed through PLIC. Configuration steps:

1. Configure PLIC interrupt priority
2. Configure GPIO interrupt trigger condition (`tlk_gpio_irq_configure`)
3. Register GPIO interrupt callback (`tlk_gpio_irq_add_callback`)
4. Enable global interrupts (`tlk_core_interrupt_enable`)

```c
// Complete example
tlk_plic_set_priority(IRQ_GPIO, 3);
tlk_gpio_irq_configure(GPIO_PORT_A, GPIO_PIN_0, TLK_GPIO_INTR_RISING_EDGE);
tlk_gpio_irq_add_callback(GPIO_PORT_A, &my_callback);
tlk_core_interrupt_enable();
```
