---
title: Kconfig Configuration System
status: STABLE
---

# Kconfig Configuration System

Kconfig is the configuration management core of UniSDK, using a hierarchical structure to manage compile-time configuration options.

## Architecture

### Configuration Entry Points

UniSDK uses a dual-entry Kconfig design:

```
Kconfig.chip     → Chip-related configuration (SoC selection, peripheral enabling)
Kconfig.build    → Build-related configuration (feature options, parameter settings)
```

### Hierarchy

```{mermaid}
graph TD
    subgraph Entry["Configuration Entry Points"]
        KC[Kconfig.chip<br/>Chip configuration]
        KB[Kconfig.build<br/>Build configuration]
    end

    subgraph ChipInc["Included by Kconfig.chip"]
        CORE[core/Kconfig<br/>Core configuration]
        SOC[soc/Kconfig<br/>Chip series]
        BRD[boards/Kconfig<br/>Boards]
    end

    subgraph BuildInc["Included by Kconfig.build"]
        API[api/Kconfig<br/>API config]
        CFG[core/configs/Kconfig<br/>Core features]
        SMP[samples/Kconfig<br/>Samples]
        SYS[system/Kconfig<br/>System]
    end

    KC --> CORE
    KC --> SOC
    KC --> BRD
    KB --> API
    KB --> CFG
    KB --> SMP
    KB --> SYS
```

### Application-Level Kconfig Integration

Through the `KCONFIG_APPLICATION_DIR` variable, the application layer can define its own Kconfig options, seamlessly integrating with the SDK configuration.

## Configuration Generation Flow

```{mermaid}
graph LR
    subgraph Input["Kconfig Sources"]
        A[Kconfig.chip]
        A2[Kconfig.build]
    end

    subgraph Gen["Generated Configs"]
        B[chip.config]
        E[build.config]
    end

    subgraph Output["Final Outputs"]
        D[capabilities.h]
        I[autoconf.h]
    end

    A --> B
    A2 --> E
    B --> C[preprocess_kconfig.py]
    C --> D
    E --> F[Merge]
    B --> F
    F --> G[.config]
    G --> H[kconfig.py parsing]
    H --> I
```

### Key Configuration Files

| File | Source | Description |
|------|--------|-------------|
| `chip.config` | Kconfig.chip | Chip-related configuration (SoC, peripheral enabling) |
| `build.config` | Kconfig.build | Build option configuration |
| `.config` | chip.config + build.config | Final merged configuration |
| `capabilities.h` | chip.config → preprocessing | Chip capability declaration header |
| `autoconf.h` | .config → parsing | C preprocessor macro definitions |

### SOC/BOARD Parameter Handling

```bash
# Specify SOC during build
cmake -B build -DSOC=TLSR9528A -S .
# Specify BOARD during build
cmake -B build -DBOARD=TLSR9528A_EVK -S .

# West command (specify SOC)
west tl-build --soc TLSR9528A

# West command (specify BOARD)
west tl-build --board TLSR9528A_EVK
```

`SOC`/`BOARD` passed this way only take effect the **first time** `chip.config` is generated for a build directory (as of UniSDK v0.3.0) — CMake seeds the choice into the non-interactive Kconfig pass so it comes out selected, instead of requiring the interactive `menuconfig` UI. If `chip.config` already exists (e.g. a build directory reused across configure runs), these flags are ignored; delete `chip.config` or edit it directly to change SOC/BOARD.

`kconfig_parser.py`/`soc_board_setter.py` provide standalone SOC/BOARD dependency resolution and combination validation, but are not currently invoked automatically as part of this flow.

## Key Scripts

| Script | Purpose |
|--------|---------|
| `kconfig.py` | Non-interactive Kconfig processing, configuration merging, validity verification |
| `menuconfig.py` | Interactive terminal configuration interface |
| `preprocess_kconfig.py` | Configuration preprocessing, YAML variable expansion |
| `kconfig_parser.py` | Kconfig parsing and SOC/BOARD validation |
| `soc_board_setter.py` | SOC/BOARD configuration and dependency resolution |

## Menuconfig Trigger Methods

1. **Auto-triggered during build** — Automatically opens the interactive interface when config files are missing
2. **Manually triggered** — `python scripts/menuconfig.py Kconfig.chip`
3. **Non-interactive generation** — CMake configuration phase uses `kconfig.py` to auto-generate defaults

## Configuration Option Examples

```kconfig
# core/configs/Kconfig.gpio

config TLK_GPIO_PORT_A_ENABLED
    bool "Enable GPIO Port A"
    default y
    help
        Enable GPIO Port A instance.

config TLK_GPIO_PREVENT_SLEEP
    bool "Prevent sleep when GPIO is active"
    depends on TLK_PM
    default y
```
