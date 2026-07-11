---
title: YAML Description Reference
status: PLANNED
---

# YAML Description Reference

!!! note "Document Status: PLANNED — Automatic generation system under development"

The YAML Reference will be automatically extracted from YAML files in directories such as `core/*/properties/`, `core/*/registers/`, `soc/*/pinmux/`, providing a complete reference for device properties, register definitions, and pin multiplexing configurations.

## Planned Content

### Device Properties
- Configuration properties and capability descriptions for each peripheral (`core/*/properties/*.yaml`)

### Register Definitions
- Register layout and bit field descriptions for each peripheral (`core/*/registers/*.yaml`)

### Pin Multiplexing (Pinmux)
- Pin function assignments for each chip package (`soc/*/pinmux/*.yaml`)

## Implementation Plan

Based on extending the existing `yaml_reader.py`, `properties_gen.py`, and `registers_gen.py`, structured reference documentation will be automatically generated.

The automatic generation system will be added later.
