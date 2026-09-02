# QuantumultX-Rules

适用于 Quantumult X 的模块化分流、广告拦截与隐私保护规则。

仓库以可直接使用的完整配置为入口，保留现有策略组名称和图标，并将不同服务的规则拆分到独立文件，方便按需引用和维护。

## 功能

- 🚫 常见广告域名拦截
- 🤖 AI 平台分流
- 🎬 YouTube 分流
- ✈️ Telegram 分流
- 🌐 Google 服务分流
- 🎵 TikTok 分流
- 🍎 Apple 服务策略选择
- 🎯 未匹配流量的最终策略

## 目录结构

```text
QuantumultX-Rules/
├── config/
│   └── full.conf
├── rules/
│   ├── adblock/
│   │   └── adblock.list
│   ├── direct/
│   │   └── apple.list
│   └── proxy/
│       ├── ai.list
│       ├── google.list
│       ├── telegram.list
│       ├── tiktok.list
│       └── youtube.list
├── adblock.list
├── CHANGELOG.md
├── LICENSE
└── README.md
```

根目录的 `adblock.list` 暂时保留为兼容入口；新配置使用 `rules/adblock/adblock.list`。

## 快速使用

### 导入完整配置

在 Quantumult X 中打开配置文件下载或导入功能，使用下面的 Raw 地址：

```text
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/full.conf
```

导入后请在 Quantumult X 中自行添加节点或订阅。`Proxies` 策略组会自动收集所有节点标签。

### 单独引用规则

也可以在已有配置的 `[filter_remote]` 中按需添加：

```ini
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

## 注意事项

- 广告规则可能出现误拦截。如应用或网页异常，请先停用广告规则定位问题，再添加更精确的放行规则。
- 不同地区和网络环境的可用策略不同，可在 Quantumult X 中手动切换各策略组。
- 本仓库不包含节点、订阅地址、服务器信息或访问令牌。
- 规则会随服务域名变化而调整，建议保留 `update-interval=86400`。

## 许可证

本项目使用 [MIT License](LICENSE)。
