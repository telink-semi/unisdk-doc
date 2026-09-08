---
title: MCUboot Bootloader Sample
status: DRAFT
---

# MCUboot Bootloader Sample

## Overview

The `mcuboot_bootloader_demo` sample builds MCUboot as the bootloader stage: it validates and jumps to the signed application in Slot 0, and can optionally expose a UART serial recovery (DFU) console for uploading new images without a debugger.

## Features Demonstrated

- Bootloader startup and handoff to the application via `tlk_mcuboot_run()`
- Board-specific DFU-entry detection and recovery UART setup
- UART serial recovery transport configuration for `boot_serial`

## How It Works

### Initialization

1. **Global interrupts** are enabled via `tlk_core_interrupt_enable()`.
2. **Debug UART0** is configured if `CONFIG_TLK_DEBUG_LOG_INTERFACE_UART` is enabled, so bootloader log messages are visible.
3. `tlk_mcuboot_run()` is called, handing control to the bootloader core.

```c
int main(void)
{
    tlk_core_interrupt_enable();

#if TLK_IS_ENABLED(CONFIG_TLK_DEBUG_LOG_INTERFACE_UART)
    configure_uart(TLK_UART0, CONFIG_TLK_UART0_BAUDRATE, TLK_UART_RX_TIMEOUT_MUL_2);
#endif

    tlk_mcuboot_run();

    while (1)
    {
    }
}
```

### Boot Sequence (`tlk_mcuboot_run`)

1. Logs startup and warns if the image is verified against the SDK's development signing key (see `subsystem/mcuboot/port/keys.c`).
2. Initializes the crypto backend used for signature verification.
3. Calls `tlk_mcuboot_recovery_requested()`. If it returns `true`, the bootloader enters serial recovery instead of booting:
   - `tlk_mcuboot_prepare_recovery()` configures the recovery UART and DFU indicator LED.
   - `boot_serial_start()` runs the `boot_serial` console until reset.
4. Otherwise, `boot_go()` locates and validates a bootable image in Slot 0/Slot 1 and the sample jumps to it.
5. If no valid image is found, the bootloader logs an error and halts.

### DFU-Entry Detection

`tlk_mcuboot_recovery_requested()` is checked once, at boot, before `boot_go()` runs — the button must be held through power-up/reset, not pressed after the app has already booted. A 30 ms debounce confirms the press:

```c
bool tlk_mcuboot_recovery_requested(void)
{
    tlk_gpio_configure(PINMUX_KEY_2_PORT, PINMUX_KEY_2_PIN, TLK_GPIO_OUTPUT);
    tlk_gpio_pin_write(PINMUX_KEY_2_PORT, PINMUX_KEY_2_PIN, 1);

    tlk_gpio_configure(PINMUX_KEY_0_PORT, PINMUX_KEY_0_PIN, TLK_GPIO_INPUT_PULL_DOWN);

    tlk_api_time_delay(TLK_MS_TO_US(1));

    if (!tlk_gpio_pin_read(PINMUX_KEY_0_PORT, PINMUX_KEY_0_PIN))
    {
        return false;
    }

    tlk_api_time_delay(TLK_MS_TO_US(DFU_BUTTON_DEBOUNCE_MS));

    return tlk_gpio_pin_read(PINMUX_KEY_0_PORT, PINMUX_KEY_0_PIN) != 0;
}
```

When recovery is entered, `tlk_mcuboot_prepare_recovery()` turns on `LED1` as a visual indicator and configures the recovery UART (`RECOVERY_UART_TX_PORT`/`PIN` = PC4, `RECOVERY_UART_RX_PORT`/`PIN` = PC5) at 115200 baud on the `tlk_uart_module` selected by `CONFIG_TLK_MCUBOOT_SERIAL_UART`.

:::{note} Bootloader vs. Application build
This sample only builds the **bootloader** stage (`TLK_MCUBOOT_MODE_BOOTLOADER`). A separate application target built with `CONFIG_TLK_MCUBOOT_MODE_APP` runs under it, linked with space reserved for the MCUboot header. That application also links `bootutil_public.c`, so it can call `boot_set_confirmed()` to mark itself confirmed and avoid a revert on the next reset.
:::

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_MCUBOOT_SERIAL_RECOVERY` | Compiles in `boot_serial` and enables the DFU-entry button check. Disabled by default — without it, the sample only boots the application. |
| `CONFIG_TLK_MCUBOOT_SERIAL_UART` | Selects which `tlk_uart_module` (integer instance) carries the recovery console (default `0`). The corresponding `TLK_UARTx` must be enabled. |
| `CONFIG_TLK_MCUBOOT_PRODUCTION_KEY` | Silences the development-key warning once the public key in `subsystem/mcuboot/port/keys.c` has been replaced with a real release key. |
| `CONFIG_TLK_MCUBOOT_BOOTLOADER_SIZE` | Flash size allocated for the bootloader binary (default `0x00090000`, 576KB). |
| `CONFIG_TLK_MCUBOOT_HEADER_SIZE` | Space reserved at the start of each application slot for the MCUboot image header (default `0x00000200`). Must exactly match the `--header-size` passed to `imgtool` when signing. |
| `CONFIG_TLK_MCUBOOT_SLOT_SIZE` | Size allocated for each application slot (default `0x000B0000`, 704KB). |
| `CONFIG_TLK_MCUBOOT_SCRATCH_SIZE` | Size allocated for swap operations (default `0x00004000`, 16KB). |

:::{dropdown} Signing an Application Image
An application built with `CONFIG_TLK_MCUBOOT_MODE_APP` is linked with space reserved for the MCUboot header, but still needs to be signed with `imgtool` before the bootloader will accept it:

```
imgtool sign \
    --header-size   <CONFIG_TLK_MCUBOOT_HEADER_SIZE> \
    --pad-header \
    --slot-size     <CONFIG_TLK_MCUBOOT_SLOT_SIZE> \
    --version       1.0.0 \
    --key           <path-to-signing-key>.pem \
    app.bin app_signed.bin
```

Use the corresponding development signing key for local testing, or generate a real key pair and set `CONFIG_TLK_MCUBOOT_PRODUCTION_KEY`.
:::

:::{dropdown} Testing Serial Recovery (DFU)
1. Build and flash this sample with `CONFIG_TLK_MCUBOOT_SERIAL_RECOVERY=y`.
2. Hold `KEY_0` down **through power-up or reset** — `LED1` turns on once recovery mode is entered.
3. Connect to the recovery UART pins at 115200 baud and use an `mcumgr`-compatible client to interact with `boot_serial`, e.g.:
   - `image list` — list images currently in the slots.
   - `image upload` — upload a signed image. By default this targets the **primary** slot; pass the client's image-index flag (e.g. `-n 2`) to target the secondary slot for a normal test/confirm upgrade flow.
   - `image test` / `reset` / `image confirm` — mark the uploaded image for one-time boot or permanent confirmation.
:::

## Build & Run

```bash
west tl-build samples/mcuboot_bootloader_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/mcuboot_bootloader_demo.bin
```

Source code: `samples/mcuboot_bootloader_demo/main.c`
