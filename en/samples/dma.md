---
title: DMA Sample
status: DRAFT
---

# DMA Sample

!!! note "Document Status: DRAFT — Content is being finalized"

The DMA sample (`samples/dma_demo`) demonstrates the usage of direct memory access.

## Build & Run

```bash
west tl-build samples/dma_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/dma_demo.bin
```
