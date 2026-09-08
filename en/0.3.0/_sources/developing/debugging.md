---
title: Debugging & Testing
status: STABLE
---

# Debugging & Testing

## Hardware Debugging

### Debugger Support

UniSDK supports the following debug interfaces:

| Debugger | Interface | Supported Platforms |
|--------|------|---------|
| **J-Link** | JTAG/SWD | All platforms |
| **Telink Debugger** | SWS (Single Wire) | All platforms |
| **BDT** | Flashing/Debugging | All platforms |

### Debugging Connection

1. Connect the debugger to the JTAG/SWS interface on the development board
2. Use GDB or an IDE for source-level debugging

## Software Debugging

### Logging System (Debug Print)

UniSDK has a built-in debug logging system that can be enabled via Kconfig:

```kconfig
# Enable debug logging
CONFIG_TLK_DEBUG_PRINT=y
CONFIG_TLK_DEBUG_PRINT_UART=0
CONFIG_TLK_DEBUG_PRINT_BUFFER_SIZE=256
```

Logs are output via UART and can be viewed in a serial terminal.

### Firmware Verification Script

```bash
# Verify firmware integrity
bash scripts/tl_check_fw.sh build/Telink.elf
```

## Performance Analysis

### Memory Usage Report

A memory usage summary is automatically output after compilation:

```
Memory region         Used Size  Region Size  %age Used
          RAM:        1234 B        64 KB      1.88%
         FLASH:       5678 B       512 KB      1.08%
```

### ELF Analysis

```bash
# Generate disassembly for analysis
riscv32-elf-objdump -d build/Telink.elf > disasm.txt

# View section sizes
riscv32-elf-size build/Telink.elf
```

## Debugging with GDB

```bash
# Start GDB server (using J-Link or Telink Debugger)
# Then connect the GDB client

riscv32-elf-gdb build/Telink.elf
(gdb) target remote :2331
(gdb) break main
(gdb) continue
```

## Common Debugging Tips

1. **LED Debugging** — Toggle LED state in critical code paths
2. **UART Output** — Output variable values via `TLK_DEBUG_PRINT`
3. **Assertion Checks** — Use assertions to catch abnormal states
4. **Memory Inspection** — Check the `.map` file to verify memory layout

## Next Steps

- [IDE Integration](ide_integration.md) — VS Code development environment configuration
- [Build & Configuration](../build_config/index.md) — Detailed build system documentation
