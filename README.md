# QuantumultX-Rules

适用于 Quantumult X 的分流和广告域名拦截规则。

这里提供一份规则配置框架，也可以单独引用各个规则文件。策略组名称和图标沿用现有配置。

## 功能

- 常见广告域名拦截
- ChatGPT、Claude、Gemini 及其他 AI 服务分流
- YouTube、Telegram、Google 和 TikTok 分流
- Apple 服务策略选择
- 局域网及保留地址直连
- 未匹配流量的最终策略

## 目录结构

```text
QuantumultX-Rules/
├── config/
│   └── full.conf
├── rules/
│   ├── Advertising/
│   │   ├── Advertising.list
│   │   └── README.md
│   ├── AI/
│   │   ├── AI.list
│   │   └── README.md
│   ├── Apple/
│   ├── ChatGPT/
│   ├── Claude/
│   ├── Gemini/
│   ├── Google/
│   ├── LAN/
│   ├── Telegram/
│   ├── TikTok/
│   └── YouTube/
├── scripts/
│   ├── generate_readme.py
│   └── validate_rules.py
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── adblock.list
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

每个服务目录包含同名 `.list` 文件和自动生成的 `README.md`。根目录的 `adblock.list` 暂时保留为兼容入口；新配置使用 `rules/Advertising/Advertising.list`。

## 快速使用

### 使用配置框架

在 Quantumult X 中打开配置文件下载或导入功能，使用下面的 Raw 地址：

```text
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/full.conf
```

这份配置不包含节点和订阅地址。导入后，在 `[server_remote]` 中添加自己的订阅；`Proxies` 会自动收集节点标签。

### 单独引用规则

也可以在已有配置的 `[filter_remote]` 中按需添加：

```ini
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/LAN/LAN.list, tag=LAN, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Advertising/Advertising.list, tag=广告拦截, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/ChatGPT/ChatGPT.list, tag=ChatGPT, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Claude/Claude.list, tag=Claude, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Gemini/Gemini.list, tag=Gemini, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/AI/AI.list, tag=AI, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/YouTube/YouTube.list, tag=YouTube, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Telegram/Telegram.list, tag=Telegram, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Google/Google.list, tag=Google, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/TikTok/TikTok.list, tag=TikTok, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Apple/Apple.list, tag=Apple, update-interval=86400, enabled=true
```

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

## 策略组

| 策略组 | 默认选择 | 备用选择 | 用途 |
|---|---|---|---|
| `Proxies` | 自动收集全部节点 | — | 节点总入口 |
| `🎯Direct` | 直连 | Proxies | 国内与无需代理的流量 |
| `YouTube` | Proxies | 🎯Direct | YouTube |
| `AI` | Proxies | 🎯Direct | ChatGPT、Claude、Gemini 等 |
| `Telegram` | Proxies | 🎯Direct | Telegram |
| `Apple` | 🎯Direct | Proxies | Apple 与 iCloud 服务 |
| `Google` | Proxies | 🎯Direct | Google 服务 |
| `TikTok` | Proxies | 🎯Direct | TikTok |
| `✈️Final` | Proxies | 🎯Direct | 其他未匹配流量 |

策略组图标沿用原配置中的 `img-url`，仓库不会强制下载或替换图标。

## 检查规则

安装 Python 3.10 或更高版本后，先更新 README 统计，再执行校验：

```bash
python scripts/generate_readme.py
python scripts/validate_rules.py
```

校验会检查目录结构、空行、规则格式、重复项、IP/CIDR、策略名称、README 统计、Raw 路径、旧用户名和两个广告列表是否一致。每次提交也会由 GitHub Actions 自动检查。

## 反馈问题

误拦截和新规则请求可以直接通过仓库的 Issue 模板提交。准备修改规则时，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 注意事项

- 广告规则可能出现误拦截。确认域名后，请提交 Issue 并在自己的配置中先加入直连规则。
- 不同地区和网络环境的可用策略不同，可在 Quantumult X 中手动切换各策略组。
- 本仓库不包含节点、订阅地址、服务器信息或访问令牌。
- 规则会随服务域名变化而调整，建议保留 `update-interval=86400`。

## 许可证

本项目使用 [MIT License](LICENSE)。
