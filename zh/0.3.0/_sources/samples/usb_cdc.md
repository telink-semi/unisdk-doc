---
title: USB CDC Sample
status: DRAFT
---

# USB CDC Sample

:::{note} Document Status: DRAFT — Content is being finalized
:::

## Overview

The USB CDC demo, built on the TinyUSB framework, demonstrates a USB CDC (virtual serial port)
device that echoes back any data received from the host.

:::{note} Source directory name
The sample currently lives at `samples/tinyusb_demos/usb_device/cdc_demo` (project name
`USB_Demo`), not `samples/tinyusb_demos/usb_cdc_demo`. Build and download paths below use the
actual directory.
:::

## Features Demonstrated

- TinyUSB device stack initialization (`tud_init`) and task servicing (`tud_task`)
- USB device/configuration/string descriptor callbacks for a single CDC interface
  (`tud_descriptor_device_cb`, `tud_descriptor_configuration_cb`, `tud_descriptor_string_cb`)
- CDC data echo using `tud_cdc_available`, `tud_cdc_read`, `tud_cdc_write`, `tud_cdc_write_flush`
- Device lifecycle callbacks: `tud_mount_cb`, `tud_umount_cb`, `tud_suspend_cb`, `tud_resume_cb`
- CDC line coding/state callbacks: `tud_cdc_line_coding_cb`, `tud_cdc_line_state_cb`

## How It Works

### Descriptors

The device descriptor uses the Miscellaneous class (`TUSB_CLASS_MISC`) with the Interface
Association Descriptor subclass/protocol, which is the recommended setup for CDC so host drivers
(Windows/Linux) enumerate it correctly. Vendor ID, product ID, device version, manufacturer,
product, serial number, and interface name strings are all pulled from Kconfig
(`CONFIG_TLK_USB_VENDOR_ID`, `CONFIG_TLK_USB_PRODUCT_ID`, `CONFIG_TLK_USB_DEVICE_VERSION`,
`CONFIG_TLK_USB_DEVICE_MANUFACTURER`, `CONFIG_TLK_USB_DEVICE_PRODUCT_NAME`,
`CONFIG_TLK_USB_DEVICE_SERIAL_NUMBER`, `CONFIG_TLK_USB_DEVICE_INTERFACE_NAME`). The single CDC
interface's notification/OUT/IN endpoint numbers come from `CONFIG_TLK_USB_CDC_NOTIF_EP`,
`CONFIG_TLK_USB_CDC_OUT_EP`, and `CONFIG_TLK_USB_CDC_IN_EP`.

### Main Loop

```c
int main(void)
{
    tud_init(BOARD_TUD_RHPORT); // Initialize USB Device Stack

    while (1)
    {
        tud_task(); // Device task: Handle USB events (MUST be called frequently)
        cdc_task(); // Application task: Handle Serial data
    }

    return 0;
}
```

### Echo Task

`cdc_task()` checks that a host is connected and that RX data is available, reads up to 64 bytes
from the CDC RX FIFO, and immediately writes the same bytes back out, flushing to force
transmission without waiting for the buffer to fill:

```c
void cdc_task(void)
{
    if (tud_cdc_connected())
    {
        if (tud_cdc_available())
        {
            uint8_t buf[64];
            uint32_t count = tud_cdc_read(buf, sizeof(buf));

            tud_cdc_write(buf, count);
            tud_cdc_write_flush();
        }
    }
}
```

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_USB_CDC_DEMO` | Enables the sample (selects `TLK_USB`); enabled by default |

The device/interface identity (vendor/product IDs, strings) and endpoint numbers are configured
via the shared `TLK_USB` Kconfig options referenced above rather than demo-specific symbols.

## Build & Run

```bash
west tl-build samples/tinyusb_demos/usb_device/cdc_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/cdc_demo.bin
```

Source code: `samples/tinyusb_demos/usb_device/cdc_demo/main.c`
