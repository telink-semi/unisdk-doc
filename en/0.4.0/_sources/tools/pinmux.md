---
title: Pinmux Pin Configuration Tool
status: STABLE
---

# Pinmux Pin Configuration Tool

## Overview

The Pinmux (Pin Multiplexing) tool is a graphical pin configuration tool provided by UniSDK to help developers visually configure chip pin multiplexing functions in the terminal.

**Key Features:**

- Graphical terminal interface (based on the Textual framework)
- Visual selection of pin functions with interactive popup menus
- Pin configuration conflict detection
- Requirement validation (ensures all required functions are assigned)
- Support for multiple chip package variants
- Integration with the Kconfig configuration system
- Automatic generation of the `pinmux.h` header file

## Launch Methods

```bash
# Method 1: Via CMake target
make pinmux

# Method 2: Direct Python module invocation
python -m scripts.pinmux

# Method 3: Skip GUI, generate default configuration
python -m scripts.pinmux --skip-gui
```

## Main View

Once opened, you will see the main dashboard:

- **Ports:** A scrollable vertical list of all GPIO ports (e.g., PORT A, PORT B)
- **Pins:** Inside each port section, individual pins are displayed as interactive buttons showing the pin's name and its currently assigned function

![Pinmux Interface overview](pics/pinmux_1.png)
*Figure 1. Pinmux Interface overview showing GPIO ports, pins, and assigned functions.*

## Selecting a Function

1. Click on a pin (or navigate to it and press **Enter**)
2. A popup window titled **Function Select** will appear
3. The list shows all supported hardware functions for that specific pin
4. Select the desired function (e.g., `UART0_RX`) or select **NONE** to disable the pin
5. Press **Enter** to confirm

![Function select screen](pics/pinmux_2.png)
*Figure 2. Function select screen for a GPIO pin.*

## Shortcuts

| Key | Action |
|-----|--------|
| **s** (Save) | Validates configuration — checks for conflicts and missing functions. If valid, saves and exits. If invalid, shows an error notification |
| **q** (Quit) | Exits the application. A confirmation dialog appears if there are unsaved modifications |

Validation errors occur when:
- Necessary functions are not assigned to pins (e.g., UART0 is enabled but UART0_TX is not assigned)
- Conflicting pins exist (e.g., UART0_TX assigned to both PC3 and PC4)

![Exit Screen](pics/pinmux_3.png)
*Figure 3. Exit Screen.*

## Saving

The configuration is saved to a file named `<SoC or board name>.<soc or board>.pinmux`. For example, building for TL3218X_EVK generates `TL3218X_EVK.board.pinmux`.

This `.pinmux` file contains pin-to-function mappings in a human-readable format and is used to restore previous pin settings when the tool is invoked again.

Additionally, `pinmux.h` is generated in the build folder based on the saved settings, containing C preprocessor definitions usable by firmware code.

The `.pinmux` files persist until the project switches, allowing previous pin settings to be restored when switching between chips.

## File Format

The `.pinmux` files use a simple key-value format:

```
PC4=UART0_TX
PB2=UART0_RX
PA0=GPIO_OUTPUT
```

- Each line represents a single pin assignment
- All letters are upper-case
- Format: `<pin name>=<function name>`
- Pin name consists of letter **P**, port letter, and pin number

During parsing, the following lines are ignored:
- Invalid data that doesn't match the pattern
- Valid data referencing non-existent pins or functions
- Assignments to pins on ports disabled in the current configuration
- Assignments to functions not enabled in the current configuration

## Overriding Mechanism

Each time pinmux is invoked, data is loaded in the following sequence (each overrides the previous):

1. **SoC defaults** — from `soc/<soc>/pinmux/function.yaml` (used for development)
2. **Project `.pinmux`** — in the project directory (sets custom defaults for any chip)
3. **`<identifier>.pinmux`** — in the project directory (chip-specific overrides)
4. **`<identifier>.pinmux`** — in the build directory (last actual user pin settings)

This allows projects to have out-of-the-box pin settings while still allowing customization.

## Internal Execution Flow

### Data Loading & Synchronization

When the application starts, it combines multiple data sources:

