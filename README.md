# QuantumultX-Rules

一套面向中国大陆日常使用的 Quantumult X 完整配置，提供标准版、扩展版和自定义策略组。
**分流列表直接引用上游，本项目负责配置、策略组及默认走向。** 添加自己的订阅即可开始配置使用。

Complete Quantumult X configurations with upstream rules and customizable policy groups.
Bring your own subscription.

## 快速开始

推荐使用标准版：

```text
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/recommended.conf
```

1. 备份当前配置，在 Quantumult X 导入上面的配置。
2. 在 `[server_remote]` 添加自己的订阅链接，配置内有示例格式。
3. 刷新解析器、节点和规则资源，在 `Proxies` 选择可用节点。
4. 开启规则分流模式，根据需要调整下面的策略组。

已配置 KOP-XIAO 资源解析器，需要转换的节点订阅使用 `opt-parser=true`。
首次下载 GitHub 资源需要可用网络；本项目不提供节点。

## Quantumult X 中的策略组

下面列出的是导入后在客户端操作的策略组。一个策略组可以接收多个上游规则列表。

| 策略组 | 默认走向 / 用途 | 标准版 | 扩展版 |
| --- | --- | :---: | :---: |
| Proxies | 手动选择一个订阅节点，供其他组跟随 | ✓ | ✓ |
| 🎯Direct | 固定直连 | ✓ | ✓ |
| AdBlock | 广告拦截：reject / direct | ✓ | ✓ |
| Hijacking | 防劫持：reject / direct | ✓ | ✓ |
| ✈️Final | 未命中规则的请求 → Proxies | ✓ | ✓ |
| AI | AI 服务 → Proxies | ✓ | ✓ |
| Google | Google 通用服务 → Proxies | ✓ | ✓ |
| YouTube | 默认跟随 Google，也可单独选节点 | ✓ | ✓ |
| Telegram | 默认跟随 Proxies | ✓ | ✓ |
| TikTok | 默认跟随 Proxies | ✓ | ✓ |
| Apple | 默认直连，也可单独选节点 | ✓ | ✓ |
| ChatGPT、Claude、Gemini、Copilot | 默认跟随 AI，也可分别选节点 | — | ✓ |
| Netflix、Spotify | 默认跟随 Proxies，也可分别选节点 | — | ✓ |
| AppleTV、AppleNews | 默认跟随 Proxies，也可分别选节点 | — | ✓ |
| Microsoft | 默认直连，也可单独选节点 | — | ✓ |

**局域网和国内 IP 直接绑定内置 direct，不创建 LAN 或 China 策略组。**
AI 汇总 OpenAI、Claude、Gemini、Copilot 上游列表；其他 AI 网站按实际命中的规则或 Final 分流。

## 选择配置

- [标准版：11 个策略组](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/recommended.conf)
- [扩展版：20 个策略组](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/extended.conf)
- [按需组合策略组](docs/profiles.md#按需组合策略组)

自定义组合可安全导出到新文件（需要 Node.js 22+）：

```bash
node scripts/generate_profiles.js --groups AI,Telegram,YouTube --output ../my-quantumultx.conf
```

已有文件不会被覆盖；生成后导入 Quantumult X，再添加自己的订阅。

两版加载相同的上游资源，区别是显示哪些独立策略组。没有独立组的 AI 服务跟随 AI，
YouTube 优先跟随 Google，其他海外服务跟随 Proxies；Apple / Microsoft 默认直连。
组名是服务用途，不要求与上游规则文件名一一对应。

## 规则来源

服务、广告和防劫持规则直接引用 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/QuantumultX)，
通过 `force-policy` 绑定到上述策略组。局域网和国内 IP 使用 Quantumult X 内置资源。
节点解析器引用 [KOP-XIAO / Shawn](https://github.com/KOP-XIAO/QuantumultX/blob/master/Scripts/resource-parser.js)。

上游独立维护并更新，规则可能交叉覆盖。拦截组选择 direct 时，对应命中请求直连；
不会继续交给后面的代理规则。配置不启用 HTTPS 解密，无需安装证书。

## 使用与维护

- [完整使用指南、默认策略和升级方式](docs/profiles.md)
- [配置资源来源](docs/upstream-rules.md)
- [贡献与自动检查](CONTRIBUTING.md)
- [维护与验证范围](docs/maintenance.md)
- [更新日志](CHANGELOG.md)

自动检查覆盖配置生成、上游绑定及策略引用，尚未完成 Quantumult X 手机实测。
服务是否可用还取决于节点、账号、地区及上游规则，请以请求日志为准。

问题反馈：[Issues](https://github.com/lonecoding/QuantumultX-Rules/issues/new/choose)。
`full.conf`、`daily.conf` 与标准版保持相同内容；新用户使用上方标准版或扩展版。
已有独立规则订阅见 [兼容目录](docs/legacy-rule-files.md)，它们不被完整配置加载。

## License

[MIT](LICENSE)。直接引用的上游资源保留原作者的版权和许可。
