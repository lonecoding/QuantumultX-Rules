# Upstream rules / 上游规则

## Template choice

| Template | Rule sources | Broad routing |
| --- | --- | --- |
| [full.conf](../config/full.conf) | This repository's 11 service modules | Unmatched traffic goes to Final; no general China-direct list |
| [daily.conf](../config/daily.conf) | The same modules plus three upstream lists | Hijacking rejects; Global uses Proxies; China uses direct; unmatched traffic still goes to Final |

Both templates use the same policy groups, base network settings and empty
subscription section. The daily template adds no GeoIP/FILTER_REGION rule, DNS
override, parser, rewrite, certificate, or personal domain exception. It is not
a complete reproduction of a personal configuration. Static groups retain
manual choices; the initial Final candidate is Proxies.

## Sources and ownership

These lists are maintained by
[blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script).
They are referenced directly; their contents are not copied, counted as our
own rules, or redistributed under this repository's license.

| List | Upstream file | Bound policy | Intended position |
| --- | --- | --- | --- |
| Hijacking | [Hijacking.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Hijacking/Hijacking.list) | reject | After LAN, before advertising and services |
| Global | [Global.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Global/Global.list) | Proxies | After specific service lists |
| China | [China.list](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/China/China.list) | direct | After Global, before FINAL fallback |

The imports use `force-policy` so upstream labels do not require additional
policy groups. Each requests a refresh interval of 86400 seconds. Hijacking is
a separate blocking source, not a replacement for our Advertising list.
Inspect the actual matched resource when troubleshooting a rejected request.

These URLs follow upstream `master` and may change independently of this project.
Pinning this repository to a release does not pin those external URLs. For a
reproducible personal configuration, replace upstream `master` with a reviewed
upstream commit SHA and verify all three files exist there. Keep the source
links and upstream notices when sharing modifications.

## 中文快速使用

日常模板的导入地址：

```text
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/daily.conf
```

1. 备份手机上当前的配置，再导入日常模板。
2. 在手机的 `[server_remote]` 中添加自己的订阅；模板不含任何私人订阅。
3. 刷新节点和规则资源，选择 Proxies 节点，确认各服务的策略。
4. 使用规则分流模式，在请求日志中核对命中的列表和最终策略。

日常模板保留本仓库自维护的 AI、YouTube、Telegram 等规则，只把 China、Global、
Hijacking 交给上游维护；它与全部使用 blackmatrix7 服务规则的个人配置并不相同。

China 列表命中的流量指定直连，Global 列表命中的流量指定 Proxies。
未命中的流量仍交给 ✈️Final。没有增加中国 IP 区域规则，不能理解为所有国内流量
一定直连。规则之间可能重叠，客户端匹配优化也可能影响优先级，请以实机日志为准。

原有 `full.conf` 和各个规则订阅地址继续可用。日常模板是可选入口，不需要强制迁移。
若出现问题，恢复备份，或暂时关闭日志中实际命中的上游列表进行对照；不要为了排障
把所有流量一律改为直连。

## Maintenance and verification

`config/daily.conf` is generated from `config/full.conf` and the three bindings in
`scripts/generate_daily.py`. After changing base settings or upstream bindings, run:

```bash
python scripts/generate_daily.py
python scripts/validate_rules.py
python scripts/generate_daily.py --check
python -m unittest discover -s tests -v
```

Offline checks verify the exact generated configuration, resource order,
force-policy bindings, and unchanged base settings. Network checks include all
three upstream URLs. The existing 34 routing cases apply to `full.conf` only;
they do not simulate external lists or validate daily-template routing.
No upstream snapshot is bundled; offline CI does not download upstream rules.
On-device verification of the new template is still pending. Test domestic
access, AI services, streaming and false-positive recovery before relying on it
for everyday use.
