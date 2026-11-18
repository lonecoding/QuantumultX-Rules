# 个人分流订阅

这组文件用于用户现有的 Quantumult X 配置，保留原有分类和策略组。
来源为 blackmatrix7/ios_rule_script 的 QuantumultX 规则；本地副本由 lonecoding 维护。
复制日期：2026-11-18。来源版本、删改明细和补充域名见 [来源记录](personal-rules-sources.json)。

## 使用

打开 [分流替换片段](../personal-filters.conf)，只替换原配置的 `[filter_remote]` 和 `[filter_local]` 两节。
该片段不是完整配置；节点订阅、DNS、图标及原有策略组继续使用用户自己的设置。
如果后来增加过其他本地例外，先保留并检查它们，不要直接覆盖。
手动更新规则资源，并确认 `✈️Final` 选择 `Proxies`。
不要继续同时挂载旧的同类分流列表或 `FILTER_REGION` 中国 IP 直连。

## 本次修改

- 原配置的 10 份远程列表均提供了自己的副本。
- 从实际订阅副本中共移除 221 条 IP-CIDR、IP6-CIDR、IP-ASN 或 GEOIP 规则。
- 原有域名、CDN 和分类规则保留；China.list 保留此前已删除的 IP 查询网站例外。
- China.list 新增 213 条明确的国内服务域名，覆盖微信图片、B站资源、银行、运营商、铁路、物流等缺口。
- 不恢复所有 `.cn` 域名直连；因此不能保证所有国内网站都被收录。
- [Diagnostics.list](../Diagnostics.list) 明确将 12 个 IP 查询/隐私检测域名规则绑定到 Proxies。
- 保留所有分类策略：OpenAI、Claude 使用 AI；YouTube、Telegram、TikTok、Apple、Google 使用各自的原策略组。

| 文件 | 当前规则数 | 本次移除的 IP/ASN 规则数 |
| --- | ---: | ---: |
| [Hijacking](../Hijacking.list) | 186 | 42 |
| [Telegram](../Telegram.list) | 25 | 15 |
| [OpenAI](../OpenAI.list) | 32 | 3 |
| [Claude](../Claude.list) | 3 | 0 |
| [YouTube](../YouTube.list) | 193 | 3 |
| [TikTok](../TikTok.list) | 35 | 0 |
| [Apple](../Apple.list) | 1867 | 13 |
| [Google](../Google.list) | 706 | 5 |
| [Global](../Global.list) | 35895 | 119 |
| [China](../China.list) | 3933 | 21 |

## 行为与限制

移除 IP 规则是为了减少未命中域名规则的请求为了 IP 分流而触发本地解析，不是 DNS 零泄露保证。
直连域名仍需本地解析，应用自带 DNS、系统例外或代理服务端 DNS 也可能影响检测结果。
直接以 IP 建立的连接会进入最终策略；Telegram 的纯 IP 连接通常仍走代理，Apple 等连接不再按原 IP 段自动分类。
Hijacking 的域名拦截仍保留，但原先仅依赖 IP 的 42 条拦截已移除。
国内 CDN 域名不会因为名称包含 CDN 而被删除；共享 CDN、云服务后缀的直连范围仍可能较广。
没有在 Quantumult X 真机验证；以客户端更新后的规则命中及 DNS 记录为准。

## 维护

这些是可手工编辑的副本，不会自动合并上游。资源的 update-interval 只让客户端刷新本仓库文件。
原项目作者及来源信息保留在每份列表顶部。
仓库已有 config/recommended.conf、config/extended.conf 及 rules/ 下的兼容模块保持原样；本次使用仓库根目录的列表。
