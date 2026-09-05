# Quantumult X setup

## Configuration template

Import [full.conf](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/full.conf),
then add your subscription under `[server_remote]`. The template contains no
servers, subscriptions, or access tokens. `Proxies` collects all server tags.

## Individual rule lists

Add the lists you need under `[filter_remote]` in your existing configuration:

```ini
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/LAN/LAN.list, tag=LAN, update-interval=86400, enabled=true
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/Advertising/Advertising.list, tag=Advertising, update-interval=86400, enabled=true
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

Keep the listed order, especially YouTube before Google. Each list references
policy names from the template; define matching policies in your configuration
or bind imported lists to your own policies with `force-policy`.

## Policy groups

| Group | Default | Alternative | Purpose |
| --- | --- | --- | --- |
| `Proxies` | All server tags | — | Server entry point |
| `🎯Direct` | direct | Proxies | Direct traffic |
| `YouTube` | Proxies | 🎯Direct | YouTube |
| `AI` | Proxies | 🎯Direct | ChatGPT, Claude, Gemini, and other AI services |
| `Telegram` | Proxies | 🎯Direct | Telegram |
| `Apple` | 🎯Direct | Proxies | Apple and iCloud |
| `Google` | Proxies | 🎯Direct | Google services |
| `TikTok` | Proxies | 🎯Direct | TikTok |
| `✈️Final` | Proxies | 🎯Direct | Unmatched traffic |

Policy names and icon URLs are retained for compatibility. Select policies to
suit your network and region.

## Troubleshooting

If a site or app stops working, temporarily disable the advertising list and
check the request log. Add a direct rule for a confirmed false positive before
the advertising rules, then [report it](https://github.com/lonecoding/QuantumultX-Rules/issues/new/choose).

Keep `update-interval=86400` to refresh remote lists daily. The legacy
`adblock.list` contains the same effective rules as
`rules/Advertising/Advertising.list`; use the latter for new configurations.

## Repository layout

- `config/full.conf`: configuration template.
- `rules/Service/Service.list`: rules grouped by service.
- `rules/Service/README.md`: generated counts and subscription link.
- `scripts/`: README generation and validation.
- `.github/`: issue forms and automated checks.

See [Contributing](../CONTRIBUTING.md) before changing rules.
