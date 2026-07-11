---
title: Analog Driver
status: STABLE
---

# Analog Driver

## Overview

The Analog driver provides raw access to chip analog registers and type-safe register field read/write macro definitions.

**Key Features:**

- Read/write analog registers by byte, half-word, and word
- YAML register descriptions converted to C type definitions
- Type-safe register read/write/modify macros

## API Reference

### C Functions

```c
// Analog register read/write
uint8_t  tlk_analog_read_reg8(uint8_t addr);
void     tlk_analog_write_reg8(uint8_t addr, uint8_t data);
uint16_t tlk_analog_read_reg16(uint8_t addr);
void     tlk_analog_write_reg16(uint8_t addr, uint16_t data);
uint32_t tlk_analog_read_reg32(uint8_t addr);
void     tlk_analog_write_reg32(uint8_t addr, uint32_t data);
```

These functions form the low-level transport layer, primarily used internally by the type-safe macros.

### Type-Safe Macros

To use these macros, include `registers/tlk_analog.h` with a complete analog register description. It contains named macros with corresponding addresses (e.g., `TLK_AREG_BG_CTRL0 -> 0x00`), which should be preferred over raw addresses.

If a register contains bitfields, a union type is generated:

```c
typedef union tlk_areg_bg_ctrl0 {
    struct {
        <bitfields>
    } bit;
    uint8_t raw;
} tlk_areg_0x00;
```

| Macro | Description |
|-------|------|
| `TLK_AREG_TYPE(reg)` | Expands to the C type for the named analog register |
| `TLK_AREG_SIZE(reg)` | Expands to the generated size constant for the register (in bits) |
| `TLK_ANALOG_READ(reg)` | Reads the register, casting the returned value to the register value type |
| `TLK_ANALOG_WRITE(reg, var)` | Writes a typed register value back to the register |
| `TLK_ANALOG_MODIFY(reg, statement)` | Reads, modifies, and writes back a typed register value |
| `TLK_ANALOG_MODIFY_RAW8(reg, statement)` | Modifies raw 8-bit register data using `uint8_t` |
| `TLK_ANALOG_MODIFY_RAW16(reg, statement)` | Modifies raw 16-bit register data using `uint16_t` |
| `TLK_ANALOG_MODIFY_RAW32(reg, statement)` | Modifies raw 32-bit register data using `uint32_t` |

## Register Definitions

Register definitions come from `core/*/registers/analog.yaml`, and type-safe C access macros are automatically generated via `registers_gen.py`.
