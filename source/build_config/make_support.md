---
title: Make Support
status: STABLE
---

# Make Support

The UniSDK `Makefile` provides a traditional make command interface, serving as a CMake frontend to simplify build commands. **Can only be used at the project root directory.**

## Makefile Targets

| Target | Description | Command |
|--------|-------------|---------|
| `cmake` | Run CMake configuration | `make cmake` |
| `config` | Generate project configuration | `make config` |
| `pinmux` | Run Pinmux configuration tool | `make pinmux` |
| `build` | Full build (cmake + config + build) | `make build` |
| `clean` | Clean build artifacts | `make clean` |
| `cleanbuild` | Clean then rebuild | `make cleanbuild` |

## Makefile Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP` | `samples/gpio_demo` | Application path |
| `SOC` | (empty) | Target chip |
| `BOARD` | (empty) | Target development board |
| `BUILD_DIR` | `build` | Build directory |

## Usage Examples

```bash
# Default build
make build

# Specify application
make cmake build APP=samples/gpio_demo

# Specify chip and board
make cmake build SOC=TLSR9528A BOARD=TLSR9528A_EVK

# Specify application, chip, and board simultaneously
make cmake build APP=samples/gpio_demo SOC=TLSR9528A BOARD=TLSR9528A_EVK

# Clean and rebuild
make cleanbuild

# Configure only
make config
make pinmux
```

## Build Flow (make build)

1. **`cmake`** — Initialize the CMake build system for the specified application
2. **`config`** — Generate configuration files (`.config`, etc.)
3. **Pre-build checks** — 4 automatic check and recovery steps:
   - Check if the build directory exists
   - Check if the `.config` file exists
   - Check if `pinmux.h` exists
   - Check if `pinmux.h` is up to date
4. **`cmake --build`** — Execute Ninja compilation

## SOC/BOARD Parameter Forwarding

The Makefile automatically forwards SOC and BOARD variables to CMake:

```makefile
ifneq ($(SOC),)
CMAKE_FLAGS += -DSOC=$(SOC)
endif
ifneq ($(BOARD),)
CMAKE_FLAGS += -DBOARD=$(BOARD)
endif
```
