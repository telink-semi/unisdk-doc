---
title: ADC Sample
status: DRAFT
---

# ADC Sample

:::{note} Document Status: DRAFT — Content is being finalized
:::

## Overview

The `adc_demo` sample demonstrates the basic usage of the ADC driver: configuring a single-ended channel, sampling into a buffer, and logging the results in a loop. An optional configuration shows the ADC read loop running alongside the power-management sleep API.

## Features Demonstrated

- ADC channel configuration (`tlk_adc_configure`) — channel, prescale, resolution, sample frequency, voltage reference, and sampling pin
- Buffered sampling (`tlk_adc_read`) with timeout/error handling via `enum tlk_adc_status`
- Optional DMA channel reservation for the ADC (`tlk_dma_chn_request`, guarded by `CONFIG_TLK_DMA`)
- Optional low-power sampling loop using `tlk_api_sleep` (requires `CONFIG_TLK_ADC_DEMO_PM`)

## How It Works

### Initialization

The sample builds a `struct tlk_adc_config` and passes it to `tlk_adc_configure`:

```c
struct tlk_adc_config cfg = {
    .channel     = TLK_ADC_CHANNEL_0,
    .prescale    = TLK_ADC_PRESCALE_1F4,
    .resolution  = TLK_ADC_RESOLUTION_12,
    .sample_freq = TLK_ADC_SAMPLE_FREQ_96K,
    .vref        = TLK_ADC_VREF_1P2V,
    .sampling_port_pin =
        {
            .port = TLK_GPIO_PORT_B,
            .pin  = TLK_GPIO_PIN_0,
        },
    .is_differential = false,
    .differential_port_pin =
        {
            .port = TLK_GPIO_PORT_D,
            .pin  = TLK_GPIO_PIN_0,
        },
    .timeout_us = 10000,
#if TLK_IS_ENABLED(CONFIG_TLK_DMA)
    .dma_en      = false,
    .dma_channel = tlk_dma_chn_request(),
#endif
};

tlk_adc_configure(&cfg);
```

The channel samples on GPIO port B pin 0 in single-ended mode (`is_differential = false`); the differential pin is set but unused in that mode. When `CONFIG_TLK_DMA` is enabled, a DMA channel is reserved for the ADC configuration up front (though `dma_en` is left `false` in this sample).

### Main Loop

```c
while (1)
{
    enum tlk_adc_status status = tlk_adc_read(adc_values, ADC_BUFFER_SIZE);

    if (status == TLK_ADC_OK)
    {
        for (uint32_t i = 0; i < ADC_BUFFER_SIZE; i++)
        {
            TLK_LOG_INFO(adc_demo, "%u", adc_values[i]);
        }
    }
    else
    {
        TLK_LOG_ERROR(adc_demo, "Timeout");
    }

#if TLK_IS_ENABLED(CONFIG_TLK_ADC_DEMO_PM)
    tlk_api_sleep(TLK_SEC_TO_MS(1));
#else
    tlk_api_time_delay(TLK_SEC_TO_US(1));
#endif
}
```

Each iteration reads `ADC_BUFFER_SIZE` (8) samples into `adc_values` and logs every value on success, or logs a timeout error otherwise. The loop then either sleeps for 1 second (PM build) or busy-delays for 1 second (default build).

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_ADC_DEMO_PM` | Build the ADC demo with power management: uses `tlk_api_sleep` instead of a busy delay between reads, selects `TLK_API_SLEEP` and implies `TLK_ADC_PM_DEVICE` |

The sample's base `TLK_ADC_DEMO` config selects `TLK_ADC`, `TLK_DEBUG_LOG_CONSOLE`, and `TLK_API_TIME` unconditionally.

## Build & Run

```bash
west tl-build samples/adc_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/Telink.bin
```

Source code: `samples/adc_demo/main.c`
