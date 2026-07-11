# UniSDK Handbook

**Telink Unified Software Development Kit — Developer Reference**

Version: 0.2.0-dev · Branch: `develop` · Date: 2026-07-03

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Getting Started](#3-getting-started)
4. [Build System](#4-build-system)
5. [Chip and Board Support](#5-chip-and-board-support)
6. [Peripheral Drivers](#6-peripheral-drivers)
   - 6.1 [GPIO](#61-gpio)
   - 6.2 [UART](#62-uart)
   - 6.3 [I2C](#63-i2c)
   - 6.4 [SPI](#64-spi)
   - 6.5 [ADC](#65-adc)
   - 6.6 [DMA](#66-dma)
   - 6.7 [Power Management (PM)](#67-power-management-pm)
   - 6.8 [Watchdog (WDT)](#68-watchdog-wdt)
   - 6.9 [Timer (STimer / MTimer)](#69-timer-stimer--mtimer)
   - 6.10 [USB](#610-usb)
   - 6.11 [PLIC — Interrupt Controller](#611-plic--interrupt-controller)
   - 6.12 [Analog Register Access](#612-analog-register-access)
   - 6.13 [PMP — Physical Memory Protection](#613-pmp--physical-memory-protection)
7. [Samples and Demos](#7-samples-and-demos)
8. [Tools](#8-tools)
9. [System Services](#9-system-services)
10. [Public API Layer](#10-public-api-layer)
11. [Configuration Reference](#11-configuration-reference)
12. [Directory Structure Reference](#12-directory-structure-reference)
13. [Troubleshooting](#13-troubleshooting)
14. [Glossary](#14-glossary)

---

## 1. Introduction

UniSDK (Unified Software Development Kit) is Telink's embedded software platform for the full range of RISC-V IoT SoC families. It provides a **single codebase, unified API, and modern build system** that works across chip families, allowing application code to be ported between chips with minimal changes.

### 1.1 Target Audience

- Chip customer R&D engineers developing IoT products on Telink SoCs
- FAE teams evaluating and supporting Telink hardware
- SDK developers extending the SDK with new drivers or chip support

### 1.2 What UniSDK Provides

| Capability | Details |
|---|---|
| Unified API | One set of `tlk_*` headers spans all chip families |
| Peripheral drivers | GPIO, UART, I2C, SPI, ADC, DMA, WDT, Timer, USB, PM, PLIC, PMP |
| Wireless | BLE controller integration; Proprietary RF |
| Security | Cryptographic hardware acceleration (TL321X, TL721X, TLSR952X) |
| Build system | CMake 3.20+ · Ninja · Kconfig · West · Make frontend |
| Tools | Menuconfig · Pinmux visual tool · BDT flash/debug utility |
| Samples | 15+ ready-to-compile demos covering every major subsystem |

### 1.3 Supported Chips and Boards

| Chip Family | Core | Boards |
|---|---|---|
| TL321X | RISC-V (TL321X core) | TL3218X\_EVK |
| TL721X | RISC-V (TL721X core) | TL7218X\_EVK |
| TLSR922X | RISC-V (B92 core) | TLSR9228A\_EVK |
| TLSR952X | RISC-V (B92 core) | TLSR9528A\_EVK · TLSR9528A\_DONGLE |

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                    │
│          (samples/  or your own application)            │
├─────────────────────────────────────────────────────────┤
│                   Public API Layer (api/)               │
│        tlk_sleep.h · tlk_time.h · tlk_api.h            │
├──────────────┬──────────────┬──────────────┬────────────┤
│  Core B92    │  Core TL321X │  Core TL721X │  ...       │
│  (core/B92/) │(core/TL321X/)│(core/TL721X/)│            │
│  Peripheral  │  Peripheral  │  Peripheral  │            │
│  drivers     │  drivers     │  drivers     │            │
├──────────────┴──────────────┴──────────────┴────────────┤
│                     SoC Layer (soc/)                    │
│   Chip-specific drivers · Pinmux · Registers · Crypto   │
├─────────────────────────────────────────────────────────┤
│               Optional Subsystems (modules/)            │
│           TinyUSB · BLE controller · ...                │
├─────────────────────────────────────────────────────────┤
│                      Hardware                           │
└─────────────────────────────────────────────────────────┘
```

### 2.1 Layer Responsibilities

**`api/`** — The outermost, stable API layer. Application code should include headers from here (`tlk_api.h`, `tlk_sleep.h`, `tlk_time.h`). This layer insulates application code from hardware differences.

**`core/<FAMILY>/`** — Per-chip-family peripheral drivers. Organized by hardware architecture (B92, TL321X, TL721X). Each family directory contains:
- `drivers/` — Peripheral driver implementations (.c files)
- `registers/` — Register definitions (YAML + generated .h)
- `properties/` — Device capability properties (YAML)

**`soc/<SERIES>/`** — Per-chip-series extensions on top of the core:
- `drivers/` — SoC-specific drivers (MSPI, OTP, etc.)
- `pinmux/` — Pin multiplexing YAML files per package variant
- `crypto/` — Hardware cryptographic acceleration
- `registers/` — SoC register additions

**`boards/<BOARD>/`** — Board-specific pin assignments (`board_pinout.yaml`).

**`modules/`** — Optional third-party integrations, conditionally included via Kconfig and `add_subdirectory()`. Currently: TinyUSB.

### 2.2 Config-Driven Selection

Chip, SoC series, and board are selected through the Kconfig system:

```
CONFIG_TLK_SOC_SERIES=TL321X
  └─> selects CONFIG_TLK_CORE=TL321X
  └─> sets include paths: core/TL321X · soc/TL321X · boards/<BOARD>
```

---

## 3. Getting Started

### 3.1 Prerequisites

- **OS:** Ubuntu 20.04+ / Windows 10+ / macOS 12+
- **Hardware:** One Telink EVK (e.g., TLSR9528A\_EVK)
- **Network:** Access to GitHub and PyPI for dependency installation

### 3.2 Install System Tools

**Linux (Ubuntu):**
```bash
sudo apt install --no-install-recommends git cmake ninja-build \
    python3-dev python3-venv python3-tk make
```

**Windows (PowerShell / winget):**
```powershell
winget install Kitware.CMake Ninja-build.Ninja Python Git.Git
```

**macOS:**
```bash
brew install cmake ninja python3 python-tk
```

### 3.3 Set Up Python Environment

```bash
cd unisdk

# Create virtual environment
python3 -m venv .venv          # Linux/macOS
python -m venv .venv           # Windows

# Activate
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\activate.ps1      # Windows PowerShell

# Install SDK Python dependencies
pip install -r requirements.txt
```

### 3.4 Initialize West

```bash
west init -l
```

> **Tip:** If you see `already initialized` errors because `ZEPHYR_BASE` points to another workspace:
> ```bash
> unset ZEPHYR_BASE && west init -l      # Linux/macOS
> Remove-Item Env:ZEPHYR_BASE; west init -l  # Windows PowerShell
> ```

### 3.5 Configure Toolchain

Download the Telink RISC-V GCC toolchain (V5.4.1+) from your Telink FAE, then:

```bash
# Linux/macOS
export TELINK_TOOLCHAIN_PATH=/path/to/toolchain

# Windows CMD
set TELINK_TOOLCHAIN_PATH=C:\toolchain

# Windows PowerShell
$env:TELINK_TOOLCHAIN_PATH = "C:\toolchain"
```

### 3.6 Build Your First Example

```bash
# Using West (recommended)
west tl-build samples/gpio_demo --board TLSR9528A_EVK

# Using Make
make build APP=samples/gpio_demo BOARD=TLSR9528A_EVK

# Using CMake directly
cmake -B build -G Ninja -DTelink_DIR=./cmake -S samples/gpio_demo
cmake --build build
```

### 3.7 Flash Firmware

```bash
west tl-bdt download --chip TLSR9528A -i build/gpio_demo.bin
```

---

## 4. Build System

UniSDK uses a layered build system: **West → Make → CMake + Ninja**, with **Kconfig** managing all compile-time options.

### 4.1 Build System Components

| Component | Role |
|---|---|
| **CMake 3.20+** | Core build system — project configuration, dependency management |
| **Ninja** | Fast parallel build executor (CMake backend) |
| **West** | Project management, custom build commands |
| **Kconfig** | Compile-time configuration management |
| **Make** | Convenience frontend for CMake commands |

### 4.2 West Commands

```bash
# Build a sample
west tl-build [source_dir] [--board BOARD] [--soc SOC]
west tl-build samples/gpio_demo --board TLSR9528A_EVK

# Interactive configuration (chip + build options)
west tl-config [source_dir]

# List supported chips
west tl-socs [-v]

# List supported boards
west tl-boards [-v] [--soc SOC]

# Flash and debug
west tl-bdt download --chip TLSR9528A -i build/app.bin
west tl-bdt read --chip TLSR9528A -a 0x00 -s 1k
west tl-bdt erase --chip TLSR9528A -a 0x00 -s 4k
```

### 4.3 Configuration System

UniSDK separates hardware configuration from build options:

**`Kconfig.chip`** — Selects chip family, SoC series, and board. Generates `chip.config`.

**`Kconfig.build`** — Selects features to enable (drivers, subsystems, Kconfig options). Generates `build.config`.

Both merge into `.config`, from which `autoconf.h` is generated for the compiler.

```bash
# Run interactive chip + build configuration
west tl-config

# Or manually
west tl-build --kconfig   # runs menuconfig then builds
```

### 4.4 Application CMakeLists.txt

Every application provides its own `CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.20.0)
find_package(Telink REQUIRED HINTS $ENV{TELINK_BASE})
project(MyApp LANGUAGES C)

file(GLOB C_SOURCES "*.c")
target_sources(Telink PRIVATE ${C_SOURCES})
```

The `find_package(Telink)` call loads `cmake/TelinkConfig.cmake`, which sets up the entire build infrastructure and discovers the selected chip's drivers.

### 4.5 Pinmux Configuration

Pin multiplexing is configured through the interactive pinmux tool:

```bash
# Launch pinmux GUI
west tl-config   # includes pinmux step

# Or run directly
python -m scripts.pinmux
```

The tool reads YAML pin definitions from `soc/<SERIES>/pinmux/` and generates `pinmux.h` into the build directory.

---

## 5. Chip and Board Support

### 5.1 Chip Families

#### TL321X

- **Core:** RISC-V (TL321X architecture)
- **Key peripherals:** GPIO, UART, I2C, SPI, ADC, DMA, PM, WDT, Timer
- **Security:** Hardware cryptographic acceleration (hash, PKE, SKE, TRNG)
- **Wireless:** BLE
- **Board:** TL3218X\_EVK

#### TL721X

- **Core:** RISC-V (TL721X architecture)
- **Key peripherals:** GPIO, UART, I2C, SPI, ADC, DMA, USB, PM, WDT, Timer
- **Security:** Hardware cryptographic acceleration (hash, PKE, SKE, TRNG)
- **Wireless:** BLE
- **Board:** TL7218X\_EVK

#### TLSR922X

- **Core:** RISC-V (B92 architecture)
- **Key peripherals:** GPIO, UART, I2C, SPI, ADC, PM, WDT, Timer
- **Wireless:** BLE
- **Board:** TLSR9228A\_EVK

#### TLSR952X

- **Core:** RISC-V (B92 architecture)
- **Key peripherals:** GPIO, UART, I2C, SPI, ADC, DMA, PM, WDT, Timer
- **Security:** Hardware cryptographic acceleration (hash, PKE, SKE, TRNG)
- **Wireless:** BLE
- **Boards:** TLSR9528A\_EVK · TLSR9528A\_DONGLE

### 5.2 Specifying Chip and Board at Build Time

```bash
# West
west tl-build samples/gpio_demo --soc TLSR9528A --board TLSR9528A_EVK

# CMake
cmake -B build -G Ninja -DTelink_DIR=./cmake -DSOC=TLSR9528A -DBOARD=TLSR9528A_EVK -S samples/gpio_demo

# Make
make build APP=samples/gpio_demo SOC=TLSR9528A BOARD=TLSR9528A_EVK

# Validate a combination first
west tl-config --validate TLSR9528A TLSR9528A_EVK
```

---

## 6. Peripheral Drivers

All UniSDK peripheral drivers follow a consistent programming model:

1. **Configure** — Set pin multiplexing and operating parameters (either via Kconfig auto-config or manual code)
2. **Use** — Call the driver API functions
3. **Deinitialize (optional)** — Disable the peripheral when done

The common header for all peripherals is `#include <tlk_api.h>`.

### Transfer Modes

Communication peripherals (UART, I2C, SPI, DMA) support multiple transfer modes:

| Mode | Description | Use Case |
|---|---|---|
| **Blocking** | Synchronous; waits with timeout | Simple, single-threaded code |
| **PLIC (Interrupt)** | Interrupt-driven; CPU-free during transfer | Power-efficient, responsive applications |
| **DMA** | Hardware DMA; zero CPU load during bulk transfer | High-throughput data transfer |

Mode is selected per peripheral instance via Kconfig.

---

### 6.1 GPIO

**Header:** `core/include/tlk_gpio.h`  
**Kconfig prefix:** `CONFIG_TLK_GPIO_*`

#### Overview

GPIO provides general-purpose digital I/O with support for input/output mode configuration, pull-up/pull-down resistors, pin multiplexing, and interrupt handling.

#### Enumerations

**`enum tlk_gpio_port`** — Port identifier, generated from `UNISDK_GPIO_PORT_COUNT` and enabled ports.  
Values: `GPIO_PORT_A`, `GPIO_PORT_B`, `GPIO_PORT_C`, ... (chip-specific)

**`enum tlk_gpio_pin`** — Pin bitmask within a port.

| Value | Description |
|---|---|
| `TLK_GPIO_PIN_NONE` | No pin (value 0) |
| `GPIO_PIN_0` … `GPIO_PIN_7` | Pin bitmasks (e.g., `GPIO_PIN_0 = BIT(0)`) |

**`enum tlk_gpio_mode`** — Pin mode.

| Value | Description |
|---|---|
| `TLK_GPIO_OUTPUT` | Digital output |
| `TLK_GPIO_INPUT_NO_PULL` | Floating input |
| `TLK_GPIO_INPUT_PULL_UP` | Input with pull-up |
| `TLK_GPIO_INPUT_PULL_DOWN` | Input with pull-down |

**`enum tlk_gpio_intr_trigger`** — Interrupt trigger.

| Value | Description |
|---|---|
| `TLK_GPIO_INTR_RISING_EDGE` | Rising edge |
| `TLK_GPIO_INTR_FALLING_EDGE` | Falling edge |
| `TLK_GPIO_INTR_HIGH_LEVEL` | High level |
| `TLK_GPIO_INTR_LOW_LEVEL` | Low level |
| `TLK_GPIO_INTR_BOTH_EDGE` | Both edges |

#### API Reference

```c
// Configure pin mode
void tlk_gpio_configure(enum tlk_gpio_port port, enum tlk_gpio_pin pin,
                        enum tlk_gpio_mode mode);

// Pin output control
void tlk_gpio_pin_write(enum tlk_gpio_port port, enum tlk_gpio_pin pin, bool value);
void tlk_gpio_pin_toggle(enum tlk_gpio_port port, enum tlk_gpio_pin pin);
bool tlk_gpio_pin_read(enum tlk_gpio_port port, enum tlk_gpio_pin pin);

// Pin multiplexing
void tlk_gpio_set_mux(enum tlk_gpio_port port, enum tlk_gpio_pin pin, uint8_t mux);

// Disable pin
void tlk_gpio_disable(enum tlk_gpio_port port, enum tlk_gpio_pin pin);

// Interrupt (requires CONFIG_TLK_PLIC)
void tlk_gpio_irq_configure(enum tlk_gpio_port port, enum tlk_gpio_pin pin,
                            enum tlk_gpio_intr_trigger trigger);
void tlk_gpio_irq_add_callback(enum tlk_gpio_port port,
                               struct tlk_gpio_irq_callback *callback);
```

#### Kconfig Options

```
CONFIG_TLK_GPIO_PORT_x_ENABLED     # Enable GPIO port x (x = A, B, C, ...)
CONFIG_TLK_GPIO_PREVENT_SLEEP      # Block sleep when GPIO is driving output
CONFIG_TLK_GPIO_PM_DEVICE          # GPIO power management support
```

#### Usage Example

```c
#include <tlk_api.h>

/* Toggle an LED every 500 ms */
void led_blink(void) {
    tlk_gpio_configure(GPIO_PORT_B, GPIO_PIN_4, TLK_GPIO_OUTPUT);
    while (1) {
        tlk_gpio_pin_toggle(GPIO_PORT_B, GPIO_PIN_4);
        tlk_sleep_ms(500);
    }
}

/* GPIO interrupt callback */
static struct tlk_gpio_irq_callback key_cb;

static void on_key_press(const struct tlk_gpio_irq_callback *cb) {
    tlk_gpio_pin_toggle(GPIO_PORT_B, GPIO_PIN_5);  // toggle LED1
}

void gpio_interrupt_example(void) {
    tlk_gpio_configure(GPIO_PORT_B, GPIO_PIN_5, TLK_GPIO_OUTPUT);
    tlk_gpio_configure(GPIO_PORT_C, GPIO_PIN_0, TLK_GPIO_INPUT_PULL_DOWN);
    key_cb.handler = on_key_press;
    tlk_gpio_irq_add_callback(GPIO_PORT_C, &key_cb);
    tlk_gpio_irq_configure(GPIO_PORT_C, GPIO_PIN_0, TLK_GPIO_INTR_RISING_EDGE);
    tlk_core_interrupt_enable();
}
```

---

### 6.2 UART

**Header:** `core/include/tlk_uart.h`  
**Kconfig prefix:** `CONFIG_UART{i}_*`

#### Overview

UART provides asynchronous serial communication with configurable baud rate, parity, stop bits, and optional hardware flow control. Each instance supports Blocking, PLIC (interrupt), and DMA transfer modes.

#### Enumerations

**`enum tlk_uart_module`** — UART instance, generated from `UNISDK_UART_COUNT`. Values: `UART0`, `UART1`, etc.

**`enum tlk_uart_parity`**

| Value | Description |
|---|---|
| `TLK_UART_PARITY_NONE` | No parity |
| `TLK_UART_PARITY_EVEN` | Even parity |
| `TLK_UART_PARITY_ODD` | Odd parity |

**`enum tlk_uart_stop_bit`**

| Value | Description |
|---|---|
| `TLK_UART_STOP_BIT_ONE` | 1 stop bit |
| `TLK_UART_STOP_BIT_ONE_DOT_FIVE` | 1.5 stop bits |
| `TLK_UART_STOP_BIT_TWO` | 2 stop bits |

**`enum tlk_uart_status`** — Return code for UART operations.

#### API Reference

```c
// Initialize UART
void tlk_uart_configure(enum tlk_uart_module uart_num, uint32_t baudrate,
                        enum tlk_uart_parity parity,
                        enum tlk_uart_stop_bit stop_bit);

// Configure TX/RX pins
void tlk_uart_configure_pinmux(enum tlk_uart_module uart_num,
                               struct tlk_gpio_port_pin tx_port_pin,
                               struct tlk_gpio_port_pin rx_port_pin);

// Send data (blocking, interrupt, or DMA depending on Kconfig)
enum tlk_uart_status tlk_uart_send_bytes(enum tlk_uart_module uart_num,
    const uint8_t *buff, uint32_t buff_size,
    tlk_uart_tx_handler_t tx_handler, uint32_t timeout_us);

// Receive data
enum tlk_uart_status tlk_uart_receive_bytes(enum tlk_uart_module uart_num,
    uint8_t *buff, uint32_t buff_size,
    tlk_uart_rx_handler_t rx_handler, uint32_t timeout_us);

// Flow control (requires CONFIG_TLK_UART_FLOW_CONTROL)
void tlk_uart_flow_configure(enum tlk_uart_module uart_num,
    enum tlk_uart_flow_control flow_control,
    enum tlk_uart_flow_polarity flow_polarity);
```

#### Transfer Modes

| Mode | Kconfig Value | Description |
|---|---|---|
| Blocking | `TLK_UART_XFER_BLOCKING` | Synchronous wait with timeout |
| Interrupt | `TLK_UART_XFER_PLIC` | Interrupt-driven |
| DMA | `TLK_UART_XFER_DMA` | DMA-driven, zero CPU overhead |

#### Kconfig Options

```
CONFIG_UART0_ENABLED                # Enable UART0 instance
CONFIG_UART0_AUTO_CONFIG            # Auto-configure from pinmux settings
CONFIG_UART0_BAUDRATE               # Baud rate (default 115200)
CONFIG_UART0_TX_MODE                # TX transfer mode
CONFIG_UART0_RX_MODE                # RX transfer mode
CONFIG_UART0_FLOW_CONTROL_TYPE      # Hardware flow control type
CONFIG_TLK_UART_FLOW_CONTROL        # Enable flow control support
```

#### Usage Example

```c
#include <tlk_api.h>

static volatile bool rx_done = false;
static uint8_t rx_buf[64];

static void rx_handler(enum tlk_uart_module uart, uint32_t bytes) {
    rx_done = true;
}

void uart_echo_example(void) {
    /* Manual configuration when auto-config is off */
    tlk_uart_configure(UART1, 115200,
                       TLK_UART_PARITY_NONE,
                       TLK_UART_STOP_BIT_ONE);

    tlk_core_interrupt_enable();

    while (1) {
        tlk_uart_receive_bytes(UART1, rx_buf, sizeof(rx_buf), rx_handler, 0);
        while (!rx_done) { /* wait */ }
        rx_done = false;
        tlk_uart_send_bytes(UART1, rx_buf, sizeof(rx_buf), NULL, 1000000);
    }
}
```

---

### 6.3 I2C

**Header:** `core/include/tlk_i2c.h`  
**Kconfig prefix:** `CONFIG_I2C{i}_*`

#### Overview

The I2C driver supports master/slave communication in blocking and DMA modes.

#### API Reference

```c
// Initialize I2C
void tlk_i2c_configure(enum tlk_i2c_module i2c_num, uint32_t speed_hz);

// Write to I2C device
enum tlk_i2c_status tlk_i2c_write(enum tlk_i2c_module i2c_num,
    uint8_t device_addr, const uint8_t *data, uint32_t len);

// Read from I2C device
enum tlk_i2c_status tlk_i2c_read(enum tlk_i2c_module i2c_num,
    uint8_t device_addr, uint8_t *data, uint32_t len);
```

#### Related Samples

- `samples/i2c_demo/ds1307/` — I2C communication with DS1307 RTC
- `samples/i2c_demo/ping_pong/` — I2C ping-pong transfer test

---

### 6.4 SPI

**Header:** `core/include/tlk_spi.h`  
**Kconfig prefix:** `CONFIG_SPI{i}_*`

#### Overview

The SPI driver supports master/slave communication in blocking and DMA modes.

#### API Reference

```c
// Initialize SPI
void tlk_spi_configure(enum tlk_spi_module spi_num, uint32_t speed_hz);

// SPI write
enum tlk_spi_status tlk_spi_write(enum tlk_spi_module spi_num,
    const uint8_t *data, uint32_t len);

// SPI read
enum tlk_spi_status tlk_spi_read(enum tlk_spi_module spi_num,
    uint8_t *data, uint32_t len);

// SPI full-duplex transfer
enum tlk_spi_status tlk_spi_transfer(enum tlk_spi_module spi_num,
    const uint8_t *tx, uint8_t *rx, uint32_t len);
```

---

### 6.5 ADC

**Header:** `core/include/tlk_adc.h`  
**Kconfig prefix:** `CONFIG_TLK_ADC_*`

#### Overview

The ADC (Analog-to-Digital Converter) driver supports blocking acquisition of single-ended and differential analog measurements.

#### API Reference

```c
// Configure ADC channel
void tlk_adc_configure(enum tlk_adc_channel ch, enum tlk_adc_ref_voltage ref);

// Read ADC sample (blocking)
uint16_t tlk_adc_read(enum tlk_adc_channel ch);

// Convert raw value to millivolts
uint32_t tlk_adc_raw_to_mv(uint16_t raw);
```

---

### 6.6 DMA

**Header:** `core/include/tlk_dma.h`  
**Kconfig prefix:** `CONFIG_TLK_DMA_*`

#### Overview

The DMA (Direct Memory Access) driver provides channel management and memory/peripheral transfer operations with zero CPU overhead during the transfer.

#### API Reference

```c
// Configure a DMA channel
void tlk_dma_configure(enum tlk_dma_channel ch,
                       const struct tlk_dma_config *config);

// Start a transfer
void tlk_dma_start(enum tlk_dma_channel ch,
                   uint32_t src, uint32_t dst, uint32_t len);

// Check if channel is done
bool tlk_dma_is_done(enum tlk_dma_channel ch);

// Register transfer-complete callback
void tlk_dma_set_callback(enum tlk_dma_channel ch,
                          tlk_dma_callback_t callback);
```

---

### 6.7 Power Management (PM)

**Header:** `core/include/tlk_pm.h`  
**Library:** `libtelink-unisdk-<SOC_SERIES>-pm.a` (conditional, `CONFIG_TLK_PM`)  
**Kconfig prefix:** `CONFIG_TLK_PM_*`

#### Overview

The PM driver controls the MCU power state. It supports three sleep modes with different power/wakeup trade-offs, configurable GPIO and timer wakeup sources, and before/after-sleep hooks for peripheral state management.

#### Sleep Modes

| Mode | Enum | Power | Wakeup Speed | SRAM Retained |
|---|---|---|---|---|
| Suspend | `TLK_PM_SLEEP_MODE_SUSPEND` | Medium | Fast | Yes (full) |
| Deep Sleep | `TLK_PM_SLEEP_MODE_DEEP_SLEEP` | Very Low | Slow (full reinit) | No |
| Deep Retention | `TLK_PM_SLEEP_MODE_DEEP_RETENTION` | Low | Medium | Partial |

#### Wakeup Sources

`enum tlk_pm_wakeup_source` — bitmask, combine with `|`:

| Value | Description |
|---|---|
| `TLK_PM_WAKEUP_SOURCE_PAD` | GPIO pin wakeup |
| `TLK_PM_WAKEUP_SOURCE_TIMER` | System timer wakeup |
| `TLK_PM_WAKEUP_SOURCE_CORE` | Core event wakeup |
| `TLK_PM_WAKEUP_SOURCE_COMPARATOR` | Comparator wakeup |

#### Sleep Return Codes

| Value | Meaning |
|---|---|
| `TLK_PM_SLEEP_OK` | Sleep completed, system resumed |
| `TLK_PM_SLEEP_TOO_SHORT` | Requested duration below minimum threshold |
| `TLK_PM_SLEEP_DENIED` | Sleep blocked by a peripheral (e.g., UART RX active) |

#### API Reference

```c
// Enter sleep
enum tlk_pm_sleep_status tlk_pm_sleep(enum tlk_pm_sleep_mode mode,
                                      uint32_t duration_us);

// Configure GPIO wakeup source
enum tlk_pm_sleep_status tlk_pm_set_gpio_wakeup(
    enum tlk_gpio_port port, enum tlk_gpio_pin pin,
    enum tlk_pm_gpio_wakeup_level polarity);

// Query last wakeup reason
enum tlk_pm_wakeup_source tlk_pm_get_wakeup_reason(void);

// Clear wakeup flags before next sleep
void tlk_pm_clear_wakeup_sources(void);
```

#### Kconfig Options

```
CONFIG_TLK_PM_SUSPEND_MIN_DURATION_MS          # Minimum suspend duration (default: 2 ms)
CONFIG_TLK_PM_DEEP_SLEEP_MIN_DURATION_MS       # Minimum deep sleep duration (default: 3 ms)
CONFIG_TLK_PM_DEEP_RETENTION_MIN_DURATION_MS   # Minimum retention duration (default: 3 ms)
CONFIG_TLK_PM_RETENTION_MEMORY_SIZE            # Bytes of SRAM to retain in Deep Retention
CONFIG_TLK_PM_RAM_RETENTION_ENABLE             # Enable retention memory support
```

#### Usage Example

```c
#include <tlk_api.h>

void power_management_example(void) {
    /* Configure GPIO C4 as high-level wakeup source */
    tlk_pm_set_gpio_wakeup(GPIO_PORT_C, GPIO_PIN_4,
                           TLK_PM_GPIO_WAKEUP_LEVEL_HIGH);

    /* Sleep for 5 seconds or until GPIO event */
    enum tlk_pm_sleep_status st =
        tlk_pm_sleep(TLK_PM_SLEEP_MODE_DEEP_SLEEP, 5000000);

    if (st == TLK_PM_SLEEP_OK) {
        enum tlk_pm_wakeup_source reason = tlk_pm_get_wakeup_reason();
        if (reason & TLK_PM_WAKEUP_SOURCE_PAD) {
            /* woken by GPIO */
        }
        tlk_pm_clear_wakeup_sources();
    }
}
```

---

### 6.8 Watchdog (WDT)

**Header:** `core/include/tlk_watchdog.h`  
**Kconfig prefix:** `CONFIG_TLK_WDT_*`

#### Overview

The Watchdog Timer driver monitors system health. If the application fails to reset (feed) the watchdog within the configured timeout, the device resets automatically.

#### API Reference

```c
// Initialize watchdog with timeout period (ms)
void tlk_wdt_configure(uint32_t timeout_ms);

// Enable (start) the watchdog
void tlk_wdt_enable(void);

// Feed (reset) the watchdog counter
void tlk_wdt_feed(void);

// Disable the watchdog
void tlk_wdt_disable(void);
```

#### Usage Example

```c
#include <tlk_api.h>

void watchdog_example(void) {
    tlk_wdt_configure(5000);   // 5-second timeout
    tlk_wdt_enable();

    while (1) {
        /* Application work */
        do_work();
        tlk_wdt_feed();        // Must be called within 5 seconds
    }
}
```

---

### 6.9 Timer (STimer / MTimer)

**Headers:** `core/include/tlk_stimer.h` · `core/include/tlk_mtimer.h`  
**Kconfig prefixes:** `CONFIG_TLK_STIMER_*` · `CONFIG_TLK_MTIMER_*`

#### STimer (System Timer)

The STimer is a free-running 32-bit system tick counter used for precise time measurement and delays.

```c
// Get current tick count
uint32_t tlk_stimer_get_tick(void);

// Get elapsed microseconds since reference tick
uint32_t tlk_stimer_get_elapsed_us(uint32_t ref_tick);

// Busy-wait delay
void tlk_stimer_delay_us(uint32_t us);
```

#### MTimer (Machine Timer)

The MTimer is the RISC-V standard machine-mode timer, used for periodic interrupt generation.

```c
// Configure and start machine timer interrupt (interval in us)
void tlk_mtimer_configure(uint32_t interval_us);

// Enable/disable MTimer interrupt
void tlk_mtimer_enable(void);
void tlk_mtimer_disable(void);
```

**Kconfig:** `CONFIG_TLK_MTIMER_IRQ_ENABLE` — Enable MTimer interrupt.

---

### 6.10 USB

**Header:** `core/include/tlk_usb.h`  
**Module:** `modules/tinyUSB/` (enabled by `CONFIG_TLK_USB`)  
**Kconfig prefix:** `CONFIG_TLK_USB_*`

#### Overview

USB support is provided through the TinyUSB stack integrated as an optional module. UniSDK provides Telink-specific port code in `modules/tinyUSB/port/`.

#### CDC (Virtual Serial Port) Example

```c
#include <tlk_api.h>
#include "tusb.h"

void usb_cdc_example(void) {
    /* TinyUSB is initialized automatically when CONFIG_TLK_USB is enabled */
    while (1) {
        tud_task();  /* TinyUSB main task */

        if (tud_cdc_available()) {
            uint8_t buf[64];
            uint32_t count = tud_cdc_read(buf, sizeof(buf));
            tud_cdc_write(buf, count);   /* echo back */
            tud_cdc_write_flush();
        }
    }
}
```

**Sample:** `samples/tinyusb_demos/usb_device/cdc_demo/`

---

### 6.11 PLIC — Interrupt Controller

**Header:** `core/include/tlk_plic.h`  
**Kconfig prefix:** `CONFIG_TLK_PLIC_*`

#### Overview

The PLIC (Platform-Level Interrupt Controller) manages all external interrupt sources. It supports configurable priorities, threshold-based masking, and optional interrupt preemption (nesting).

#### Interrupt Mode Selection

Selected at compile time via Kconfig:
- **General mode** — Single handler dispatches all interrupts
- **Vector mode** — Each interrupt source has a dedicated vector entry

#### API Reference

```c
// ISR registration macro
TLK_PLIC_ISR_REGISTER(my_handler, IRQ_UART0);

// Enable/disable interrupt source
void tlk_plic_interrupt_enable(uint32_t src);
void tlk_plic_interrupt_disable(uint32_t src);

// Set per-source priority
void tlk_plic_set_priority(uint32_t src, enum tlk_irq_priority priority);

// Set global threshold (only priorities > threshold are serviced)
void tlk_plic_set_threshold(enum tlk_irq_priority threshold);

// Claim/complete interrupt (used in General mode)
uint32_t tlk_plic_interrupt_claim(void);
void tlk_plic_interrupt_complete(uint32_t src);
```

#### Priority Levels

| Enum | Value | Description |
|---|---|---|
| `TLK_IRQ_PRI_LEV0` | 0 | Disabled (no interrupt generated) |
| `TLK_IRQ_PRI_LEV1` | 1 | Lowest priority |
| `TLK_IRQ_PRI_LEV2` | 2 | Medium |
| `TLK_IRQ_PRI_LEV3` | 3 | Highest priority |

#### Usage Example

```c
/* Register a UART0 interrupt handler */
TLK_PLIC_ISR_REGISTER(uart0_isr, IRQ_UART0);

void uart0_isr(void) {
    /* Handle UART0 interrupt */
}

void setup_uart_interrupt(void) {
    tlk_plic_set_priority(IRQ_UART0, TLK_IRQ_PRI_LEV2);
    tlk_plic_interrupt_enable(IRQ_UART0);
    tlk_core_interrupt_enable();
}
```

---

### 6.12 Analog Register Access

**Header:** `core/include/tlk_analog.h`

#### Overview

The Analog driver provides raw access to chip analog registers (used for analog bias, bandgap, oscillator configuration, etc.) and type-safe register field macros generated from YAML register descriptions.

#### API Reference

```c
// Byte-width read/write
uint8_t  tlk_analog_read_reg8(uint8_t addr);
void     tlk_analog_write_reg8(uint8_t addr, uint8_t data);

// Half-word read/write
uint16_t tlk_analog_read_reg16(uint8_t addr);
void     tlk_analog_write_reg16(uint8_t addr, uint16_t data);

// Word read/write
uint32_t tlk_analog_read_reg32(uint8_t addr);
void     tlk_analog_write_reg32(uint8_t addr, uint32_t data);
```

Type-safe macros are generated into `registers/tlk_analog.h` for each chip; use named constants rather than raw addresses.

---

### 6.13 PMP — Physical Memory Protection

**Header:** `core/include/tlk_pmp.h`  
**Kconfig prefix:** `CONFIG_TLK_PMP_*`

#### Overview

The PMP (Physical Memory Protection) driver configures RISC-V PMP entries to restrict memory access for privilege levels. It is used in combination with the user-mode execution framework to sandbox application code.

#### API Reference

```c
// Configure a PMP region
void tlk_pmp_configure(uint8_t entry, uint32_t addr, uint32_t size,
                       enum tlk_pmp_permissions perm,
                       enum tlk_pmp_addr_mode mode);

// Clear a PMP entry
void tlk_pmp_clear(uint8_t entry);
```

**Sample:** `samples/pmp_demo/`

---

## 7. Samples and Demos

All samples are in the `samples/` directory. Each has its own `CMakeLists.txt`, `Kconfig`, and `main.c`.

### Building Any Sample

```bash
west tl-build samples/<sample_name> --board <BOARD>
west tl-bdt download --chip <CHIP> -i build/<sample_name>.bin
```

### Sample Catalog

#### Basic Peripherals

| Sample | Directory | Key APIs | Notes |
|---|---|---|---|
| GPIO | `samples/gpio_demo` | `tlk_gpio_configure`, `tlk_gpio_pin_toggle`, GPIO IRQ | Supports interrupt demo via `CONFIG_TLK_GPIO_DEMO_INTERRUPT` |
| UART | `samples/uart_demo` | `tlk_uart_configure`, `tlk_uart_send_bytes`, `tlk_uart_receive_bytes` | Echo demo; sleep prevention test |
| Power Management | `samples/pm_demo` | `tlk_pm_sleep`, `tlk_pm_set_gpio_wakeup` | Deep/Suspend sleep; GPIO wakeup; retention variables |
| Watchdog | `samples/wdt_demo` | `tlk_wdt_configure`, `tlk_wdt_feed` | WDT reset demo |
| STimer | `samples/stimer_demo` | `tlk_stimer_get_tick`, `tlk_stimer_get_elapsed_us` | Precision timing demo |

#### Communication Interfaces

| Sample | Directory | Key APIs | Notes |
|---|---|---|---|
| ADC | `samples/adc_demo` | `tlk_adc_configure`, `tlk_adc_read` | Single-channel ADC measurement |
| DMA | `samples/dma_demo` | `tlk_dma_configure`, `tlk_dma_start` | Memory-to-memory transfer |
| I2C DS1307 | `samples/i2c_demo/ds1307` | `tlk_i2c_write`, `tlk_i2c_read` | RTC chip communication |
| I2C Ping-Pong | `samples/i2c_demo/ping_pong` | `tlk_i2c_*` | Two-device loopback test |
| SPI | `samples/spi_demo` | `tlk_spi_configure`, `tlk_spi_transfer` | SPI master/slave demo |
| USB CDC | `samples/tinyusb_demos/usb_device/cdc_demo` | TinyUSB CDC | Virtual serial port via USB |

#### System Features

| Sample | Directory | Key APIs | Notes |
|---|---|---|---|
| IRQ demo | `samples/irq_demo` | PLIC APIs | Interrupt nesting and priority demo |
| PMP demo | `samples/pmp_demo` | `tlk_pmp_configure` | Memory protection demo |
| User mode | `samples/umode_demo` | User-mode framework | RISC-V user-mode execution |
| RF demo | `samples/rf_demo` | RF APIs | Proprietary 2.4 GHz radio demo |
| BLE adv | `samples/adv_demo` | BLE controller API | BLE advertising demo |
| NV storage | `samples/nv_storage_demo` | NV storage API | Non-volatile key-value storage |
| System demo | `samples/system_demo/` | Task planner, log | System service demos |

### GPIO Demo — Detailed Walkthrough

```bash
# 1. Build
west tl-build samples/gpio_demo --board TLSR9528A_EVK

# 2. Enable interrupt demo (optional)
west tl-config samples/gpio_demo  # enable CONFIG_TLK_GPIO_DEMO_INTERRUPT in menuconfig

# 3. Flash
west tl-bdt download --chip TLSR9528A -i build/gpio_demo.bin

# Expected behavior:
# - LED0 (Port B, Pin 4) toggles every 1 second
# - If interrupt demo enabled: pressing KEY0 (Port C, Pin 0) toggles LED1
```

---

## 8. Tools

### 8.1 West Command Reference

```bash
# Build
west tl-build [APP_DIR] [-d BUILD_DIR] [--soc SOC] [--board BOARD]
              [-k] [--kconfig] [--clean] [--pristine auto|always|never]

# Configure
west tl-config [APP_DIR] [-d BUILD_DIR] [--list-socs] [--list-boards]
               [--validate SOC BOARD] [-c]

# Chip/board discovery
west tl-socs [-v]
west tl-boards [-v] [--soc SOC]

# Flash / debug
west tl-bdt download [--chip CHIP] [-i BIN] [-a ADDR] [--usb] [--bdt-path PATH]
west tl-bdt read    [--chip CHIP] [-a ADDR] -s SIZE [-o OUTPUT]
west tl-bdt write   [--chip CHIP] [-a ADDR] [-i FILE] [data...]
west tl-bdt erase   [--chip CHIP] [-a ADDR] -s SIZE
west tl-bdt lock    [--chip CHIP] [-a ADDR] [-s SIZE]
west tl-bdt unlock  [--chip CHIP]
west tl-bdt reset   [--chip CHIP]
```

### 8.2 Menuconfig

Interactive Kconfig UI for configuring chip selection, peripheral options, and build features:

```bash
# Full interactive configuration
west tl-config

# Script-level access
python scripts/menuconfig.py Kconfig.chip   # chip config
python scripts/menuconfig.py Kconfig.build  # build config
```

The tool presents a curses-based text UI where you can navigate options, set values, and save the configuration to `chip.config` / `build.config`.

### 8.3 Pinmux Visual Tool

The pinmux tool provides a graphical pin assignment editor based on the YAML pin definitions in `soc/<SERIES>/pinmux/`:

```bash
# Launch GUI (default)
python -m scripts.pinmux

# Generate pinmux.h non-interactively (CI/headless)
python -m scripts.pinmux --skip-gui
```

The tool reads `.config` to determine the chip series, presents available functions per pin, and generates `build/pinmux.h` consumed by the compiler.

### 8.4 BDT (Burning and Debugging Tool)

BDT is Telink's proprietary flash/debug utility, integrated through the `west tl-bdt` command.

**BDT path configuration (in priority order):**
1. `--bdt-path /path/to/bdt` command-line option
2. `BDT_PATH` environment variable
3. System PATH search
4. `$TELINK_BASE/tools/` directory

```bash
# Download with explicit path
west tl-bdt download --chip TLSR9528A \
     --bdt-path C:\BDT\Cmd_download_tool.exe \
     -i build/app.bin

# SWire clock settings for faster programming
west tl-bdt download --chip TLSR9528A \
     --sws 8000000 1 4000000 1 \
     -i build/app.bin
```

---

## 9. System Services

### 9.1 Task Planner

`system/` provides an optional cooperative task scheduler for dividing application logic into independent tasks.

**Sample:** `samples/system_demo/task_planner_demo/`

### 9.2 NV Storage

Non-volatile key-value storage for persisting configuration across power cycles.

**Sample:** `samples/nv_storage_demo/`

### 9.3 Logging

`system/debug/` provides printf-style logging with configurable output backends (UART, USB CDC, RTT).

**Sample:** `samples/system_demo/log_demo/`

### 9.4 User Mode Execution

The user-mode framework allows untrusted application code to run at RISC-V User privilege level while the SDK runs at Machine level. Combined with PMP, it provides spatial memory isolation.

**Sample:** `samples/umode_demo/`

---

## 10. Public API Layer

The `api/` directory provides the stable, chip-independent interface that application code should primarily use.

**`#include <tlk_api.h>`** — Umbrella header that pulls in all public APIs.

| Header | API | Description |
|---|---|---|
| `api/include/tlk_sleep.h` | `tlk_sleep_ms(ms)` · `tlk_sleep_us(us)` | Portable sleep/delay |
| `api/include/tlk_time.h` | `tlk_time_get_us()` · `tlk_time_elapsed_us(ref)` | Time measurement |

### Sleep API

```c
#include <tlk_api.h>

void delay_example(void) {
    tlk_sleep_ms(100);    // Sleep 100 milliseconds
    tlk_sleep_us(500);    // Sleep 500 microseconds
}
```

### Time API

```c
#include <tlk_api.h>

void timing_example(void) {
    uint32_t start = tlk_time_get_us();
    do_work();
    uint32_t elapsed = tlk_time_elapsed_us(start);
    // elapsed is now the duration of do_work() in microseconds
}
```

---

## 11. Configuration Reference

### 11.1 Core Kconfig Options

| Option | Default | Description |
|---|---|---|
| `CONFIG_TLK_SOC_SERIES` | — | SoC series: TL321X, TL721X, TLSR922X, TLSR952X |
| `CONFIG_TLK_CORE` | (derived) | Core family: B92, TL321X, TL721X |
| `CONFIG_TLK_BOARD` | — | Board: TLSR9528A\_EVK, TL3218X\_EVK, etc. |

### 11.2 GPIO Kconfig

```
CONFIG_TLK_GPIO                         # Enable GPIO driver
CONFIG_TLK_GPIO_PORT_A_ENABLED          # Enable Port A
CONFIG_TLK_GPIO_PORT_B_ENABLED          # Enable Port B
CONFIG_TLK_GPIO_PREVENT_SLEEP           # Prevent sleep if GPIO output active
CONFIG_TLK_GPIO_PM_DEVICE               # GPIO PM integration
```

### 11.3 UART Kconfig

Per-instance options (replace `{i}` with instance number 0, 1, 2, …):

```
CONFIG_UART{i}_ENABLED                  # Enable instance
CONFIG_UART{i}_AUTO_CONFIG              # Auto-apply pinmux settings
CONFIG_UART{i}_BAUDRATE                 # Baud rate
CONFIG_UART{i}_TX_MODE                  # TX mode: blocking/plic/dma
CONFIG_UART{i}_RX_MODE                  # RX mode: blocking/plic/dma
CONFIG_UART{i}_FLOW_CONTROL_TYPE        # RTS/CTS/none
```

### 11.4 Power Management Kconfig

```
CONFIG_TLK_PM                                   # Enable PM driver
CONFIG_TLK_PM_SUSPEND_MIN_DURATION_MS           # Min suspend duration
CONFIG_TLK_PM_DEEP_SLEEP_MIN_DURATION_MS        # Min deep sleep duration
CONFIG_TLK_PM_DEEP_RETENTION_MIN_DURATION_MS    # Min retention duration
CONFIG_TLK_PM_RETENTION_MEMORY_SIZE             # Retention SRAM bytes
CONFIG_TLK_PM_RAM_RETENTION_ENABLE              # Enable retention SRAM
```

### 11.5 Interrupt (PLIC) Kconfig

```
CONFIG_TLK_PLIC                         # Enable PLIC driver
CONFIG_TLK_PLIC_VECTOR_MODE            # Use vector interrupt mode
CONFIG_TLK_PLIC_NESTING               # Enable interrupt nesting
```

### 11.6 USB Kconfig

```
CONFIG_TLK_USB                          # Enable USB support (requires TinyUSB)
```

---

## 12. Directory Structure Reference

```
unisdk/
├── CMakeLists.txt              # Root CMake entry
├── Kconfig.chip                # Chip Kconfig root
├── Kconfig.build               # Build feature Kconfig root
├── west.yml                    # West workspace manifest
│
├── api/                        # Public API layer
│   ├── include/tlk_sleep.h
│   └── include/tlk_time.h
│
├── core/                       # Per-core-family peripheral drivers
│   ├── B92/drivers/            # Drivers for TLSR922X, TLSR952X
│   ├── TL321X/drivers/         # Drivers for TL321X
│   ├── TL721X/drivers/         # Drivers for TL721X
│   ├── include/                # Shared driver headers (tlk_gpio.h, tlk_uart.h, ...)
│   └── common/startup/         # RISC-V startup assembly and linker script
│
├── soc/                        # Per-SoC-series extensions
│   ├── TL321X/                 # TL321X: crypto, SoC drivers, pinmux YAML
│   ├── TL721X/
│   ├── TLSR922X/
│   └── TLSR952X/
│
├── boards/                     # Board pin assignments
│   ├── TL3218X_EVK/board_pinout.yaml
│   ├── TL7218X_EVK/board_pinout.yaml
│   ├── TLSR9228A_EVK/board_pinout.yaml
│   ├── TLSR9528A_EVK/board_pinout.yaml
│   └── TLSR9528A_DONGLE/board_pinout.yaml
│
├── common/                     # Shared utilities (linked lists, bit ops, etc.)
├── modules/tinyUSB/            # TinyUSB USB stack (optional)
├── system/                     # System services (task planner, NV storage, log)
│
├── samples/                    # Example applications
│   ├── gpio_demo/
│   ├── uart_demo/
│   ├── pm_demo/
│   ├── adc_demo/
│   ├── dma_demo/
│   ├── i2c_demo/
│   ├── spi_demo/
│   ├── stimer_demo/
│   ├── wdt_demo/
│   ├── pmp_demo/
│   ├── irq_demo/
│   ├── umode_demo/
│   ├── rf_demo/
│   ├── adv_demo/
│   ├── nv_storage_demo/
│   ├── system_demo/
│   └── tinyusb_demos/
│
├── cmake/                      # Build system infrastructure
│   ├── TelinkConfig.cmake      # Package entry point
│   └── modules/                # CMake modules (compiler, kconfig, linker, ...)
│
├── scripts/                    # Build and tool scripts
│   ├── west_commands/          # West extension commands
│   ├── pinmux/                 # Pinmux visual tool
│   ├── lib_builder/            # Prebuilt library builder
│   ├── sdk_exporter.sh         # Closed-source SDK export
│   └── ...
│
└── docs/                       # Documentation
    ├── HANDBOOK.md             # This document
    ├── RELEASE_NOTES.md
    └── en/                     # English documentation source
```

---

## 13. Troubleshooting

### `west init` fails with "already initialized"

The `ZEPHYR_BASE` variable points to another workspace. Fix:
```bash
unset ZEPHYR_BASE && west init -l          # Linux/macOS
Remove-Item Env:ZEPHYR_BASE; west init -l  # Windows PowerShell
```

### Compiler not found

Ensure `TELINK_TOOLCHAIN_PATH` points to the extracted RISC-V GCC toolchain directory containing `bin/riscv32-elf-gcc`.

### `tlk_pm_sleep` returns `TLK_PM_SLEEP_TOO_SHORT`

Increase the sleep duration above the minimum configured by `CONFIG_TLK_PM_*_MIN_DURATION_MS`, or lower the minimum threshold via Kconfig.

### `tlk_pm_sleep` returns `TLK_PM_SLEEP_DENIED`

A peripheral has flagged that sleep is unsafe (e.g., UART RX is active). Check whether `CONFIG_TLK_UART_DEMO_PREVENT` or similar "prevent sleep" options are enabled.

### Pinmux mismatch — peripheral not working after changing board

Rerun the pinmux tool to regenerate `pinmux.h` for the new board:
```bash
python -m scripts.pinmux
```
Or through West: `west tl-config`.

### Kconfig option not appearing in menuconfig

Check that the required parent option is enabled (e.g., `CONFIG_TLK_PLIC` is needed for GPIO interrupt options). Rebuild configuration from scratch with `west tl-build --pristine always`.

### Build fails after changing `SOC` or `BOARD`

Old config files can conflict. Use:
```bash
west tl-build --clean
# or
west tl-build --pristine always
```

---

## 14. Glossary

| Term | Definition |
|---|---|
| **API** | Application Programming Interface — the public headers in `api/include/` and `core/include/` |
| **BDT** | Burning and Debugging Tool — Telink's proprietary flash/debug utility |
| **Core** | The silicon IP used by a chip family (B92, TL321X, TL721X). One core may be shared by multiple SoC series. |
| **DMA** | Direct Memory Access — hardware data transfer without CPU involvement |
| **EVK** | Evaluation Kit — reference development board for a chip series |
| **Kconfig** | Configuration system (borrowed from Linux kernel) used to manage compile-time options |
| **MTimer** | Machine Timer — RISC-V standard timer used for periodic interrupt generation |
| **Ninja** | Fast parallel build executor used as CMake's backend |
| **PLIC** | Platform-Level Interrupt Controller — manages all external interrupt sources on RISC-V |
| **PM** | Power Management — system for controlling MCU power states and wakeup sources |
| **PMP** | Physical Memory Protection — RISC-V mechanism for restricting memory access by privilege level |
| **Pinmux** | Pin Multiplexing — assignment of hardware signals (UART TX, I2C SCL, etc.) to physical pins |
| **SoC** | System on Chip — the complete chip (e.g., TL321X, TLSR952X) |
| **STimer** | System Timer — free-running microsecond counter built on the chip's tick counter |
| **TinyUSB** | Open-source USB stack integrated as an optional module |
| **UART** | Universal Asynchronous Receiver/Transmitter — serial communication peripheral |
| **West** | Zephyr project management tool, extended by UniSDK with custom commands |
| **WDT** | Watchdog Timer — hardware counter that resets the MCU if not periodically fed |

---

*UniSDK Handbook — Telink Semiconductor · Apache License 2.0*
