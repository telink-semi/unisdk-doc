---
title: SPI Driver
status: DRAFT
---

# SPI Driver

:::{note} Document Status: DRAFT — Content is being finalized
:::

## Overview

The SPI driver supports master/slave mode communication, providing blocking and DMA transfer modes.

## API Reference

```c
// SPI initialization
void tlk_spi_configure(enum tlk_spi_module spi_num, uint32_t speed);

// SPI read/write
enum tlk_spi_status tlk_spi_write(enum tlk_spi_module spi_num, ...);
enum tlk_spi_status tlk_spi_read(enum tlk_spi_module spi_num, ...);
```

## Samples

See [SPI Samples](../samples/spi.md).
