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
   :glob:

   introduction/index
   getting_started/*

.. toctree::
   :maxdepth: 2
   :caption: Development Guide
   :glob:

   developing/index
   developing/*

.. toctree::
   :maxdepth: 2
   :caption: Chips & Boards
   :glob:

   chips_boards/index
   chips_boards/chips/*
   chips_boards/boards/*

.. toctree::
   :maxdepth: 2
   :caption: Peripherals & Drivers
   :glob:

   peripherals/index
   peripherals/*

.. toctree::
   :maxdepth: 2
   :caption: Connectivity
   :glob:

   connectivity/index
   connectivity/*

.. toctree::
   :maxdepth: 2
   :caption: System Services
   :glob:

   system_services/*

.. toctree::
   :maxdepth: 2
   :caption: Build & Configuration
   :glob:

   build_config/index
   build_config/*

.. toctree::
   :maxdepth: 2
   :caption: Development Tools
   :glob:

   tools/index
   tools/*

.. toctree::
   :maxdepth: 2
   :caption: Security
   :glob:

   security/*

.. toctree::
   :maxdepth: 2
   :caption: Production Guide
   :glob:

   productization/*

.. toctree::
   :maxdepth: 2
   :caption: Samples & Demos
   :glob:

   samples/index
   samples/*

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   :glob:

   api_reference/*

.. toctree::
   :maxdepth: 2
   :caption: Reference
   :glob:

   kconfig_reference/*
   yaml_reference/*

.. toctree::
   :maxdepth: 2
   :caption: Community
   :glob:

   releases/*
   contribute/*
   support/*
   about/*
   terminology

.. only:: builder_html

   .. note::

      This documentation was built with **Sphinx**.
      The previous MkDocs-based build system has been replaced.
      See :doc:`contribute/index` for documentation contribution guidelines.
