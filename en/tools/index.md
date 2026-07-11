---
title: Development Tools
status: STABLE
---

# Development Tools

UniSDK provides a series of development tools to simplify chip configuration, flashing/debugging, and code editing workflows.

| Tool | Description | Documentation |
|------|------|------|
| **BDT** | Telink Burning and Debugging Tool | [BDT Tool](bdt.md) |
| **Pinmux** | Graphical pin multiplexing configuration tool | [Pinmux Tool](pinmux.md) |
| **Menuconfig** | Terminal interactive system configuration interface | [Menuconfig](menuconfig.md) |
| **West** | Unified command-line entry point | [West Commands](../build_config/west_commands.md) |

## Tool Overview

```
Tool positions in the developer workflow:

  [Configuration Phase]              [Build Phase]                  [Flash/Debug Phase]
  ┌───────────────┐               ┌──────────────┐               ┌───────────────┐
  │  Menuconfig   │  ──►          │    CMake     │   ──►         │     BDT       │
  │   Pinmux      │               │    Ninja     │               │               │
  └───────────────┘               └──────────────┘               └───────────────┘
        │                                                                │
        └──────────────── West (tl-build) ───────────────────────────────┘
                     (Unified entry point)
```
