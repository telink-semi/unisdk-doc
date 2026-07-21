---
title: Contribution Guide
status: DRAFT
---

# Contribution Guide

Community developers and contributors are welcome to contribute code, documentation, examples, and issue reports to the UniSDK project.

> **Note on SDK code contributions**: This guide focuses on the **unisdk-doc** documentation repository. For SDK code contributions (unisdk), please refer to the [unisdk repository](https://github.com/telink-semi/unisdk).

---

## Documentation Repository: unisdk-doc

The documentation repository ([unisdk-doc](https://github.com/telink-semi/unisdk-doc)) follows the same branch model as the SDK code repository.

### Branch Model

```
main                                        ← Stable (latest release)
  ↑ merge
release-v*.*.*                              ← Release branches
  ↑ merge
develop                                     ← Active development
  ↑ merge
doc/<topic>  fix/<topic>  feat/<topic>      ← Feature / fix branches
```

| Branch | Purpose | CI/CD Deployment |
|---|---|---|
| `main` | Stable branch. Only updated when a release is finalized. Content is a snapshot from `develop` promoted via `release-v*.*.*`. | Pushes deploy to `/en/latest/` |
| `develop` | Active development branch. All documentation changes land here first. | Pushes deploy to `/en/dev/` |
| `release-v*.*.*` | Release preparation branch. Created from `develop` before tagging a new release. | Tag pushes deploy to `/en/v*.*.*/` |
| `doc/*` | Feature branches for documentation changes (e.g., `doc/gpio-update`, `doc/restructure-getting-started`). | No deployment |
| `fix/*` | Feature branches for documentation fixes (e.g., `fix/typo-uart`, `fix/broken-link`). | No deployment |

### Lifecycle

1. **Development**: Create a feature branch from `develop` → make changes → open PR → merge into `develop`
2. **Release**: When ready for a release, create `release-v*.*.*` from `develop` → finalize → tag → CI builds the tag
3. **Stable**: Merge the release branch into `main`, updating the stable documentation

---

## Contributing Documentation Changes

### Step-by-Step Workflow

1. **Create a branch from `develop`**

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b doc/your-topic
   ```
   Use a descriptive branch name: `doc/<topic>` for new content, `fix/<topic>` for fixes.

2. **Make your changes**

   - Documentation files are written in **Markdown** (`.md`) or **reStructuredText** (`.rst`)
   - English documentation is in `en/`, Chinese in `zh/` (if applicable)
   - Follow the existing document structure and formatting conventions

3. **Build locally (optional but recommended)**

   ```bash
   pip install -r requirements.txt
   pip install sphinx
   sphinx-build -b html -c . en/ _build/html
   ```

4. **Commit and push**

   ```bash
   git add <changed-files>
   git commit -m "docs(topic): brief description of the change"
   git push origin doc/your-topic
   ```

   Use conventional commit prefixes: `docs:` for documentation, `fix:` for bug fixes, `ci:` for CI changes.

5. **Open a Pull Request**

   - Target branch: `develop`
   - Describe what you changed and why
   - Link any related issues

6. **Review and merge**

   - The PR will be reviewed by maintainers
   - After approval, it will be merged into `develop`
   - The CI pipeline will automatically build and deploy to `/en/dev/`

---

## Document Status Markers

Each documentation page should include a status marker in its frontmatter:

| Status | Meaning |
|---|---|
| `STABLE` | Content is complete, reviewed, and ready for production use |
| `DRAFT` | Content is under development, may be incomplete or unreviewed |
| `DEPRECATED` | Content is outdated and should not be used for new designs |
| `PLANNED` | Content is planned but not yet written |

Example:

```yaml
---
title: GPIO Driver Guide
status: STABLE
---
```

---

## Release Process

When the documentation is ready for a release:

1. **Create a release branch** from `develop`:
   ```bash
   git checkout develop
   git checkout -b release-v0.x.x
   ```

2. **Finalize**: Make any last-minute fixes on the release branch.

3. **Tag the release**:
   ```bash
   git tag v0.x.x
   git push origin v0.x.x
   ```
   The CI will build and deploy the tag to `/en/v0.x.x/`.

4. **Merge to main**:
   ```bash
   git checkout main
   git merge release-v0.x.x
   git push origin main
   ```
   The CI will build and deploy to `/en/latest/`.

---

## CI/CD Behavior

| Trigger | Source Checked Out | Deploy Path |
|---|---|---|
| Push to `develop` | `develop` branch | `/en/dev/` |
| Push to `main` | `develop` branch (snapshot) | `/en/latest/` |
| Push tag `v*.*.*` | Tagged commit | `/en/v*.*.*/` |

All versions are built and deployed to the `gh-pages` branch, which serves the documentation via GitHub Pages.

---

## Submitting Issues

- Use [GitHub Issues](https://github.com/telink-semi/unisdk-doc/issues) to report documentation bugs or request improvements
- Provide the page URL and describe what is incorrect or missing
- Attach screenshots or error logs if applicable

---

## Code Standards (SDK Contributions)

For contributions to the SDK codebase (unisdk):

- C code should follow the format defined in `.clang-format`
- Run `pre-commit` checks before submitting
- See the [unisdk repository](https://github.com/telink-semi/unisdk) for detailed guidelines
