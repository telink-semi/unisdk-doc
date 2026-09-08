## V0.3.0(FR)

### Version
* SDK Version: unisdk V0.3.0
* Chip Version
  - TLSR952x
  - TL721x A2
  - TL321x A0/A1
* Hardware EVK Version
  - TLSR952x: C1T266A20
  - TL721x: C1T314A20
  - TL321x: C1T331A20/C1T335A20

* Toolchain Version
  - TL321X: TL32 ELF MCULIB V5 GCC14.2 (andes-riscv32-v5-gcc14.2)
  - TL721X/TLSR952X/TLSR922X: TL32 ELF MCULIB V5F GCC14.2 (andes-riscv32-v5f-gcc14.2)
  - Zephyr build (all series): Zephyr RISC-V64 SDK v0.17.0

<hr style="border-bottom:2.5px solid rgb(146, 240, 161)">

### Features
* [BLE Host]
  - Added BLE Host v2 project, build configuration, and sample application (`ble_host_demo`), including the SAL (Service Abstraction Layer) timers implementation and an enabled ACL data path.
  - Moved the SAL layer into the BLE host and split the BLE host module out into its own repository, integrated via West.
* [MCUboot]
  - Introduced MCUboot support, including a bootloader sample and its README/API documentation.
* [Build System / Kconfig]
  - Improved the Kconfig configuration flow and fixed several follow-on issues in the chip/build configuration generation.
  - `chip.config` generation now honors `SOC`/`BOARD` values passed on the CMake command line (e.g. `make cmake BOARD=TL3218X_EVK`), so the board/SoC can be preselected non-interactively instead of only through the interactive `menuconfig` UI.
  - Propagated the toolchain type (Andes / Zephyr) into `build.config`, and the cached toolchain path is now invalidated when the selected SoC series changes.
* [Toolchain]
  - Updated the Zephyr toolchain to v0.17.0.
  - Added automatic winget-based toolchain installation with a fallback path.
* [Drivers]
  - Added missing RF driver functions and DCOC/LDO_PLL/HPMC calibration and compensation support.
  - Implemented the advanced random driver for TL721X.
  - Added DMA driver improvements.
  - Reworked the i2s demo and added i2s support for TL321X.
  - Added common driver source files.
* [Logging]
  - Added hexdump support to the logger.
* [Security]
  - Added Mbed TLS support.
* [Linker / Binary]
  - Linker script no longer forces the LMA address of FLASH sections.
  - Added binary identification values (SDK/app version signature) for the debugger.
* [Samples]
  - Updated existing samples to support C++.

### Bug Fixes
* Critical Bugs：
  - [Build System]
    - Fixed the board selector so it works correctly when `SOC`/`BOARD` are passed on the command line — previously a first-time, non-interactive `chip.config` generation silently ignored these values and left the board unselected, causing configure-time Kconfig source failures.
      - Impact Scope: Any project first configuring a released/exported SDK tree (`DEV SDK mode`) with `-DBOARD=...`/`-DSOC=...` on the command line.
      - Update Recommendation: Mandatory update for anyone relying on command-line board/SoC selection instead of interactive `menuconfig`.
  - [Audio]
    - Fixed a linker issue affecting audio builds.
* General Bugs：
  - [Power Management]
    - Reduced power consumption and added tick resolution for sleep duration.
  - [SPI]
    - Increased SPI driver speed.
  - [USB]
    - Fixed typos left over from a prior renaming pass.
  - [System]
    - Fixed `sys_init` priority ordering.
  - [Logger]
    - Fixed an unused-parameter build error that occurred when the logger is disabled.
  - [mtimer]
    - Guarded mtimer source with the correct `#if` conditional.
  - [CI]
    - Fixed the Andes CI job build.
  - [Samples / BLE Host v2]
    - Removed an audio demo file that was added by mistake.
    - Fixed several coding-style issues in the BLE Host v2 demo.
    - Renamed `ble_host_v2_demo` to `ble_host_demo`.
    - Removed building applications from within the `ble_host_v2` module.
  - [Misc]
    - Fixed a typo in `core/common/src/tlk_plic.c`.
    - Removed excessive blank lines in `nv_storage_demo` logs.

### BREAKING CHANGES
* Change Description: The board-properties file path layout was changed (`refactor(properties): Change board properties path`).
  - Impact Scope: Any out-of-tree code or configuration referencing the old board-properties path.
  - Update Recommendation: Re-check board-properties references after upgrading; see the updated path layout in `boards/`.
* Change Description: `ble_host_v2_demo` was renamed to `ble_host_demo`, and the BLE host module now lives in a separate repository pulled in via West.
  - Impact Scope: Any project referencing the old `ble_host_v2_demo` sample name, or directly vendoring/pinning the BLE host sources in-tree.
  - Update Recommendation: Update sample references to `ble_host_demo` and update West manifest pins as needed.

### Note
* Development Note: The `SOC`/`BOARD` CMake cache variables only take effect the first time `chip.config` is generated. If `chip.config` already exists from a previous configure, delete it (or edit it directly) before re-running with new `SOC`/`BOARD` values.

