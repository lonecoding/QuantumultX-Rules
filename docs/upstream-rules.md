# 分流资源与策略组

完整配置的远程规则直接引用 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/QuantumultX)。
本项目维护 Quantumult X 配置及 force-policy 绑定，上游维护规则内容。
标准版、扩展版加载相同资源，策略组的显示数量和候选不同。

| 上游资源 | 标准版绑定 | 扩展版绑定 |
| --- | --- | --- |
| OpenAI、Claude、Gemini、Copilot | AI | ChatGPT、Claude、Gemini、Copilot 分别绑定 |
| YouTube | YouTube，默认跟随 Google | YouTube，默认跟随 Google |
| Telegram、TikTok、Google、Apple | 对应同名策略组 | 对应同名策略组 |
| Netflix、Spotify、AppleTV、AppleNews | Proxies | 对应同名策略组 |
| Microsoft | 🎯Direct | Microsoft，默认直连 |
| AdvertisingLite | AdBlock | AdBlock |
| Hijacking | Hijacking | Hijacking |
| Global | Proxies | Proxies |
| China | direct | direct |

每个列表使用上游原始文件地址，格式为：

```text
https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/服务名/服务名.list
```

服务名大小写与上游一致。完整配置包含已核对的实际 URL，不需要用户自己拼接。
`force-policy` 指定实际绑定，不依赖上游文件内部的策略名称。

局域网采用 Quantumult X 内置 `FILTER_LAN`，国内 IP 采用 `FILTER_REGION`，均直接绑定
内置 `direct`。没有 LAN / China 策略组，也不需要下载本仓库的 LAN 文件。
`[filter_local]` 默认只保留 Final 兜底。

## 解析器

配置引用 [KOP-XIAO / Shawn resource-parser.js](https://github.com/KOP-XIAO/QuantumultX/blob/master/Scripts/resource-parser.js)。
需要转换的节点订阅同时设置 `opt-parser=true`。解析器地址只负责资源转换，策略组负责
决定请求走哪个节点，两者用途不同。真实订阅仅在自己的设备中填写。

## 覆盖范围

AI 组汇总四个上游服务列表，不表示所有 AI 网站都会进入这个组。YouTube 虽属于 Google，
仍保留单独资源，便于用户在需要时为视频选择不同节点，默认跟随 Google 即可。

上游列表可能重复或覆盖同一域名；直接引用上游不等于列表之间完全没有重叠。
Copilot 列表包含共享 OpenAI 域名及 IP-ASN，AdvertisingLite 的覆盖也比原有独立广告文件广。
配置将具体服务放在通用厂商列表前，但实际规则类型优先级、匹配优化和节点结果仍需查看
客户端日志，不能把资源顺序当作完整的客户端模拟。

上游规则与脚本跟随各自 master 更新；本项目发布版本固定配置结构，不会固定上游内容。
需要固定快照时，分别替换资源 URL 中的分支为核对过的上游提交 SHA。
上游版权与许可证属于原作者，不计为本项目规则数量。

## 配置入口和维护

- recommended.conf：标准版。
- extended.conf：扩展版。
- full.conf、daily.conf：标准版的兼容入口，内容相同。
- 独立规则文件保留在 [兼容目录](legacy-rule-files.md)，完整配置不加载它们。

修改 scripts/config-builder.js 后，运行 `node scripts/generate_profiles.js --write` 同步四个入口。
`python scripts/generate_daily.py` 是将已有标准版同步到两个兼容入口的辅助命令。
完整的设置、检查与升级方法见 [使用指南](profiles.md)。
