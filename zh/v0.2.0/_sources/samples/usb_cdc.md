---
title: USB CDC Sample
status: DRAFT
---

# USB CDC Sample

:::{note} Document Status: DRAFT — Content is being finalized
:::

The `usb_cdc_demo` sample is based on the TinyUSB framework and demonstrates USB CDC serial port functionality.

## Build & Run

```bash
west tl-build samples/tinyusb_demos/usb_cdc_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/usb_cdc_demo.bin
```
