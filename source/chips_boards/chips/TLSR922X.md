---
title: TLSR922X Chip Series
status: DRAFT
---

# TLSR922X Chip Series

:::{note} Document Status: DRAFT — Detailed specifications to be added. The information below is based on SDK metadata and is subject to update.
:::

## Overview

The TLSR922X is a RISC-V microcontroller series from Telink, designed for wireless audio application scenarios.

## Core Parameters

| Parameter | Value |
|------|-----|
| Core | RISC-V (32-bit) |
| Supported Protocols | BLE |
| Toolchain | `andes-riscv32-v5f-gcc14.2` (TL32 ELF MCULIB V5F GCC14.2) |

## Memory

| Region | Size | Start Address |
|------|-----|------|
| ROM | — | — |
| IRAM | 256 KB | 0x00000000 |
| DRAM | 256 KB | 0x00080000 |

## Peripheral List

### Standard Peripherals
- GPIO
- UART
- I2C
- SPI
- ADC
- DMA

### Audio
- Audio Codec

### System & Control
- PLIC (Platform-Level Interrupt Controller)
- PM (Power Management: Suspend, Deep Sleep, Deep Retention)
- PMP (Physical Memory Protection)
- STIMER (System Timer)
- MTIMER (Machine Timer)
- MSPI

### Security & Crypto
- PKE (Public Key Engine)
- SKE (Symmetric Key Engine)
- HASH
- TRNG (True Random Number Generator)

### Supported Package Options

- QFN48, QFN88

## Supported Boards

- [TLSR9228A_EVK](../boards/TLSR9228A_EVK.md)
