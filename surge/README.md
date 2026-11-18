# Surge Mac 订阅配置

主配置：[Surge-Mac.conf](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/surge/Surge-Mac.conf)

这是个人 QuanX 配置对应的 Surge 版本，保留 11 份分类规则、国内域名及 IP 直连、阿里 DoH，并为微信应用提供直连规则。

## 首次导入

1. 需要 Surge Mac 6.12 或更新版本，以使用个人 VLESS Reality 节点。
2. 将私人 `Lonecoding-Local.dconf` 放在 Surge Profiles 文件夹中。文件含 `[Proxy]` 节点和可选的 `[Rule]` 本地优先规则，不要提交到公开仓库。没有这个文件，主配置不能单独使用。
3. 使用上面的主配置 URL 从 Surge 下载并导入。
4. 选择规则模式和 Proxies 中的节点；开启所需网络接管前关闭另一代理软件的接管。

## 更新范围

- 主配置是 managed profile，最短更新间隔 86400 秒；主应用运行时更新，失败可沿用缓存。
- 每个远程规则集也以 86400 秒为更新间隔。
- 根目录个人 QuanX `.list` 更新后，GitHub Actions 自动将其转换到 `surge/rules/`，两种客户端使用同一份个人维护内容。
- 不会自动用 blackmatrix7 原版覆盖个人删改；此仓库的原始个人规则维护方式不变。
- 节点保存在本地，不会随主配置更新被覆盖，也不会自动更新机场/面板节点订阅。
- 本地应用例外可写入 `Lonecoding-Local.dconf` 的 `[Rule]`，例如 `PROCESS-NAME,/Applications/Claude.app/,Proxies`。不要在本地例外中加入 FINAL，否则后续远程规则不会执行。

生成/检查：`python scripts/generate_surge.py`、`python scripts/generate_surge.py --check`。

DNS 与原配置一致：国内阿里 DoH。此配置不承诺隐藏国内解析器或所有直连出口。

规则原始来源为 blackmatrix7/ios_rule_script；个人来源记录见根目录规则头和 `docs/personal-rules-sources.json`。
