---
title: Connectivity
status: STABLE
---

# Connectivity

## Overview

UniSDK integrates BLE (Bluetooth Low Energy) Controller (Link Layer), providing fundamental wireless connectivity for BLE application development.

## Code Location

:::{dropdown} BLE Controller Directory
:summary: Click to expand/collapse

```text
subsystem/ble/controller/
├── acl/                    # ACL Link Layer
├── CMakeLists.txt
├── Kconfig
├── README.md               # Coding standards
└── README_zh.md
```
:::

## Coding Standards

The BLE Controller follows strict coding standards to ensure performance and reliability:

### File Naming

- Source files use lowercase letters and underscores, e.g., `tlk_ble_ll_acl.c`

### Function Naming

- Public functions use the `tlk_ble_` prefix
- Internal functions use the `_` prefix

### Interrupt Functions

- Interrupt handler functions have specific naming and modifier requirements
- Interrupt functions should be as short as possible, avoiding complex operations

## Kconfig Configuration

```kconfig
# BLE related configuration options (configured interactively via menuconfig)
```

## Examples

- [BLE Example](../samples/ble.md) — BLE advertising and connection demo

## Planned

The following protocol stack features are under planning:

- BLE Host Layer (GAP, GATT, SM)
- Zigbee
- Thread
- Matter

> For more details, please contact the Telink team for the latest updates.
