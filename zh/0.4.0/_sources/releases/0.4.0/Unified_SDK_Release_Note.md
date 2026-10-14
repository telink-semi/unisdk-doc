## V0.4.0(FR)

### Version
* SDK Version: unisdk V0.4.0
* Package Versions
  - MCU packages: B92 (TLSR922X/TLSR952X) 0.1.1, TL321X 0.1.1, TL721X 0.1.1
  - Modules: flashdb 0.1.1, mbedtls 0.1.1, tinyusb 0.1.1
  - All packages declare `sdk: "^0.4.0"`
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
* [Modular SDK / TLKPKG]
  - Introduced TLKPKG, the UniSDK package manager. The SDK is now split into a small core plus independently versioned packages: MCU packages (`packages/B92`, `packages/TL321X`, `packages/TL721X`) and modules (`modules/FlashDB`, `modules/mbedtls`, `modules/tinyUSB`).
  - MCU sources and the tinyUSB, Mbed TLS and FlashDB modules moved to their own repositories and are pulled in as submodules.
  - Added package versioning: the SDK version is defined in `version.yaml`, and each package declares its own version and the SDK range it is compatible with in `tlkpkg.yaml`.
  - Added package integrity checks on installation.
  - Added module autodiscovery: installed modules are found and added to the build automatically.
  - Module dependencies are now declared in each module's `dependency.yaml` instead of the West manifest.
  - Added per-package exporters (`export-all` command), packing of the Python scripts into the SDK, and the SDK/SRC split of exported trees.
* [Package Registry Server]
  - Added the package registry server with a sample registry, used to publish, list and download packages.
* [Git Publishing and Fallback]
  - Added publishing and fetching of packages through git: each package can be released as a tag in its own git repository.
  - Added a git fallback: when the TLKPKG server is unavailable, packages are installed directly from their git repositories. The VS Code extension uses the same fallback.
* [VS Code Extension]
  - Updated the UniSDK VS Code extension and prepared it for publishing: SDK management (several SDK installations, stored in a file instead of VS Code storage), separate SDK and SRC modes, package install and refresh from the sidebar, and a status refresh button.
  - Added the new project wizard: a new project is created outside the SDK from a sample, with its own Makefile and `.clangd` file.
* [Pinmux]
  - Added the pinmux GUI, including the board view and pin generation for a bare SoC when no board is selected.
* [Build System / Kconfig]
  - Added `prj.conf` support: each sample and project sets its Kconfig options in its own `prj.conf`.
  - External projects can now be built with `make`, outside the SDK tree.
  - Added the `GEN_ALL_BOARD_PROPERTIES` CMake option, which generates the properties of all boards of the selected SoC at build time.
  - Headers of disabled drivers are now checked: including a header whose driver is disabled in Kconfig reports an error.
  - On Windows, the Makefile now runs all configuration steps instead of CMake.
* [Toolchain]
  - Toolchain discovery now verifies the installed GCC version against the version required for the SoC series in `soc.yaml`.
* [MCUboot]
  - Added a recovery request through a RAM flag, so the application can ask the bootloader to enter recovery mode.
  - Updated the MCUboot bootloader sample and its README.
* [FlashDB]
  - Introduced the FlashDB module and the `flashdb_demo` sample.
* [Audio / USB]
  - Added a USB audio sample with microphone and speaker.
* [TLSR922X]
  - Updated the TLSR922X support in the B92 package.
* [CI]
  - The CI script now discovers all chips, samples and configs, and can be limited to specific SoC series or samples.
  - Added CI configs for most of the samples and refactored the memory report generator.

### Bug Fixes
* Critical Bugs：
  - [Build System]
    - Fixed the configure flow (`kconfig.cmake`) and the SDK exporter.
      - Impact Scope: Projects configured from an exported SDK tree.
      - Update Recommendation: Mandatory update for anyone exporting or building from an exported SDK.
    - Fixed a race condition in CMake that made CI builds fail.
