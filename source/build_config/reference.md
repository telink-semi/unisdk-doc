---
title: File & Script Reference
status: STABLE
---

# File & Script Reference

## Core Configuration Files

| File | Location | Function |
|------|----------|----------|
| `CMakeLists.txt` | Repository root | CMake main entry point |
| `Makefile` | Repository root | Make command interface |
| `west.yml` | Repository root | West workspace configuration |
| `Kconfig.chip` | Repository root | Chip Kconfig entry point |
| `Kconfig.build` | Repository root | Build Kconfig entry point |

## Build Artifacts (build/ Directory)

| File | Description |
|------|-------------|
| `.config` | Final merged configuration |
| `chip.config` | Chip configuration |
| `build.config` | Build configuration |
| `autoconf.h` | C configuration macro definitions |
| `capabilities.h` | Chip capability declarations |
| `pinmux.h` | Pin multiplexing configuration |

## CMake Files

### Core Files

| File | Location | Function |
|------|----------|----------|
| `CMakeLists.txt` | Repository root | CMake main entry point |
| `TelinkConfig.cmake` | `cmake/` | Telink package configuration |
| `telink_default.cmake` | `cmake/modules/` | Module loading and default configuration |

### CMake Modules (cmake/modules/)

| Module | Function |
|--------|----------|
| `compiler.cmake` | RISC-V compiler configuration |
| `extensions.cmake` | CMake extension functions |
| `kconfig.cmake` | Kconfig integration |
| `linker.cmake` | Linker configuration |
| `pinmux.cmake` | Pin multiplexing configuration |
| `python.cmake` | Python environment configuration |
| `west.cmake` | West tool integration |
| `library.cmake` | Library build module |
| `headers_gen.cmake` | Header file generation |

## Build Scripts (scripts/)

| Script | Function |
|--------|----------|
| `kconfig.py` | Non-interactive Kconfig processing |
| `menuconfig.py` | Interactive configuration interface |
| `preprocess_kconfig.py` | Kconfig preprocessing |
| `kconfig_parser.py` | Kconfig parsing and validation |
| `soc_board_setter.py` | SOC/BOARD configuration |
| `tl_check_fw.sh` | Firmware verification |
| `set_telink_base.sh` | Set TELINK_BASE (Linux/Mac) |
| `set_telink_base.cmd` | Set TELINK_BASE (Windows CMD) |
| `set_telink_base.ps1` | Set TELINK_BASE (Windows PowerShell) |
| `windows_setup.ps1` | Windows automated environment setup |
| `sdk_exporter.sh` | SDK export script |

### West Command Implementations (scripts/west_commands/)

| Script | Corresponding Command |
|--------|-----------------------|
| `build.py` | `west tl-build` |
| `config.py` | `west tl-config` |
| `bdt.py` | `west tl-bdt` |
| `boards.py` | `west tl-boards` |
| `socs.py` | `west tl-socs` |
| `zcmake.py` | CMake helper |

### Pinmux Tools (scripts/pinmux/)

| File | Function |
|------|----------|
| `app.py` | Pinmux application core |
| `__main__.py` | CLI entry point |
| `data/` | Data processing modules |
| `ui/` | Terminal UI components |
| `styles.tcss` | UI stylesheet |

### CI Scripts (scripts/ci/)

| Script | Function |
|--------|----------|
| `ci_build.sh` | Single project CI build |
| `ci_build_all.sh` | All projects CI build |
| `ci_prepare.sh` | CI preparation |
| `defconfig_to_dotconfig.py` | defconfig to .config conversion |
| `dotconfig_to_defconfig.py` | .config to defconfig conversion |

## Kconfig Files

| File | Location | Function |
|------|----------|----------|
| `Kconfig.chip` | Repository root | Chip Kconfig entry point |
| `Kconfig.build` | Repository root | Build Kconfig entry point |
| `core/Kconfig` | `core/` | Core configuration |
| `core/configs/Kconfig` | `core/configs/` | Core feature configuration |
| `soc/Kconfig` | `soc/` | Chip series configuration |
| `boards/Kconfig` | `boards/` | Development board configuration |
| `api/Kconfig` | `api/` | API configuration |
| `samples/Kconfig` | `samples/` | Sample configuration |
