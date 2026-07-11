# PMP Driver

Provides an API for configuring the Physical Memory Protection (PMP) unit on RISC-V cores.
PMP allows M-mode software to restrict physical memory access privileges (read, write, execute)
for each defined region, enforced in hardware for U-mode and optionally for M-mode when locked.


## Overview

The PMP unit supports up to **8 entries**. Each entry defines one protected memory region
and a set of access permissions.

Any violation is trapped precisely at the processor. The trap cause can be inspected via
`mcause`, `mdcause`, and `mtval` CSRs.


## Address Matching Modes

Each entry operates in one of two address matching modes:

| Mode | API | Description |
|---|---|---|
| `TOR` | `tlk_pmp_tor_config` | Top Of Range. The protected region is `[pmpaddr[entry-1], address)`. For entry 0, the lower bound is implicitly `0x00000000`. |
| `NAPOT` | `tlk_pmp_napot_config` | Naturally Aligned Power Of Two. The region is `[address, address + size)`. Base must be aligned to `size`; `size` must be a power of two, at minimum 8 bytes. |

To use TOR with an explicit lower bound, call `tlk_pmp_entry_disable` on `entry - 1` with
the desired lower bound address. This writes the address into `pmpaddr[entry-1]` without
activating protection on that entry.


## Permissions

Permissions are defined per entry via `struct tlk_pmp_config`:

| Field | Description |
|---|---|
| `r` | Allow read access. |
| `w` | Allow write access. |
| `x` | Allow instruction execution. |
| `l` | Lock the entry. See [Lock](#lock) below. |


## Lock

When `l = 1` is set on an entry:

- Writes to `PMPiCFG` and `PMPADDRi` are **ignored** by hardware until system reset.
- For TOR entries, `pmpaddr[entry-1]` is also frozen.
- Permissions apply to **all privilege modes**, including M-mode.

> A locked entry can only be cleared by a system reset. Set `l = 1` only when the
> protection must survive any software fault, including bugs in M-mode code.


## API

```c
void tlk_pmp_tor_config(enum tlk_pmp_entry entry, void *address,
                        struct tlk_pmp_config *config);
```

Configures `entry` in TOR mode. `address` is the exclusive upper bound of the protected region.

```c
void tlk_pmp_napot_config(enum tlk_pmp_entry entry, void *address, uint32_t size,
                          struct tlk_pmp_config *config);
```

Configures `entry` in NAPOT mode. `address` must be aligned to `size`.
`size` must be a power of two and at least 8 bytes.

```c
void tlk_pmp_entry_disable(enum tlk_pmp_entry entry, void *address);
```

Sets the entry to OFF mode, removing any active protection. The value of `address`
is retained in `pmpaddr[entry]` and can serve as the lower bound for a subsequent TOR entry.
Pass `NULL` if the address is not relevant. Has no effect if the entry is locked (`l = 1`).


## Configuration

All options are available under `PMP` in Kconfig.

| Symbol | Default | Description |
|---|---|---|
| `TLK_PMP_PM_DEVICE` | `n` | Enable Power Management support. When enabled, all PMP entry registers are saved before sleep and restored after wakeup. |
