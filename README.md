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
- [Contributing and validation](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

Report false positives or request rules through [Issues](https://github.com/lonecoding/QuantumultX-Rules/issues/new/choose).
The root `adblock.list` remains available for existing subscriptions.

## License

[MIT](LICENSE)
