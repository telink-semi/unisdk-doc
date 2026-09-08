---
title: PMP Sample
status: DRAFT
---

# PMP Driver Sample

## Overview

A sample application demonstrating the usage of the TLK PMP API. It protects the upper half
of a 16-element array against all access, then attempts to read or write the full array,
triggering a PMP violation trap on the protected region.

## Features Demonstrated

- PMP region protection using TOR (Top-Of-Range) address matching (`tlk_pmp_configure_tor`)
- PMP region protection using NAPOT (Naturally Aligned Power-Of-Two) address matching
  (`tlk_pmp_configure_napot`)
- Locked PMP entries (`l = 1`) that deny all read/write/execute access
- PMP state retention across a sleep/wake cycle (optional)

## How It Works

On startup the sample:

1. *(Optional)* Configures PMP protection on `demo_array[8..15]` using the selected address
   matching scheme. All permissions are disabled and the entry is locked (`l = 1`).
2. *(Optional)* If `CONFIG_TLK_PMP_DEMO_SLEEP` is set, enters sleep for 500 ms and wakes up,
   demonstrating that PMP state is correctly saved and restored across the sleep.
3. Iterates over all 16 elements of `demo_array`:
   - With `CONFIG_TLK_PMP_DEMO_READ` — reads and logs each value.
   - With `CONFIG_TLK_PMP_DEMO_WRITE` — writes and logs each value.

Elements `[0..7]` complete successfully. On the first access to `demo_array[8]` a PMP
violation trap is raised.

## Configuration

All options are exposed via **Kconfig** under *PMP Sample configuration*. The PMP mode and the
access action are each modeled as a single-choice group (`choice`), so exactly one option in
each group is active at a time; `TLK_PMP_DEMO_TOR` and `TLK_PMP_DEMO_READ` are the defaults.

| Symbol | Type | Default | Description |
|---|---|---|---|
| `TLK_PMP_DEMO_OFF` | `bool` (choice) | — | PMP mode: no protection is configured; all 16 elements are accessible without a fault. |
| `TLK_PMP_DEMO_TOR` | `bool` (choice) | `y` | PMP mode: protect `demo_array[8..15]` using TOR address matching. Entry 0 holds the lower bound; Entry 1 holds the upper bound. |
| `TLK_PMP_DEMO_NAPOT` | `bool` (choice) | `n` | PMP mode: protect `demo_array[8..15]` using NAPOT address matching. |
| `TLK_PMP_DEMO_READ` | `bool` (choice) | `y` | Action mode: access the array by reading. |
| `TLK_PMP_DEMO_WRITE` | `bool` (choice) | `n` | Action mode: access the array by writing. |
| `TLK_PMP_DEMO_SLEEP` | `bool` | `n` | Enter sleep between PMP configuration and array access (only selectable when the PMP mode is not `OFF`). Demonstrates PMP state retention across sleep; selects `TLK_API_SLEEP` and implies `TLK_PMP_PM_DEVICE`. |

> **Note:** With `TLK_PMP_DEMO_OFF` selected, no protection is configured and all 16 elements
> are accessible without a fault.

## Build & Run

```bash
west tl-build samples/pmp_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/pmp_demo.bin
```

Source code: `samples/pmp_demo/main.c`
