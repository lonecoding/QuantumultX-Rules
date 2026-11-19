# Surge Mac 订阅配置

主配置：[Surge-Mac.conf](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/surge/Surge-Mac.conf)

这是个人 QuanX 配置对应的 Surge 版本，保留 11 份分类规则、国内域名及 IP 直连、阿里 DoH，并为微信应用提供直连规则。

## 首次导入

公开主配置不包含节点，也不引用本地文件，可独立从 URL 下载。未添加节点时 Proxies 默认 REJECT，避免将需要代理的流量误改为直连。

推荐使用私人关联配置：在本地配置的 `[Proxy]` 中保存节点、`[Proxy Group]` 中保存策略组，`[General]` 和 `[Rule]` 通过 `#!include` 引用上面的远程主配置 URL。这样节点不公开，主配置和规则继续订阅更新。

旧版本使用远程配置引用本地 `Lonecoding-Local.dconf`，会在 Surge Mac 6.12 的 URL 导入阶段触发 `key cannot be nil`。已移除此依赖；本地文件检查通过不能代替 URL 导入验证。

## 更新范围

- 主配置是 managed profile，最短更新间隔 86400 秒；主应用运行时更新，失败可沿用缓存。
- 每个远程规则集也以 86400 秒为更新间隔。
- 根目录个人 QuanX `.list` 更新后，GitHub Actions 自动将其转换到 `surge/rules/`，两种客户端使用同一份个人维护内容。
- 不会自动用 blackmatrix7 原版覆盖个人删改；此仓库的原始个人规则维护方式不变。
- 节点保存在本地，不会随主配置更新被覆盖，也不会自动更新机场/面板节点订阅。
- 本地应用例外可写入关联配置的 `[Rule]`，置于远程 include 之前，例如 `PROCESS-NAME,/Applications/Claude.app/,Proxies`。不要在本地例外中加入 FINAL，否则后续远程规则不会执行。

生成/检查：`python scripts/generate_surge.py`、`python scripts/generate_surge.py --check`。

DNS 与原配置一致：国内阿里 DoH。此配置不承诺隐藏国内解析器或所有直连出口。

规则原始来源为 blackmatrix7/ios_rule_script；个人来源记录见根目录规则头和 `docs/personal-rules-sources.json`。
