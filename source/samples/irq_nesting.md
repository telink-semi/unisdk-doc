---
title: IRQ Nesting Sample
status: DRAFT
---

# IRQ Nesting Sample

!!! note "Document Status: DRAFT — Content is being finalized"

The `irq_nesting_demo` sample demonstrates interrupt nesting functionality.

## Build & Run

```bash
west tl-build samples/irq_nesting_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/irq_nesting_demo.bin
```
