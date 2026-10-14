---
title: BLE Host Sample
status: DRAFT
---

# BLE Host Sample

## Overview

The `ble_host_demo` sample demonstrates the **BLE Host v2** stack: a newer host implementation built on a SAL (Service Abstraction Layer, `tlk_ble_host_sal.h`), distinct from the lower-level advertising and controller-only samples. It brings up a BLE peripheral that advertises, accepts multiple simultaneous ACL connections, registers the standard Core and Device Information Service (DIS) GATT groups, and re-starts advertising automatically as connections come and go.

See also: [BLE Sample](ble.md) for the lower-level advertising/controller demos.

## Features Demonstrated

- BLE Host v2 stack bring-up (`ble_host_v1_init`, `tlk_ble_host_loop`)
- Peripheral advertising setup with custom advertising and scan-response data (`ble_host_gap_adv_set_adv_ind_param`, `ble_host_gap_adv_start`)
- GATT service groups: Core group and Device Information Service (`blc_svc_addCoreGroup`, `blc_svc_addDisGroup`, `blc_svc_calculateDatabaseHash`, `blc_svc_setDeviceName`)
- ACL connection lifecycle callbacks (`ble_host_acl_conn_register_user_data` with `connected`/`disconnected` callbacks)
- Tracking up to 4 simultaneous peripheral-role ACL connections
- SMP (Security Manager Protocol) initialization for pairing (`ble_host_smp_initial` with `BLE_HOST_SMP_LEGACY_JUST_WORKS_INIT_PARAMS`, `ble_host_smp_store_init`)

## How It Works

### Advertising Data

Advertising and scan-response payloads are built from static LTV (length-type-value) structures:

```c
static const struct ad_data_flags s_adv_flags = {
    .header.length                      = 0x02,
    .header.type                        = DT_FLAGS,
    .flags.le_limited_discoverable_mode = 1,
    .flags.br_edr_not_supported         = 1,
};

static const struct ad_data_complete_local_name_complete s_adv_complete_name = {
    .header.length = sizeof(BLE_PERIPHERAL_DEVICE_NAME),
    .header.type   = DT_COMPLETE_LOCAL_NAME,
    .name          = BLE_PERIPHERAL_DEVICE_NAME,
};
```

The device advertises as `"tlk_bluetooth_ble_per"`, including the flags and complete local name AD types in both the advertising data and the scan response.

### Initialization (`ble_host_v2_peripheral_init`)

1. Sets the advertising interval to 150 (units per `ble_host_gap_adv_set_adv_ind_param`) along with the advertising/scan-response data.
2. Registers the Core GATT group and the Device Information Service group (`blc_svc_addCoreGroup`, `blc_svc_addDisGroup`), computes the GATT database hash, and sets the device name.
3. Resets the local peripheral-connection tracking table (`s_app_acl_peripheral_info`), up to `APP_BLE_ACL_PERIPHERAL_MAX_COUNT` (4) entries, all initialized to `BLE_CONN_HANDLE_INVALID`.
4. Registers `s_app_acl_callbacks` (connected/disconnected handlers) via `ble_host_acl_conn_register_user_data`.
5. Initializes SMP pairing with Legacy Just Works parameters and sets up SMP bond storage for up to 4 devices (`ble_host_smp_store_init(4, 0)`).

### Connection Callbacks

- **`app_connected_callback`** — If the new connection is peripheral-role, records its connection handle in the first free slot and increments the connection count. As long as fewer than 4 peripheral connections are active, advertising is restarted (`ble_host_gap_adv_start`) so additional centrals can connect.
- **`app_disconnected_callback`** — If the disconnected connection was peripheral-role, frees its slot and decrements the count, then unconditionally restarts advertising.

### Main Loop

```c
int main(void)
{
    TLK_LOG_INFO(ble_host_v2_demo, "BLE HOST v2 starting...");

    ble_host_v1_init(NULL, NULL);
    tlk_core_interrupt_enable();

    ble_host_v2_peripheral_init();
    ble_host_v2_peripheral_start();

    // Main loop
    while (1)
    {
        tlk_ble_host_loop();
    }

    return 0;
}
```

`ble_host_v1_init` brings up the underlying host, interrupts are enabled, the peripheral role is initialized and advertising is started (`ble_host_v2_peripheral_start` calls `ble_host_gap_adv_start`), and the main loop repeatedly pumps the host's event loop via `tlk_ble_host_loop()`.

:::{note} SAL-Based Host Stack
This sample's naming (`ble_host_v1_init`, log tag `ble_host_v2_demo`) reflects that it exercises the newer BLE Host v2 architecture through the SAL header `tlk_ble_host_sal.h`, layered on top of the v1 host init call. This is architecturally different from `samples/adv_demo` and `samples/ble_controller_demo`, which work directly against the advertising/controller APIs — see [BLE Sample](ble.md).
:::

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_BLE_HOST_V2_DEMO` | Enables the sample; selects `TLK_BLE_HOST_V2` and `TLK_BLE_CONTROLLER` (default `y`, not user-facing) |

:::{note}
This sample has no user-selectable Kconfig choices beyond the auto-selected stack dependencies above — the peripheral behavior (advertising params, service groups, max connections) is fixed in `main.c`.
:::

## Build & Run

```bash
west tl-build samples/ble_host_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/ble_host_demo.bin
```

Source code: `samples/ble_host_demo/main.c`
