---
title: Contribution Guide
status: DRAFT
---

# Contribution Guide

## How to Contribute

Community developers are welcome to contribute code, documentation, examples, and issue reports.

### Submitting an Issue

- Use GitLab Issues to report bugs or request new features
- Provide detailed reproduction steps and environment information
- Attach error logs and configuration information

### Submitting a Merge Request

1. Fork the repository
2. Create a feature branch
3. Write code and add tests
4. Ensure CI checks pass
5. Submit MR and describe the changes

### Code Standards

- Follow the existing code style
- C code should use the format defined in `.clang-format`
- Run `pre-commit` checks before submitting

### Documentation Contributions

- Documentation uses Markdown format
- Chinese documentation is placed in the `docs/zh/` directory
- Mark document status (`STABLE` / `DRAFT` / `DEPRECATED` / `PLANNED`)

## Development Environment

See [Getting Started](../getting_started/index.md) to learn how to set up the development environment.
