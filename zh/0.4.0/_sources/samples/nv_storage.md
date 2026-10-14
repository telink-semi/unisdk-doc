---
title: NV Storage Sample
status: DRAFT
---

# NV Storage Sample

## Overview

The `nv_storage_demo` sample demonstrates the non-volatile storage abstraction layer: enumerating the available storage devices and performing a read/erase/write/read round-trip against flash.

## Features Demonstrated

- Storage device enumeration (`tlk_storage_get_next_device`)
- Locating the storage device backing a given address range (`tlk_storage_find_device`)
- Reading and writing raw flash data (`tlk_storage_read`, `tlk_storage_write`)
- Log output via `TLK_LOG_INFO` / `TLK_LOG_HEXDUMP_INFO`

## How It Works

### Device Enumeration

At startup, the sample walks the list of registered storage devices and logs each one's name, base address, size, page size, clean (erased) byte pattern, and erase/read/write capability flags:

```c
for (struct tlk_storage_device* dev = tlk_storage_get_next_device(NULL); dev != NULL;
     dev                            = tlk_storage_get_next_device(dev))
{
    TLK_LOG_INFO(nv_storage_demo, "device: %s", dev->name);
    TLK_LOG_INFO(nv_storage_demo, "\tbase address: 0x%zx", dev->base);
    TLK_LOG_INFO(nv_storage_demo, "\tsize: %zu (0x%zx)", dev->size, dev->size);
    TLK_LOG_INFO(nv_storage_demo, "\tpage: %zu", dev->page);
    TLK_LOG_INFO(nv_storage_demo, "\tclean pattern: 0x%02x", dev->clean_byte);
    TLK_LOG_INFO(nv_storage_demo,
                 "\tcapable: %c%c%c",
                 dev->erase ? 'E' : '_',
                 dev->read ? 'R' : '_',
                 dev->write ? 'W' : '_');
}
```

### Read / Write Round-Trip

The sample picks a 1024-byte test region near the top of chip ROM (`UNISDK_CHIP_MEMORY_ROM_STARTADDR + UNISDK_CHIP_MEMORY_ROM_SIZE * 1024 - 5000`) and:

1. Locates the storage device covering that region with `tlk_storage_find_device`.
2. Reads the current contents with `tlk_storage_read` and hex-dumps them.
3. Checks whether the region is in its "clean" (erased) state by comparing every byte to `s_dev->clean_byte`.
4. Builds new test data — an incrementing byte pattern if the region was clean, or each byte incremented by one otherwise.
5. Writes the new data with `tlk_storage_write`.
6. Reads the region back and hex-dumps it again to confirm the write.

Any failure at each step (`tlk_storage_find_device` returning `NULL`, or a non-zero result from `tlk_storage_read`/`tlk_storage_write`) is logged and the sample stops early.

:::{note} Device-agnostic API
The sample never assumes a specific flash chip — it discovers devices via `tlk_storage_get_next_device`/`tlk_storage_find_device`, so the same code works across boards with different storage layouts.
:::

## Configuration Options

The sample itself exposes no user-facing Kconfig options — its `Kconfig` only auto-selects the storage and logging subsystems:

| Option | Description |
|------|------|
| `TLK_NV_STORAGE_DEMO` | Always enabled (`def_bool y`) when this sample is built; selects `TLK_NV_STORAGE` and `TLK_DEBUG_LOG_CONSOLE`. |

## Build & Run

```bash
west tl-build samples/nv_storage_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/nv_storage_demo.bin
```

Source code: `samples/nv_storage_demo/main.c`
