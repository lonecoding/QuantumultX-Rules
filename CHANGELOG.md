# 更新日志

本项目的重要变更会记录在此文件中。

## [0.2.0] - 2026-09-03

### 变更

- 将规则重构为 `rules/服务名/服务名.list` 目录结构。
- 将综合 AI 规则拆分为 ChatGPT、Claude、Gemini 和通用 AI 四组。
- 将配置中的局域网规则迁移到独立的 LAN 规则文件。
- 新增自动生成服务 README 和根目录规则表格的脚本。
- 扩展规则校验，覆盖目录结构、空行、格式、重复规则、IP/CIDR 和 README 统计。
- 更新配置、文档、Issue 模板和 GitHub Actions 中的规则路径。

## [0.1.0] - 2026-09-02

### 新增

- 新增可直接导入的 `config/full.conf`。
- 新增 AI、YouTube、Telegram、Google 和 TikTok 独立分流规则。
- 新增 Apple 服务策略规则。
- 新增模块化广告规则目录。
- 新增误拦截放行规则，并保证它先于广告规则加载。
- 新增规则校验脚本和 GitHub Actions。
- 新增贡献指南、Issue 模板和 Pull Request 模板。
- 修复 YouTube、Telegram 和 Apple 的失效图标地址。
- 完善项目说明、使用方法、策略组说明和注意事项。

### 兼容

- 保留根目录 `adblock.list`，避免旧 Raw 地址失效。
- 保留原策略组名称、默认顺序和图标地址。
