# unisdk-doc 分支模型重组计划

## 概述

将 `unisdk-doc` 仓库从单 `main` 分支模式重构为与 `unisdk` 仓库一致的 Git 分支模型：`main` + `develop` + `release` 分支 + 功能分支。当前文档尚未定版，所有内容从 `main` 迁移到 `develop`，`main` 清理为仅保留 README.md 的稳定分支。

## 当前状态分析

### unisdk-doc (文档仓库)

* **分支**: 仅有 `main`（本地）+ `origin/main` + `origin/gh-pages`

* **内容**: 所有文档、配置、CI/CD 都集中在 `main` 上

* **CI/CD**: `.github/workflows/docs-deploy.yml` 监听 `main` 推送和 `v*` tag，构建到 `gh-pages`

* **远程**: `git@github.com:telink-semi/unisdk-doc.git`

* **Tag**: 无任何 tag

* **工作区**: 当前在 `main`，工作区干净

### unisdk (SDK 仓库，参考对象)

* **main**: 仅一个 `README.md`

* **develop**: 活跃开发分支

* **release-v0.2.0**: v0.2.0 发布分支

* **feat/fix/doc/refactor/\***: 功能/修复/文档/重构分支

* **tag**: `v0.2.0`

## 决策记录

| 决策项          | 选定方案               | 理由                                         |
| ------------ | ------------------ | ------------------------------------------ |
| main 清理后内容   | 仅留 README.md       | 与 unisdk main 对齐，表示稳定分支                    |
| develop 分支内容 | 当前 main 全部内容       | 文档未定版，应移到 develop 继续开发                     |
| CI/CD 触发     | main + develop 双触发 | main→latest, develop→dev, tag→v\*.*.*      |
| Release 工作流  | 与 unisdk 对齐        | develop → release-v\*.*.* → tag → 合并到 main |
| gh-pages 分支  | 保留不动               | GitHub Pages 部署分支，无需改动                     |

## 具体变更

### 变更 1: 创建 develop 分支 (从当前 main 创建)

* **文件**: N/A (Git 操作)

* **操作**: 基于当前 `main` 的 HEAD (commit `4b577b7`) 创建 `develop` 分支

* **原因**: 保留所有当前文档内容到开发分支

* **命令**:

  ```bash
  git checkout main
  git branch develop
  git push origin develop
  ```

### 变更 2: 清理 main 分支

* **文件**: N/A (Git 操作)

* **操作**: 将 `main` 硬重置到新的初始提交，仅保留 README.md

  * 创建 orphan 分支或硬重置

  * 添加一个简洁的 README.md（与 unisdk 风格一致）

* **建议的 README.md 内容**:

  ```markdown
  # UniSDK Documentation

  This is the **stable** branch of the UniSDK documentation.
  For active development, see the [develop](https://github.com/telink-semi/unisdk-doc/tree/develop) branch.
  ```

* **原因**: main 作为稳定分支，在首个正式 release 前保持干净

### 变更 3: 更新 CI/CD 工作流

* **文件**: `.github/workflows/docs-deploy.yml`

* **操作**: 修改工作流配置

  1. **触发条件**: 增加 `develop` 分支推送触发
  2. **构建版本映射**:

     * `main` → `latest`（稳定版占位）

     * `develop` → `dev`（开发版）

     * `v*` tag → `v*.*.*`（发布版，保留当前逻辑）
  3. **条件判断**: 在构建循环中判断当前触发分支，映射到对应版本标签
  4. **SDK 缓存**: 保持当前 SDK 缓存逻辑不变
  5. **多语言**: 保持当前 `LANGUAGES: "en"` 设置不变

### 变更 4: 新增文档贡献指南 (Documentation Contribute Guide)

- **文件**: `en/contribute/index.md`（修改现有文件）
- **操作**: 将当前的 SDK 通用贡献指南扩展为包含**文档仓库专用协作流程**的贡献指南
- **新增内容要点**:
  1. **分支模型说明**: 解释 unisdk-doc 的分支结构（main/develop/release/feature）
  2. **文档开发流程**:
     - 从 `develop` 创建功能分支: `doc/<topic>` 或 `fix/<topic>`
     - 在功能分支上修改文档
     - 提交 PR 合并回 `develop`
     - 定期从 `develop` 构建预览（CI 自动部署到 /en/dev/）
  3. **Release 流程**:
     - 从 `develop` 创建 `release-v*.*.*` 分支
     - 在 release 分支上打 `v*.*.*` tag
     - CI 自动构建并部署到 `/en/v*.*.*/`
     - 合并到 `main` 作为稳定版
  4. **分支命名规范**:
     - `doc/*` — 文档新增或重构
     - `fix/*` — 文档错误修复
     - `release-v*.*.*` — 发布分支
  5. **CI/CD 行为**: 解释 main→latest, develop→dev, tag→version 的部署映射
  6. **文档状态标记**: 文档页面应标注 `STABLE` / `DRAFT` / `DEPRECATED` 状态
- **原因**: 团队和外部贡献者需要清晰的协作流程说明，确保分支模型被正确使用

### 变更 5: 推送并验证

- **命令序列**:

  ```bash
  # 1. 推送 develop
  git push origin develop

  # 2. 强制推送新的 main（需要 --force，注意权限）
  git push origin main --force

  # 3. 推送到 GitHub 后，检查 Actions 运行状态
  ```

## 影响分析

| 方面          | 影响                                                 | 缓解措施                 |
| ----------- | -------------------------------------------------- | -------------------- |
| 本地 clone    | 已有 `main` checkout 的开发者需要 rebase                   | 通知团队分支模型变更           |
| CI/CD 部署路径  | 构建产物路径从 `/en/main/` 变更为 `/en/latest/` 和 `/en/dev/` | 更新 landing page 生成脚本 |
| 现有 gh-pages | 不受影响，保留现有构建记录                                      | 无需操作                 |
| GitHub 权限   | `git push --force` 可能需要分支保护规则调整                    | 确认是否有 main 分支保护      |

## 验证步骤

1. 确认 `develop` 分支包含所有原始文档内容 (与当前 `main` 一致)
2. 确认 `main` 分支仅包含 README.md
3. 确认 CI/CD 在推送 `develop` 后触发构建并部署到 `/en/dev/`
4. 确认 CI/CD 在推送 `main` 后触发构建并部署到 `/en/latest/`
5. 确认 `gh-pages` 分支内容未受影响
6. 确认 landing page 可正确导航到 dev/latest 版本

## 后续工作

* 首个正式 release 时: 从 `develop` 创建 `release-v*.*.*` 分支 → 打 tag → CI 自动构建并部署

* 未来功能开发: 从 `develop` 创建 `feat/*` 或 `fix/*` 分支，合并回 `develop`

* 稳定版发布: 合并 release 分支到 `main`，更新 `main` 上 README.md 中的版本信息

