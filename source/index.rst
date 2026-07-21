.. _unisdk-documentation:

##################################################
UniSDK — Telink Unified Software Development Kit
##################################################

.. only:: html

   .. rst-class:: lead

      UniSDK is Telink's unified software development platform, providing consistent development experience across all Telink chip series.
      SDK adopts modular, extensible architecture, integrating modern build tools like CMake, Ninja, West, and Kconfig,
      forming a complete compilation and build workflow. This documentation includes all user manuals, API references, and technical guides.

.. tip::
   **Document Status**: ``STABLE`` indicates content is complete and ready for use; ``DRAFT`` indicates content is under development.
   Issues and PRs are welcome to help improve documentation.

.. raw:: html

   <details>
   <summary><b>📚 Core Features (Click to expand)</b></summary>

- :octicon:`cpu` **Multi-Chip Unified Platform** — One codebase, one build system, covering TL321X / TL721X / TLSR922X / TLSR952X full chip series
- :octicon:`gear` **Modular Build System** — Flexible configuration based on CMake + Kconfig, supporting three build entry points: West / Make / CMake
- :octicon:`pulse` **Rich Peripheral Drivers** — Unified API layer providing full series peripheral drivers: GPIO, UART, I2C, SPI, ADC, DMA, USB, etc.
- :octicon:`broadcast` **BLE Protocol Stack** — Integrated BLE Controller, supporting flexible wireless connectivity applications
- :octicon:`sun` **Low Power Management** — Comprehensive power management framework, supporting multiple low power modes: Suspend / Retention, etc.
- :octicon:`graph` **Pinmux Visualization Tool** — Graphical pin multiplexing configuration, simplifying hardware design
- :octicon:`flame` **BDT Programming & Debugging** — One-click Flash programming, reading, erasing via ``west tl-bdt``

   </details>
   <br>

----------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   introduction/index
   getting_started/index
   getting_started/environment_setup
   getting_started/get_sdk
   getting_started/first_example
   getting_started/troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: Development Guide

   developing/index
   developing/setup_linux
   developing/setup_macos
   developing/setup_windows
   developing/blinky
   developing/directory_structure
   developing/project_management
   developing/core_architecture
   developing/init_hooks
   developing/public_api
   developing/debugging
   developing/ide_integration
   developing/clangd

.. toctree::
   :maxdepth: 2
   :caption: Chips & Boards

   chips_boards/index
   chips_boards/chips/TL321X
   chips_boards/chips/TL721X
   chips_boards/chips/TLSR922X
   chips_boards/chips/TLSR952X
   chips_boards/boards/TL3218X_EVK
   chips_boards/boards/TL7218X_EVK
   chips_boards/boards/TLSR9228A_EVK
   chips_boards/boards/TLSR9528A_EVK
   chips_boards/boards/TLSR9528A_DONGLE

.. toctree::
   :maxdepth: 2
   :caption: Peripherals & Drivers

   peripherals/index
   peripherals/gpio
   peripherals/uart
   peripherals/pm
   peripherals/analog
   peripherals/plic
   peripherals/i2c
   peripherals/spi
   peripherals/adc
   peripherals/dma
   peripherals/wdt
   peripherals/timer
   peripherals/usb
   peripherals/pmp

.. toctree::
   :maxdepth: 2
   :caption: Connectivity

   connectivity/index
   connectivity/ble/controller

.. toctree::
   :maxdepth: 2
   :caption: System Services

   system_services/index

.. toctree::
   :maxdepth: 2
   :caption: Build & Configuration

   build_config/index
   build_config/cmake_system
   build_config/kconfig_system
   build_config/west_commands
   build_config/make_support
   build_config/build_flow
   build_config/build_system_architecture
   build_config/extensions
   build_config/reference

.. toctree::
   :maxdepth: 2
   :caption: Development Tools

   tools/index
   tools/bdt
   tools/pinmux
   tools/menuconfig

.. toctree::
   :maxdepth: 2
   :caption: Security

   security/index

.. toctree::
   :maxdepth: 2
   :caption: Production Guide

   productization/index

.. toctree::
   :maxdepth: 2
   :caption: Samples & Demos

   samples/index
   samples/gpio
   samples/uart
   samples/pm
   samples/pmp
   samples/umode
   samples/adc
   samples/dma
   samples/i2c
   samples/spi
   samples/ble
   samples/irq_nesting
   samples/stimer
   samples/wdt
   samples/usb_cdc

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api_reference/index

.. toctree::
   :maxdepth: 2
   :caption: Reference

   kconfig_reference/index
   yaml_reference/index

.. toctree::
   :maxdepth: 2
   :caption: Community

   releases/index
   releases/0.2.0/Unified_SDK_Release_Note
   contribute/index
   support/index
   terminology
   about/index

.. only:: builder_html

   .. note::

      This documentation was built with **Sphinx**.
      The previous MkDocs-based build system has been replaced.
      See :doc:`contribute/index` for documentation contribution guidelines.
