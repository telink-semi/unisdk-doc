---
title: I2C Sample
status: DRAFT
---

# I2C Sample

!!! note "Document Status: DRAFT — Content is being finalized"

The I2C sample (`samples/i2c_demo`) includes two sub-samples:

- **DS1307** — I2C communication with the DS1307 RTC chip
- **Ping-Pong** — I2C master-slave bidirectional communication demo

## Build & Run

```bash
west tl-build samples/i2c_demo/ds1307 --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/ds1307.bin
```
