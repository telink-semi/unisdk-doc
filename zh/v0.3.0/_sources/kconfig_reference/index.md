---
title: Kconfig Reference
status: PLANNED
---

# Kconfig Reference

:::{note} Document Status: PLANNED — Automatic generation system under development
:::

The Kconfig Reference will be automatically extracted from `Kconfig.build`, `Kconfig.chip`, and all `rsource` sub-files, providing a complete list of Kconfig options.

## Planned Content

- Name, type, and default value of each configuration option
- Dependencies (`depends on`, `select`)
- Value ranges (`range`, `choice`)
- Help text
- Navigation organized by functional module

## Implementation Plan

Based on extending the existing `kconfig_parser.py`, reference documentation in Markdown format will be automatically extracted from Kconfig source files.

The automatic generation system will be added later.