### Royalty fee for certain Audio Codec:
* This SDK may include options for multiple audio codecs, it should be noted that use of certain Codecs may incur Royalty fees. It is the end product manufacturer's responsibility to sign license agreement with the license onwers and pay royalty fees. Telink as an IC provider cannot cover these charges.
* Use of LC3+ codec: If you choose to use LC3+ codec, please contact Fraunhofer/Ericsson (Fraunhofer IIS: lc3-licensing@iis.fraunhofer.de and Ericsson: lc3.licensing@ericsson.com) for proper license agreement and royalty fee information. A flat fee is charged by these License owners for product incorporating LC3+ codec. The royalty fee is open and transparent and charged per device (e.g. Headset, TV ,Box, …).
* Use of LC3 codec: LC3 usage is only free for product qualified as a Bluetooth product by Bluetooth SIG. If your product is not Bluetooth qualified and you choose to use LC3 codec, please contact Fraunhofer/Ericsson (Fraunhofer IIS: lc3-licensing@iis.fraunhofer.de and Ericsson: lc3.licensing@ericsson.com) for proper license agreement and royalty fee information. A flat fee is charged by these License owners for non-Bluetooth product incorporating LC3 codec. The royalty fee is open and transparent and charged per device (e.g. Headset, TV ,Box, …).

### CodeSize

`irq` is a new sample added in this release and has no v0.2.0 baseline to diff against (shown as "New"). `max_all` configs from v0.2.0 are no longer produced by the current sample set and are omitted below. Deltas are `(V0.3.0 - V0.2.0) / V0.2.0 * 100`.

| SOC | Sample | Config | Flash | Flash Δ% | RAM | RAM Δ% |
|---|---|---|---:|---:|---:|---:|
| TL321X | gpio | min | 8562 | +18.4% | 4173 | +0.0% |
| TL321X | gpio | suspend | 13108 | +16.2% | 4300 | +0.0% |
| TL321X | gpio | retention | 13952 | +14.9% | 4816 | +0.0% |
| TL321X | gpio | max | 13244 | +15.9% | 4348 | +0.0% |
| TL321X | irq | min | 17602 | New | 5356 | New |
| TL321X | irq | suspend | 21674 | New | 5508 | New |
| TL321X | irq | retention | 22518 | New | 6028 | New |
| TL321X | irq | max | 17602 | New | 5356 | New |
| TL321X | pm | suspend | 14912 | +117.4% | 4869 | +16.7% |
| TL321X | pm | retention | 14240 | +107.6% | 4869 | +16.7% |
| TL321X | pm | max | 14984 | +118.5% | 4869 | +16.7% |
| TL321X | uart | min | 13545 | +8.0% | 4355 | +3.7% |
| TL321X | uart | suspend | 17615 | +2.4% | 4507 | +1.8% |
| TL321X | uart | retention | 19131 | +2.4% | 5023 | +1.6% |
| TL321X | uart | max | 21115 | -2.3% | 4747 | +3.0% |
| TL721X | gpio | min | 11534 | +14.0% | 4173 | +0.0% |
| TL721X | gpio | suspend | 16032 | +12.9% | 4284 | +0.0% |
| TL721X | gpio | retention | 17240 | +12.2% | 4804 | +0.0% |
| TL721X | gpio | max | 16160 | +12.7% | 4364 | +0.0% |
| TL721X | irq | min | 20574 | New | 5368 | New |
| TL721X | irq | suspend | 24514 | New | 5524 | New |
| TL721X | irq | retention | 25722 | New | 6048 | New |
| TL721X | irq | max | 20574 | New | 5368 | New |
| TL721X | pm | suspend | 18136 | +85.8% | 4889 | +17.2% |
| TL721X | pm | retention | 17520 | +79.5% | 4889 | +17.2% |
| TL721X | pm | max | 18208 | +86.5% | 4889 | +17.2% |
| TL721X | uart | min | 16753 | +8.6% | 4367 | +4.0% |
| TL721X | uart | suspend | 20691 | +2.8% | 4523 | +1.8% |
| TL721X | uart | retention | 22515 | +2.8% | 5043 | +1.6% |
| TL721X | uart | max | 24347 | -0.6% | 4763 | +3.0% |
| TLSR952X | gpio | min | 8882 | +18.0% | 4180 | +0.0% |
| TLSR952X | gpio | suspend | 13932 | +15.0% | 4296 | +0.0% |
| TLSR952X | gpio | retention | 15224 | +13.6% | 4812 | +0.0% |
| TLSR952X | gpio | max | 14088 | +14.7% | 4376 | +0.0% |
| TLSR952X | irq | min | 17802 | New | 5372 | New |
| TLSR952X | irq | suspend | 22338 | New | 5536 | New |
| TLSR952X | irq | retention | 23630 | New | 6056 | New |
| TLSR952X | irq | max | 17802 | New | 5372 | New |
| TLSR952X | pm | suspend | 15920 | +121.9% | 4897 | +17.2% |
| TLSR952X | pm | retention | 15520 | +116.3% | 4897 | +17.2% |
| TLSR952X | pm | max | 15992 | +122.9% | 4897 | +17.2% |
| TLSR952X | uart | min | 14037 | +18.4% | 4371 | +4.0% |
| TLSR952X | uart | suspend | 18571 | +9.0% | 4535 | +1.8% |
| TLSR952X | uart | retention | 20263 | +8.4% | 5051 | +1.6% |
| TLSR952X | uart | max | 20839 | +5.0% | 4679 | +2.3% |
