---
title: mbedTLS Sample
status: DRAFT
---

# mbedTLS Sample

## Overview

The `mbedtls_demo` sample demonstrates using mbedTLS's PSA Crypto API on-device to generate random data and perform ECDSA (elliptic-curve) key generation, signing, and verification. The sample is built twice from the same logic: `main.c` (plain C) and `main.cpp` (a C++ variant that wraps the same headers in `extern "C"`), selected at build time by whether C++ wrappers are enabled.

## Features Demonstrated

- PSA Crypto initialization (`psa_crypto_init`)
- Random number generation (`psa_generate_random`)
- EC key pair generation on the SECP256R1 curve (`psa_generate_key` with `PSA_KEY_TYPE_ECC_KEY_PAIR(PSA_ECC_FAMILY_SECP_R1)`, 256-bit)
- Exporting private and public key material (`psa_export_key`, `psa_export_public_key`)
- ECDSA signing and verification over SHA-256 (`psa_sign_hash`, `psa_verify_hash` with `PSA_ALG_ECDSA(PSA_ALG_SHA_256)`)
- Key cleanup (`psa_destroy_key`)
- Hex-dump logging helper (`tlk_str_utils_convert_buf_to_hex` in `main.c`, `tlk_str_utils_buf_to_hex` in `main.cpp`)

## How It Works

### Initialization

1. `tlk_core_interrupt_enable()` is called first to enable interrupts.
2. The mbedTLS version string (`MBEDTLS_VERSION_STRING_FULL`) is logged.
3. `psa_crypto_init()` is called; if it fails, an error is logged and no tests run.

### Test Sequence

Once PSA Crypto is initialized, two tests run in sequence, aborting early (via `break` out of a `do { } while(0)` block) if any step fails:

1. **Random Testing** — Generates 31 random bytes with `psa_generate_random` and logs them as hex.
2. **EC DSA Testing** —
   - Builds key attributes for an exportable SECP256R1 key pair usable for signing and verifying hashes (`PSA_KEY_USAGE_SIGN_HASH | PSA_KEY_USAGE_VERIFY_HASH | PSA_KEY_USAGE_EXPORT`)
   - Generates the key pair with `psa_generate_key`
   - Exports and logs both the private key (`psa_export_key`) and public key (`psa_export_public_key`)
   - Signs a zeroed 32-byte hash with `psa_sign_hash` and logs the signature
   - Verifies the signature with `psa_verify_hash`
   - Destroys the key with `psa_destroy_key`

```c
psa_set_key_type(&attr, PSA_KEY_TYPE_ECC_KEY_PAIR(PSA_ECC_FAMILY_SECP_R1));
psa_set_key_bits(&attr, 256);
psa_set_key_usage_flags(&attr,
                        PSA_KEY_USAGE_SIGN_HASH | PSA_KEY_USAGE_VERIFY_HASH |
                            PSA_KEY_USAGE_EXPORT);
psa_set_key_algorithm(&attr, PSA_ALG_ECDSA(PSA_ALG_SHA_256));
```

A final `"All tests success!"` or `"Some tests failed!"` message is logged, and the program then spins forever in an empty `for (;;) {}` loop.

:::{note} C vs C++ Build
`CMakeLists.txt` globs all `*.c` files by default. If `CONFIG_TLK_ALLOW_CPP_WRAPPERS` is enabled, `main.c` is removed from the C sources and `main.cpp` (which wraps the same mbedTLS/PSA calls in `extern "C"` blocks) is built instead. Functionally the two files are equivalent.
:::

## Configuration Options

| Option | Description |
|------|------|
| `CONFIG_TLK_MBEDTLS_DEMO` | Enables the sample; selects `TLK_MBEDTLS` and `TLK_API_PRINT` (default `y`, not user-facing) |
| `CONFIG_TLK_BLE_CONTROLLER` | Explicitly disabled (`default n`) for this sample, since it does not use BLE |

## Build & Run

```bash
west tl-build samples/mbedtls_demo --board TLSR9528A_EVK
west tl-bdt download --chip TLSR9528A -i build/mbedtls_demo.bin
```

Source code: `samples/mbedtls_demo/main.c` (or `samples/mbedtls_demo/main.cpp` when built with `CONFIG_TLK_ALLOW_CPP_WRAPPERS`)
