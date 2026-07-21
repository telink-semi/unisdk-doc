---
title: I2C Driver
status: DRAFT
---

# I2C Driver

:::{note} Document Status: DRAFT — Content is being finalized
:::

## Overview

The I2C driver supports master/slave mode communication, providing blocking and DMA transfer modes.

## API Reference

```c
// I2C initialization
void tlk_i2c_configure(enum tlk_i2c_module i2c_num, uint32_t speed);

// I2C read/write
enum tlk_i2c_status tlk_i2c_write(enum tlk_i2c_module i2c_num, ...);
enum tlk_i2c_status tlk_i2c_read(enum tlk_i2c_module i2c_num, ...);
```

## Samples

See [I2C Samples](../samples/i2c.md).
