---
title: Get and Import the SDK
status: STABLE
---

# Get and Import the SDK

## Get the SDK

Use Git to obtain the UniSDK:

```bash
git clone https://github.com/telink-semi/unisdk.git
cd unisdk
```

## SDK Directory Structure

After obtaining the SDK, the top-level directory structure is organized as follows:

```
unisdk/
├── api/             # Public API layer — unified API interfaces for application development
├── core/            # Core drivers — peripheral drivers organized by chip family
├── soc/             # SoC-specific layer — chip-specific features and drivers
├── boards/          # Development board configurations (pinmux, etc.)
├── common/          # Common libraries (linked lists, bit operations, etc.)
├── subsystem/       # Functional subsystems (e.g., BLE Controller)
├── modules/         # Third-party module integrations (e.g., TinyUSB)
├── samples/         # Example projects (gpio_demo, uart_demo, etc.)
├── cmake/           # CMake build system modules
└── scripts/         # Build scripts and tools (west commands, pinmux, etc.)
```

For a detailed explanation of each directory, see [SDK Directory Structure](../developing/directory_structure.md).

## Next Steps

After obtaining the SDK, proceed to [Compile, Flash and Run Your First Example](first_example.md).