- `soc/<soc>/pinmux/function.yaml` — The "Function Definitions": describes all available functions for the chip
- `soc/<soc>/pinmux/pinmux.yaml` — The "Dictionary": lists every physical pin and its supported functions. Each port can have an `exclude` property, which describes what functions aren't supported by its pins. Individual pins can also use `exclude` and `include` properties. The restrictions are applied in the following order: port's exclude → pin's exclude → pin's include. For simplicity, the `all` keyword represents all functions. For groups of functions, you may use a group name (e.g., `uart0` represents `uart0_tx`, `uart0_rx`, `uart0_cts`, and `uart0_rts`; `uart` covers `uart0`, `uart1`, etc.). If a pin supports only one exact function, use `exclude: all` together with `include: your_function`.
- `soc/<soc>/pinmux/pinmux_<case>.yaml` — The "Restriction": overrides `pinmux.yaml` to remove pins or ports for specific chip packages by assigning the `delete` keyword
- `.config` — The "Requirements": tells the app which drivers are enabled (e.g., "UART0 is enabled, so we need pins for TX and RX")
- `.pinmux` files — Previous user configurations (see overriding mechanism)

**The Loading Sequence:**

1. The `.config` file, which contains the current configuration and identifies the current chip.
2. The function description from `function.yaml`, skipping functions disabled by configuration.
3. The port and pin description from `pinmux.yaml` and `pinmux_<case>.yaml` for the selected chip.
4. The `.pinmux` files in the order described in the [Overriding Mechanism](#overriding-mechanism) section.

### Changing a Pin Function

When a new function is selected for a pin, the following happens instantly:

- **Collision Check:** The system scans all other pins. If you try to assign a unique function (like `UART0_TX`) to PC0, but PB2 already has it, the system flags a **Conflict**.
- **Observer Update:** The app uses an "Observer Pattern."
  - The Pin data changes.
  - The UI widget receives a notification and redraws itself (updating the text and color).
  - The next `is_modified` property access in `PinmuxManager` will return `True`, until the save action is triggered.

### The Saving Process

When you press Save (`s`), the app performs strict validation before writing to disk.

**Step 1: Validation**

- **Check Conflicts:** Are two pins assigned to the same non-repeatable function? If yes → Error.
- **Check Requirements:** Are all functions required by the configuration assigned to valid pins? If no → Error.

**Step 2: Writing**

- If there are no errors, the pin mapping is saved to the `<identifier>.pinmux` file using the simple key-value format.

### Generating pinmux.h

After saving, `pinmux.h` is automatically generated with C preprocessor definitions:

```c
#define PINMUX_UART0_TX_PORT TLK_GPIO_PORT_C
#define PINMUX_UART0_TX_PIN TLK_GPIO_PIN_4
#define PINMUX_UART0_RX_PORT TLK_GPIO_PORT_B
#define PINMUX_UART0_RX_PIN TLK_GPIO_PIN_2
#define PINMUX_GPIO_OUTPUT_0_PORT TLK_GPIO_PORT_A
#define PINMUX_GPIO_OUTPUT_0_PIN TLK_GPIO_PIN_0
#define PINMUX_GPIO_OUTPUT_COUNT 1
```

## Configuration File Locations

:::{dropdown} Pinmux Configuration Files
:summary: Click to expand/collapse

```text
soc/<chip>/pinmux/
├── function.yaml          # Pin function definitions
├── pinmux.yaml            # Pin multiplexing configuration
├── pinmux_qfn48.yaml      # QFN48 package
├── pinmux_qfn88.yaml      # QFN88 package
└── ...
```
:::

## Build Integration

Pinmux configuration is deeply integrated into the build system:

- The `generate_pinmux` CMake target automatically executes before compilation
- Pre-build checks automatically detect whether `pinmux.h` needs to be updated
- The generated `pinmux.h` is placed in the `build/` directory and automatically added to the include path

## CI

The CI uses a single configuration across all samples. This is possible because unused assignments are skipped, so you just need to consider all pin usages in the samples within this file. Before the build, the CI copies this file to the build directory. Since the build's settings are applied last during overriding, the resulting configuration corresponds to what is described in the file — all previous settings are overridden.
