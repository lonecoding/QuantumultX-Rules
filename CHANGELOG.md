# 更新日志

本项目的重要变更会记录在此文件中。

## [0.1.0] - 2026-09-02

### 新增

- 新增可直接导入的 `config/full.conf`。
- 新增 AI、YouTube、Telegram、Google 和 TikTok 独立分流规则。
- 新增 Apple 服务策略规则。
- 新增模块化 `rules/adblock` 目录。
- 新增误拦截放行规则，并保证它先于广告规则加载。
- 新增规则校验脚本和 GitHub Actions。
- 新增贡献指南、Issue 模板和 Pull Request 模板。
- 修复 YouTube、Telegram 和 Apple 的失效图标地址。
- 完善项目说明、使用方法、策略组说明和注意事项。

### 兼容

- 保留根目录 `adblock.list`，避免旧 Raw 地址失效。
- 保留原策略组名称、默认顺序和图标地址。
