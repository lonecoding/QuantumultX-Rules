# Quantumult X setup

> 新用户推荐使用 [完整配置与可选策略组](profiles.md)。本页介绍旧 full.conf 及独立规则的接入方式。


## Configuration template

Import [full.conf](https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/full.conf),
then add your subscription under `[server_remote]`. The template contains no
servers, subscriptions, or access tokens. `Proxies` collects all server tags.

1. Back up your current configuration before importing the full template.
2. Add your own subscription URL under `[server_remote]`, then refresh that resource.
3. Open `Proxies` and select a working node. Choose the policy for each service group.
4. Use rule-based routing mode and inspect a request in the activity log to confirm
   the matched rule, policy group, and selected node.

The template's `static` groups are manual choices. An alternative candidate is
not automatic failover. Existing saved choices can differ from the initial
candidate order shown below.

### Default routing behavior

Unmatched traffic reaches `FINAL,✈️Final`; that group's initial candidate is
`Proxies`. This includes unmatched mainland-China sites and `.cn` domains.
There is no general China-direct list or GeoIP rule in the template. If you need
regional direct routing, add your own verified rules and check their interaction
with the service lists. Selecting direct for `✈️Final` changes **all** unmatched
traffic, not only mainland-China traffic.

## Individual rule lists

An optional [daily template](../config/daily.conf) adds upstream China, Global,
and Hijacking subscriptions to the existing service rules. The full template
above keeps its original behavior. Read [upstream sources and setup](upstream-rules.md)
before switching; the daily template is not an exact copy of a personal configuration.

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

For example, if your existing configuration already defines a policy named
`MyAI`, import ChatGPT with the following line under `[filter_remote]`:

```ini
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/ChatGPT/ChatGPT.list, tag=ChatGPT, force-policy=MyAI, update-interval=86400, enabled=true
```

Replace `MyAI` with your exact existing policy name. `tag` is a resource label;
`force-policy` overrides the policy written inside the imported rules, as described
in the [official configuration sample](https://github.com/crossutility/Quantumult-X/blob/master/sample.conf).
Add this line once; replace an existing ChatGPT import rather than duplicating it.

## Policy groups

| Group | Default | Alternative | Purpose |
| --- | --- | --- | --- |
| `Proxies` | All server tags | — | Server entry point |
| `🎯Direct` | direct | — | Always direct |
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
repeat the failing action. Check the request log for the exact hostname and
the rule that rejected it. Confirm which policy works when advertising blocking
is disabled, then re-enable the list and add a narrow exception.

Copy **one appropriate rule** from this example into your existing
`[filter_local]` section, before its existing `FINAL` rule:

```ini
[filter_local]
# Direct-only service: replace this reserved example hostname.
HOST,ads.example.com,direct
# Service that still needs your AI proxy policy: replace this example hostname.
HOST,assets.example.net,AI
FINAL,✈️Final
```

These are illustrative domains, not known false positives. Keep only the rule
you need and replace the hostname with the one from your log. Use your existing
policy and FINAL names; do not add a second `[filter_local]` section or FINAL.
The standalone [exception fragment](../config/exceptions.example.conf) contains
the same two examples and is not a complete configuration.

`HOST` matches only the named hostname. `HOST-SUFFIX` also allows every subdomain,
so use it only when that entire scope has been verified. Do not change all
false positives to direct: some services still need a proxy. After adding the
exception, repeat the failing action and confirm the selected rule and policy
in Quantumult X. Client matching optimization and local settings can affect
the result; textual order alone is not an on-device verification.

Then [report the issue](https://github.com/lonecoding/QuantumultX-Rules/issues/new/choose)
with the matched rule, working policy, Quantumult X version, network, and
before/after results. Remove sensitive information from logs.

Keep `update-interval=86400` to refresh remote lists daily. The legacy
`adblock.list` is generated from `rules/Advertising/Advertising.list` and contains
the same effective rules; use the latter for new configurations.

### Return to a previous version

Back up your personal configuration and subscription settings first. To pin a
rule list, replace `main` in its Raw URL with a published version tag. To pin an
entire configuration, change **every** repository URL under `[filter_remote]`
to that tag too: importing a tagged `full.conf` alone still leaves its embedded
URLs following `main`. Refresh the resources and verify their contents in the
client. Resume `main` URLs when you want ongoing updates again.

## Repository layout

- `config/full.conf`: configuration template.
- `rules/Service/Service.list`: rules grouped by service.
- `rules/Service/README.md`: generated counts and subscription link.
- `scripts/`: README generation and validation.
- `.github/`: issue forms and automated checks.

See [Contributing](../CONTRIBUTING.md) before changing rules.
