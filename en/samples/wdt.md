---
title: Watchdog Sample
status: DRAFT
---

# Watchdog Sample

!!! note "Document Status: DRAFT — Content is being finalized"

The `wdt_demo` sample demonstrates the usage of the watchdog timer.

## Build & Run

```bash
west tl-build samples/wdt_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/wdt_demo.bin
```