* General Bugs：
  - [Kconfig]
    - Fixed the board selection, and the case where an empty board is selected.
    - Added Kconfig files missing from the default core installation.
  - [Registers]
    - Fixed the generation of the enum arrays in the register generator.
  - [Drivers]
    - Global variables that were exposed by the drivers are no longer visible outside their source files.
  - [Pinmux]
    - Fixed the pin selector, the pin layout and the pinmux dependencies.
  - [TLKPKG]
    - Application modules are now installed exactly into the `modules` folder.
    - The `ci_config` folder is no longer included when packing a package.
    - Fixed the package installers, the publish code and the missing installation directive for MCU packages.
    - Fixed the display of installed modules in SDK and SRC trees.
  - [Export]
    - Fixed the packing of the sources and the crypto library, the MCU export and the module export flow.
  - [New Project]
    - Fixed the Makefile of new projects.
  - [VS Code Extension]
    - Fixed the MCU package path, the Kconfig UI flow and the message shown when no MCU package is installed.
    - The sidebar is now refreshed after a package install or an SDK switch.
  - [CI]
    - Fixed the CI scripts for the new submodules and the samples build, and removed a broken pre-commit cache.

### BREAKING CHANGES
* Change Description: The SDK is now modular. MCU sources (`core/<CHIP>`) are no longer part of the main repository; they are installed as MCU packages under `packages/`. tinyUSB, Mbed TLS and FlashDB are installed as modules under `modules/`.
  - Impact Scope: Any project or script that references the old in-tree MCU or module paths, or that expects every chip to be present in the SDK.
  - Update Recommendation: Install the MCU packages and modules your project needs (VS Code extension or TLKPKG), and update path references to `packages/<CHIP>` and `modules/<MODULE>`.
* Change Description: Kconfig option names were standardized (`review(configs): Standardize config names`). Examples:
  - `TLK_UART0_ENABLED` → `TLK_UART0`, `TLK_GPIO_PORT_A_ENABLED` → `TLK_GPIO_PORTA`
  - `TLK_SYSTEM_TIMER_*` → `TLK_STIMER_*` (e.g. `TLK_SYSTEM_TIMER_IRQ_ENABLE` → `TLK_STIMER_IRQ`)
  - `TLK_CRITICAL_PRINTOUT` → `TLK_CRITICAL_PRINT`, `TLK_CRITICAL_UART*` → `TLK_CRITICAL_PRINT_UART*`
  - `TLK_DMA_IRQ_HANDLER` → `TLK_DMA_IRQ`, `TLK_CRYPTO_DMA_SUPPORT` → `TLK_CRYPTO_DMA`
  - `*_HAS_ENABLED_DEVICE` → `*_USE_DEVICE`, `*_AUTO_CONFIG` → `*_USE_AUTO_CONFIG`, `TLK_I2C_DMA` → `TLK_I2C_USE_DMA`
  - `*_NEST_SELECTED` → `*_USE_NEST`, `TLK_RANDOM_USED_PRNG/TRNG` → `TLK_RANDOM_USE_PRNG/TRNG`, `TLK_TRAP_ECALL_NESTING` → `TLK_TRAP_ECALL_NEST`
  - Impact Scope: Any `prj.conf`, defconfig, `build.config` or source code that uses the old option names.
  - Update Recommendation: Rename the options in your configuration files and in `#if CONFIG_...` checks.
* Change Description: Sample and project Kconfig options moved to `prj.conf`.
  - Impact Scope: Projects that set their options in other config files.
  - Update Recommendation: Move project options into the project's `prj.conf`.
* Change Description: The West manifest is no longer used for module dependencies; dependencies are declared in each module's `dependency.yaml`.
  - Impact Scope: Projects that pin module versions through the West manifest.
  - Update Recommendation: Use the module versions installed through TLKPKG.
* Change Description: Samples can no longer be built directly inside an installed SDK.
  - Impact Scope: Workflows that build samples in the SDK folder.
  - Update Recommendation: Create a project from the sample with the new project wizard and build it outside the SDK.

### Note
* Development Note: A package can only be installed into an SDK whose version matches the `sdk` range in the package's `tlkpkg.yaml` (`^0.4.0` for all packages in this release).
* Development Note: When the TLKPKG server is not reachable, packages are fetched from their git repositories. Git access to the package repositories is then required.

### CodeSize

Full CI memory report for all samples and configs built in this release (sizes in bytes): {download}`memory_report.log <memory_report.log>`

```{literalinclude} memory_report.log
:language: text
```
