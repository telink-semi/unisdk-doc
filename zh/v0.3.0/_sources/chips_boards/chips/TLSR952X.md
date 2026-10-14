---
title: TLSR952X Chip Series
status: DRAFT
---

# TLSR952X Chip Series

:::{note} Document Status: DRAFT — Detailed specifications to be added. The information below is based on SDK metadata and is subject to update.
:::

## Overview

The TLSR952X is a RISC-V microcontroller series from Telink, designed for general IoT application scenarios.

## Core Parameters

| Parameter | Value |
|------|-----|
| Core | RISC-V (32-bit) |
| Supported Protocols | BLE |
| Toolchain | `andes-riscv32-v5f-gcc14.2` (TL32 ELF MCULIB V5F GCC14.2) |

## Memory

| Region | Size | Start Address |
|------|-----|------|
| ROM | 2048 KB | 0x20000000 |
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

### System & Control
- PLIC (Platform-Level Interrupt Controller)
- PM (Power Management: Suspend, Deep Sleep, Deep Retention)
- PMP (Physical Memory Protection)
- STIMER (System Timer)
- MTIMER (Machine Timer)
- PWM
- QDEC (Quadrature Decoder)
- MSPI

### Security & Crypto
- PKE (Public Key Engine)
- AES
- TRNG (True Random Number Generator)

### Supported Package Options

- QFN40, QFN56, QFN88

## Supported Boards

- [TLSR9528A_EVK](../boards/TLSR9528A_EVK.md)
- [TLSR9528A_DONGLE](../boards/TLSR9528A_DONGLE.md)
