---
title: Releases
status: DRAFT
---

# Releases

## Version Naming Convention

UniSDK follows the **MAJOR.MINOR.PATCH** format (e.g., `1.2.3`):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible feature additions
- **PATCH**: Backward-compatible bug fixes

## Current Version

Current version information is defined in `common/include/tlk_sdk_version.h`.

## Version Compatibility

### Chip Support Matrix

| SDK Version | TL321X | TL721X | TLSR922X | TLSR952X | Notes |
|---------|--------|--------|----------|----------|------|
| 0.x (current) | ✅ | ✅ | ✅ | ✅ | Initial version |

### Toolchain Versions

| Component | Version Requirement |
|------|---------|
| CMake | >= 3.20.0 |
| Python | >= 3.10 |
| Ninja | >= 1.10 |
| West | >= 0.14.0 |
| RISC-V GCC | V5.4.1+ |

## Upgrade Guide

Detailed upgrade guides and migration instructions will be provided with future version releases.
