---
title: IDE Integration
status: STABLE
---

# IDE Integration

## VS Code Configuration (Recommended)

### clangd Language Server

clangd is an LLVM/Clang-based C/C++ language server that understands UniSDK's complex macro definitions and configuration system, providing:

- Intelligent code completion
- Go to definition
- Find references
- Semantic highlighting
- Code navigation
- Inline diagnostics
- Rename refactoring

#### Why Choose clangd?

UniSDK makes extensive use of Kconfig-generated configuration macros (`autoconf.h`, `capabilities.h`) and cross-compilation. Ordinary syntax highlighting cannot correctly parse these macros, leading to false error reports and navigation failures. clangd solves this problem by reading `compile_commands.json`.

#### Installation Steps

1. Install **clangd** (publisher: LLVM) from the VS Code extension marketplace
2. Disable the Microsoft C/C++ IntelliSense engine to avoid conflicts:
   - `Ctrl+Shift+P` → `Preferences: Open Settings (UI)` → Extensions → C/C++ → IntelliSense
   - Set `IntelliSenseEngine` to `disabled`

#### Key Files

**`compile_commands.json`**

Automatically generated in the `build/` directory by CMake during the build. clangd reads this file to understand the project's compilation options.

```json
[
  {
    "file": "main.c",
    "command": "riscv32-elf-gcc -I/path/to/include -DCONFIG_DEBUG ...",
    "directory": "/project/build"
  }
]
```

**`.clangd`** (Optional configuration at project root)

```yaml
CompileFlags:
  Add:
    - -Wall
    - -Wextra

Diagnostics:
  Suppress:
    - unused-parameter
```

#### Common Issues

**Files Display Incorrectly After Switching to a Different Chip**

clangd provides semantic analysis based on the current build's `compile_commands.json`. If the project was previously built for TL321X, files for TL721X will not be correctly parsed.

**Solution**: Rebuild the project with the target chip.

**Warnings Still Present After a Recent Rebuild**

File indexing happens lazily and needs a manual trigger to update.

**Solution**: Edit and save the target file to force an update.

### Recommended Extensions

| Extension | Purpose |
|------|------|
| clangd | C/C++ language server |
| CMake Tools | CMake project support |
| Cortex-Debug | ARM/RISC-V debugging |
| GitLens | Git enhancements |
| Error Lens | Inline error display |

## Eclipse Configuration

1. Install Eclipse CDT and the RISC-V GCC plugin
2. Import the project as "Existing CMake Project"
3. Configure the cross-compilation toolchain path

## Segger Embedded Studio

1. Import the project via File → Open Solution
2. Configure the debugger as J-Link
3. Set the target device to Telink RISC-V chip

## Next Steps

- [Project Creation & Management](project_management.md) — Create new projects
- [Debugging & Testing](debugging.md) — Debugging tips
