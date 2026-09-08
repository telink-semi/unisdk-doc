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

```{mermaid}
graph LR
    subgraph Config["Configuration Phase"]
        A[Menuconfig]
        B[Pinmux]
    end
    subgraph Build["Build Phase"]
        C[CMake]
        D[Ninja]
    end
    subgraph Flash["Flash / Debug Phase"]
        E[BDT]
    end
    A --> C
    B --> C
    C --> D
    D --> E
    C -.->|"West tl-build<br/>(unified entry)"| D
```
