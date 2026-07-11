# Analog Driver Documentation

## Overview
The analog driver provides raw access to analog registers and a set of register types plus type-safe macros for field access and modification.

**Key features**:
- Analog register read/write by byte, halfword, and word
- YAML register descriptions converted into C types
- Type-safe register read/write/modify macros

## API Reference

### C functions
The driver provides raw access to analog registers through these functions:

- `uint8_t tlk_analog_read_reg8(uint8_t addr)`
  - Read one byte from an analog register.
- `void tlk_analog_write_reg8(uint8_t addr, uint8_t data)`
  - Write one byte to an analog register.
- `uint16_t tlk_analog_read_reg16(uint8_t addr)`
  - Read a 16-bit halfword from an analog register.
- `void tlk_analog_write_reg16(uint8_t addr, uint16_t data)`
  - Write a 16-bit halfword to an analog register.
- `uint32_t tlk_analog_read_reg32(uint8_t addr)`
  - Read a 32-bit word from an analog register.
- `void tlk_analog_write_reg32(uint8_t addr, uint32_t data)`
  - Write a 32-bit word to an analog register.

These functions are the low-level transport layer mainly used by the macros.

### Type-safe macros

>**Important**: to take the most advantage of this feature, you need to have the language server capable of expanding deep macros, such as clangd. Then you will be able to fully use autocomplete, type hints, highlight, and so on.

To use these macros, you need to include registers/tlk_analog.h with a complete analog register description. It contains named macros with corresponding addresses (e.g., `TLK_AREG_BG_CTRL0 -> 0x00`), which should be preferred over raw addresses when using any analog driver API.  
Depending on the kind of register, the generation is different. If the register contains bitfields, the union type is generated, for example:
```c
typedef union tlk_areg_bg_ctrl0 {
    struct {
        <bitfields>
    } bit;
    uint8_t raw;
} tlk_areg_0x00;
```
If the register has no bitfields and is a part of a multibyte value, the macro with an iterator is generated (e.g., `TLK_AREG_WDT_INTERVAL(offset) -> TLK_AREG_WDT_INTERVAL(1) -> TLK_AREG_WDT_INTERVAL0 + 1`). It cannot have a type, so it doesn't work with the type-safe macros.

- `TLK_AREG_TYPE(reg)`
  - Expands to the C type for the named analog register, for example `TLK_AREG_TYPE(TLK_AREG_BG_CTRL0) -> tlk_areg_0x00`.
  - This macro is mainly used internally by other macros and is normally not needed in application code. Instead, use the named type directly, such as `union tlk_areg_bg_ctrl0`.
- `TLK_AREG_SIZE(reg)`
  - Expands to the generated size constant for the register (in bits), such as `TLK_AREG_SIZE(TLK_AREG_BG_CTRL0) -> TLK_AREG_0x00_SIZE -> 8`.
  - Used by other macros to select the appropriate raw types and functions.
- `TLK_ANALOG_READ(reg)`
  - Reads the register, casting the returned value to the register value type.
- `TLK_ANALOG_WRITE(reg, var)`
  - Writes a typed register value back to the register.
- `TLK_ANALOG_MODIFY(reg, statement)`
  - Reads the typed register value into a local `value` variable, executes the provided statement to modify it, and writes the updated raw value back.
  - The statement should be provided in braces.
  - Use this macro to update fields of the register type safely.
- `TLK_ANALOG_MODIFY_RAW8(reg, statement)`
  - Modifies raw 8-bit register data using `uint8_t`.
  - The statement should be provided in braces.
- `TLK_ANALOG_MODIFY_RAW16(reg, statement)`
  - Modifies raw 16-bit register data using `uint16_t`.
  - The statement should be provided in braces.
- `TLK_ANALOG_MODIFY_RAW32(reg, statement)`
  - Modifies raw 32-bit register data using `uint32_t`.
  - The statement should be provided in braces.

> Note: Internal helper macros in the header begin with underscores and are not intended for user code.
