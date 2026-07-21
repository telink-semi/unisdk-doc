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

:::{dropdown} SDK Top-Level Directory Structure
:summary: Click to expand/collapse

```text
unisdk/
├── api/             # Public API layer
├── core/            # Core peripheral drivers
├── soc/             # SoC-specific features and drivers
├── boards/          # Board configurations (pinmux, etc.)
├── common/          # Common libraries
├── subsystem/       # Functional subsystems (e.g., BLE Controller)
├── modules/         # Third-party module integrations (e.g., TinyUSB)
├── samples/         # Example projects
├── cmake/           # CMake build system modules
└── scripts/         # Build scripts and tools
```
:::

For a detailed explanation of each directory, see [SDK Directory Structure](../developing/directory_structure.md).

## Next Steps

After obtaining the SDK, proceed to [Compile, Flash and Run Your First Example](first_example.md).
