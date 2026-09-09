# QuantumultX-Rules

Modular routing and advertising blocklists for Quantumult X.

Use individual service lists or start with the included configuration template.
For an experimental YAML-to-rules build tool, see [LoneRules](https://github.com/lonecoding/lonerules).

## Quick start

Import this configuration in Quantumult X:

```text
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/full.conf
```

Add your own subscription under `[server_remote]`. The template does not include
servers or subscriptions. `Proxies` collects your server tags automatically.

Unmatched traffic uses `✈️Final`, whose initial candidate is `Proxies`. This also
applies to unmatched mainland-China sites: no general China-direct list is
included. Policy groups are manual selections, not automatic failover.

For the optional daily template, use
[daily.conf](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/daily.conf).
It keeps this repository's service rules and adds upstream blackmatrix7
Hijacking (reject), Global (Proxies), and China (direct) subscriptions.
It also references KOP-XIAO's resource parser, with an opt-parser subscription
example for converting supported non-native node formats.
Only China-list matches are explicitly directed to direct; no GeoIP or
FILTER_REGION rule is added. See [upstream sources and setup / 上游规则说明](docs/upstream-rules.md).

To add individual lists to an existing configuration, follow the
[setup guide](docs/setup.md).

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
