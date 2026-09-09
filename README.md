# QuantumultX-Rules

适合中国大陆日常使用的 Quantumult X 完整配置与模块化分流规则。
包含 KOP-XIAO 资源解析器、国内直连、海外代理、广告域名拦截和可选策略组。
添加自己的有效订阅、刷新资源并选择节点后，即可开始使用。

Complete Quantumult X profiles with an upstream resource parser, modular rules,
and customizable policy groups. Bring your own subscription.

## 快速开始

**推荐使用标准版：**

```text
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/recommended.conf
```

1. 备份当前配置，在 Quantumult X 导入上面的配置。
2. 在 `[server_remote]` 添加自己的订阅链接；配置内有可复制的示例行。
3. 刷新解析器、节点及规则资源，在 `Proxies` 选择一个可用节点。
4. 开启规则分流模式。AI、视频等默认跟随代理，Apple / Microsoft 默认直连。

节点、解析器和规则资源均需下载成功；首次下载 GitHub 资源可能需要已有可用网络。
本项目不提供节点。服务是否可用还取决于订阅协议、节点地区和服务本身的限制。

## 选择配置

| 配置 | 策略组 | 适合谁 |
| --- | --- | --- |
| [标准版 recommended.conf](config/recommended.conf) | 10 个：基础 4 组 + AI、YouTube、Telegram、TikTok、Apple、Google | 大多数希望按服务选节点的用户 |
| [扩展版 extended.conf](config/extended.conf) | 16 个：标准版 + ChatGPT、Claude、Gemini、Netflix、Spotify、Microsoft | 希望更细致地分别选择节点的用户 |

**两版拥有相同规则覆盖，区别是显示哪些独立策略组。** 没有独立组的海外服务跟随
`Proxies`，Apple / Microsoft 跟随 `🎯Direct`；ChatGPT、Claude、Gemini 优先跟随
已有的 `AI` 组。`AdBlock` 可切换 `reject` / `direct` 来开启或暂停广告及防劫持列表的拦截。

需要任意组合时，可使用本项目的 JavaScript 配置生成器，按需选择策略组。
具体导入地址、默认策略和自定义方式见 [完整配置使用指南](docs/profiles.md)。
所有组均为手动选择，服务组也可以直接选订阅中的节点；没有自动选区或解锁保证。

本仓库维护服务补充规则，服务覆盖及 China、Global、Hijacking 等列表直接引用上游
blackmatrix7；中国 IP 使用 Quantumult X 内置 `FILTER_REGION`。不需要安装解密证书。
静态检查已覆盖配置生成及策略引用，尚未完成 Quantumult X 实机验证。

原有 [full.conf](config/full.conf)、[daily.conf](config/daily.conf) 和独立规则地址继续保留。
旧模板行为见 [上游规则说明](docs/upstream-rules.md)，不随新预设切换。
向已有配置添加独立规则，见 [模块使用指南](docs/setup.md)。
实验性 YAML 规则构建工具见 [LoneRules](https://github.com/lonecoding/lonerules)。

## Rules

<!-- RULES_TABLE_START -->
| Rule | Description | Rules | Subscription |
|------|-------------|------:|--------------|
| AI | General AI services | 6 | [Link](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/AI/AI.list) |
| ChatGPT | OpenAI / ChatGPT | 4 | [Link](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/ChatGPT/ChatGPT.list) |
| Claude | Anthropic / Claude | 2 | [Link](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Claude/Claude.list) |
| Gemini | Google Gemini | 3 | [Link](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Gemini/Gemini.list) |
| Google | Google services | 9 | [Link](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Google/Google.list) |
| YouTube | YouTube / YouTube Music | 8 | [Link](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/YouTube/YouTube.list) |
| Telegram | Telegram | 16 | [Link](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Telegram/Telegram.list) |
| TikTok | TikTok | 9 | [Link](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/TikTok/TikTok.list) |
| Apple | Apple / iCloud | 11 | [Link](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Apple/Apple.list) |
| Advertising | Advertising blocking | 65 | [Link](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Advertising/Advertising.list) |
| LAN | LAN / private networks | 7 | [Link](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/LAN/LAN.list) |
<!-- RULES_TABLE_END -->

## Documentation

- [完整配置、预设选择与自定义策略组](docs/profiles.md)
- [Setup, policy groups, and troubleshooting](docs/setup.md)
- [Optional daily template and upstream sources / 上游规则](docs/upstream-rules.md)
- [Contributing and validation](CONTRIBUTING.md)
- [Maintenance, regression tests, and releases](docs/maintenance.md)
- [Changelog](CHANGELOG.md)

Report false positives or request rules through [Issues](https://github.com/lonecoding/QuantumultX-Rules/issues/new/choose).
The root `adblock.list` remains available for existing subscriptions and is
generated from `rules/Advertising/Advertising.list`.

## License

[MIT](LICENSE)
