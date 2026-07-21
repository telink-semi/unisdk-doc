---
title: ADC Sample
status: DRAFT
---

# ADC Sample

!!! note "Document Status: DRAFT — Content is being finalized"

The ADC sample (`samples/adc_demo`) demonstrates the basic usage of the analog-to-digital converter.

## Build & Run

```bash
west tl-build samples/adc_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/adc_demo.bin
```
