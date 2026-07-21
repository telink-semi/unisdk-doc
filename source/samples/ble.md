---
title: BLE Sample
status: DRAFT
---

# BLE Sample

!!! note "Document Status: DRAFT — Content is being finalized"

The BLE sample (`samples/adv_demo`) demonstrates BLE advertising functionality.

## Build & Run

```bash
west tl-build samples/adv_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/adv_demo.bin
```

## Related Resources

- [BLE Controller Documentation](../connectivity/ble/controller.md)
