---
title: BLE Controller
status: STABLE
---

# BLE Controller Coding Standards

## Overview

This document describes the coding standards for the BLE Controller ROM, applicable to all code under `subsystem/ble/controller/`.

## File Naming

- Source files use lowercase letters separated by underscores
- Example: `tlk_ble_ll_acl.c`

## Function Naming

### Public Functions

Use the `tlk_ble_` prefix:

```c
void tlk_ble_ll_init(void);
int  tlk_ble_ll_send_data(uint8_t *data, uint16_t len);
```

### Internal Functions

Use the `_` prefix to mark module-internal functions:

```c
static void _internal_process(void);
```

## Variable Naming

- Global variables use the `g_` prefix
- Static variables use the `s_` prefix
- Local variables use lowercase underscore style

## Interrupt Functions

Interrupt handler functions should meet the following requirements:

- Names must include the `_irq_` or `_isr_` identifier
- Use specific modifiers to ensure correct calling conventions
- Avoid complex operations and blocking calls within interrupt functions
- Prefer the flag + main loop processing pattern whenever possible
