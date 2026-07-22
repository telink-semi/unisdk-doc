---
title: SPI Sample
status: DRAFT
---

# SPI Sample

:::{note} Document Status: DRAFT — Content is being finalized
:::

The SPI sample (`samples/spi_demo`) demonstrates the basic usage of SPI communication.

## Build & Run

```bash
west tl-build samples/spi_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/spi_demo.bin
```
