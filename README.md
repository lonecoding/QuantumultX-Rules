# QuantumultX-Rules

适用于 Quantumult X 的分流和广告域名拦截规则。

这里提供一份规则配置框架，也可以单独引用各个规则文件。策略组名称和图标沿用现有配置。

## 功能

- 常见广告域名拦截
- 误拦截域名放行
- AI、YouTube、Telegram、Google 和 TikTok 分流
- Apple 服务策略选择
- 未匹配流量的最终策略

## 目录结构

```text
QuantumultX-Rules/
├── config/
│   └── full.conf
├── rules/
│   ├── adblock/
│   │   └── adblock.list
│   ├── direct/
│   │   ├── apple.list
│   │   └── unbreak.list
│   └── proxy/
│       ├── ai.list
│       ├── google.list
│       ├── telegram.list
│       ├── tiktok.list
│       └── youtube.list
├── scripts/
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

根目录的 `adblock.list` 暂时保留为兼容入口；新配置使用 `rules/adblock/adblock.list`。

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
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/direct/unbreak.list, tag=误拦截修正, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/adblock/adblock.list, tag=广告拦截, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/proxy/ai.list, tag=AI, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/proxy/youtube.list, tag=YouTube, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/proxy/telegram.list, tag=Telegram, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/proxy/google.list, tag=Google, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/proxy/tiktok.list, tag=TikTok, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/direct/apple.list, tag=Apple, update-interval=86400, enabled=true
```

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

安装 Python 3.10 或更高版本后运行：

```bash
python scripts/validate_rules.py
```

脚本会检查规则格式、重复项、策略名称、Raw 路径、旧用户名和两个广告列表是否一致。每次提交也会由 GitHub Actions 自动检查。

## 反馈问题

误拦截和新规则请求可以直接通过仓库的 Issue 模板提交。准备修改规则时，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 注意事项

- 广告规则可能出现误拦截。确认域名后，将放行规则加入 `rules/direct/unbreak.list`。
- 不同地区和网络环境的可用策略不同，可在 Quantumult X 中手动切换各策略组。
- 本仓库不包含节点、订阅地址、服务器信息或访问令牌。
- 规则会随服务域名变化而调整，建议保留 `update-interval=86400`。

## 许可证

本项目使用 [MIT License](LICENSE)。
