## V0.2.0(FR)

### Version
* SDK Version: unified_sdk V0.2.0
* Chip Version
  - TLSR952x(B92)
  - TL721x A2
  - TL321x A0/A1
* Hardware EVK Version
  - TLSR952x: C1T266A20
  - TL721x: C1T314A20
  - TL321x: C1T331A20/C1T335A20

* Toolchain Version
  - TLSR952x(B92)/TL721x/TL321x: TL32 ELF MCULIB V5 GCC12.2 ( IDE: [Telink IoT Studio](https://www.telink-semi.com/development-tools) )


#### Features

- PMP driver - Physical Memory Protection driver for RISC-V privilege enforcement (`feat(pmp)`)
- User-mode framework - Infrastructure for running untrusted application code in RISC-V User Mode (`feat/user mode`)
- Cryptography — Hardware crypto acceleration: hash, PKE, SKE, TRNG (`feat(cryptography)`)
- RF fast-settle - Fast RF settling mode for improved RF wake-up latency (`feat(rf): Add the fast settle feature`)
- RF reset functions - New `tlk_rf_reset()` family of functions (`feat(rf): Add the rf reset functions`)
- RF mode-switching demo - Sample demonstrating dynamic RF mode changes (`feat(rf): Add the mode switching demo`)
- Legacy toolchain env var - `TELINK_BASE_SDK` environment variable alias for backward compatibility (`feat(toolchain)`)
- IRQ nesting - Updated interrupt controller code supporting interrupt preemption (`feat(IRQ code)`)
- USB Universal API - Comprehensive USB driver with unified access interface and TinyUSB integration layer
- I2C Universal API - Complete I2C driver with unified driver structure for all MCUs
- SPI Universal API - SPI driver with Master support and Unified APIs for all supported SOCs
- Power API - Power-rail control API (`tlk_power.h`)
- DMA API - Expanded DMA driver with unified dynamic configuration
- PLIC API - Unified Interrupt controller with common API for all supported SOCs
- ADC API - Unified ADC API for all supported SOCs
- UART API - Unified UART API for al supported SOCs and 3 priority levels of message processing
- Logger subsystem - Debug Log for simplifying the user experience with formatting and sending the debug messages
- Multi-level init system - Support for different system init levels
- Task planner and loops - Simple multi-task queue with multi-threading or serial execution
- Software timer - Mtimer based multi-instance software timer
- NVS - non-volatile storage module
- YAML SoC descriptor

### Notes

A full English documentation set was added under `docs/en/`, covering:

- **Getting Started** — Linux, Windows, macOS setup; first-build walkthrough; troubleshooting
- **Introduction** — SDK positioning, architecture overview, chip family table
- **Chips & Boards** — Per-chip specs (TL321X, TL721X, TLSR922X, TLSR952X) and EVK board docs
- **Peripheral Drivers** — GPIO, UART, PM, PLIC, Analog, I2C, SPI, ADC, DMA, WDT, Timer, USB
- **Samples** — gpio, uart, pm, adc, dma, i2c, spi, BLE, IRQ nesting, timer, watchdog, USB CDC
- **Build System** — CMake flow, Kconfig system, West commands, Make support, extensions
- **Tools** — Menuconfig, Pinmux visual tool, BDT flash/debug utility
- **Development Guide** — Directory structure, public API design, core architecture, IDE integration, debugging
- **API Reference, Kconfig Reference, YAML Reference** — Scaffolding with index files
- **Connectivity** — BLE controller documentation stub
- **Terminology** — SDK-wide glossary

### CodeSize

| SOC | Sample | Config | Flash | RAM |
|---|---|---|---:|---:|
| TL321X | gpio | min | 7234 | 4173 |
| TL321X | gpio | suspend | 11280 | 4300 |
| TL321X | gpio | retention | 12140 | 4816 |
| TL321X | gpio | max | 11432 | 4348 |
| TL321X | gpio | max_all | 19812 | 5112 |
| TL321X | pm | suspend | 6858 | 4173 |
| TL321X | pm | retention | 6858 | 4173 |
| TL321X | pm | max | 6858 | 4173 |
| TL321X | pm | max_all | 19320 | 5112 |
| TL321X | uart | min | 12546 | 4199 |
| TL321X | uart | suspend | 17204 | 4427 |
| TL321X | uart | retention | 18688 | 4943 |
| TL321X | uart | max | 21604 | 4607 |
| TL321X | uart | max_all | 23732 | 5135 |
| TL721X | gpio | min | 10118 | 4173 |
| TL721X | gpio | suspend | 14202 | 4284 |
| TL721X | gpio | retention | 15362 | 4804 |
| TL721X | gpio | max | 14334 | 4364 |
| TL721X | gpio | max_all | 23106 | 5132 |
| TL721X | pm | suspend | 9762 | 4173 |
| TL721X | pm | retention | 9762 | 4173 |
| TL721X | pm | max | 9762 | 4173 |
| TL721X | pm | max_all | 22618 | 5132 |
| TL721X | uart | min | 15426 | 4199 |
| TL721X | uart | suspend | 20118 | 4443 |
| TL721X | uart | retention | 21906 | 4963 |
| TL721X | uart | max | 24490 | 4623 |
| TL721X | uart | max_all | 26906 | 5155 |
| TLSR952X | gpio | min | 7530 | 4180 |
| TLSR952X | gpio | suspend | 12116 | 4296 |
| TLSR952X | gpio | retention | 13400 | 4812 |
| TLSR952X | gpio | max | 12280 | 4376 |
| TLSR952X | gpio | max_all | 19160 | 5080 |
| TLSR952X | pm | suspend | 7174 | 4180 |
| TLSR952X | pm | retention | 7174 | 4180 |
| TLSR952X | pm | max | 7174 | 4180 |
| TLSR952X | pm | max_all | 18720 | 5080 |
| TLSR952X | uart | min | 11854 | 4203 |
| TLSR952X | uart | suspend | 17044 | 4455 |
| TLSR952X | uart | retention | 18688 | 4971 |
| TLSR952X | uart | max | 19848 | 4575 |
| TLSR952X | uart | max_all | 22140 | 5103 |
