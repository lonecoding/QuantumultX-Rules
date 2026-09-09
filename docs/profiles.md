# 完整配置与策略组选择

标准版和扩展版直接引用上游分流列表，本项目负责 Quantumult X 策略组、资源绑定和配置生成。
配置面向中国大陆网络环境，帮助用户用自己的订阅完成日常分流。
不含私人订阅、账号、解密证书或需要登录的脚本。海外常驻用户应调整 DNS、国内直连
和最终策略；不存在适合所有网络环境的固定默认值。

## 直接导入

通常选择标准版；需要为不同 AI 或流媒体服务分别选节点时选择扩展版。
需要其他策略组组合，见下方“按需组合策略组”。

标准版（推荐）：

```text
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/recommended.conf
```

扩展版：

```text
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/config/extended.conf
```

1. 先在 Quantumult X 备份当前配置，再导入其中一份完整配置。
2. 编辑 `[server_remote]`，添加自己的订阅。将下面的 example.com 地址替换为真实地址，
   若从配置注释行复制，去掉行首 `#`：

   ```ini
   https://example.com/subscription, tag=Servers, update-interval=86400, opt-parser=true, enabled=true
   ```

   多个订阅各写一行，并使用不同 `tag`，例如 Servers-A、Servers-B。
   只在设备中填写真实链接；不要提交到 GitHub 或公开的问题报告。
3. 下载或刷新解析器、节点和全部分流资源。首次下载需要能访问 GitHub 原始文件的网络；
   若下载失败，先使用已有可用连接下载，再切换新配置。
4. 在 `Proxies` 中手动选择一个可用节点；使用规则分流模式。
5. 测试国内网站、AI、视频和通信服务，在请求日志核对实际命中的列表及策略。

解析器沿用你正在使用的 [KOP-XIAO / Shawn resource-parser.js](https://github.com/KOP-XIAO/QuantumultX/blob/master/Scripts/resource-parser.js)，
通过 `resource_parser_url` 引用，不复制为本项目原创代码。需要转换的节点订阅启用
`opt-parser=true`；原生 Quantumult X 订阅可以省略该参数。解析器支持的输入格式和
客户端支持的节点协议共同决定能否导入，转换不能让客户端支持原本不支持的协议。

## 两种预设如何选择

| 策略组 | 初始候选 / 用途 | 哪些预设有独立组 |
| --- | --- | --- |
| Proxies | 汇集全部订阅节点，首次使用时手动选节点 | 全部 |
| 🎯Direct | 固定 direct，始终直连 | 全部 |
| AdBlock | 广告域名：reject 拦截 / direct 放行 | 全部 |
| Hijacking | 防劫持：reject 拦截 / direct 放行 | 全部 |
| ✈️Final | Proxies；处理未命中规则的流量 | 全部 |
| AI | Proxies | 标准、扩展 |
| Google、Telegram、TikTok | Proxies | 标准、扩展 |
| YouTube | Google；未选择 Google 组时为 Proxies | 标准、扩展 |
| Apple | 🎯Direct | 标准、扩展 |
| ChatGPT、Claude、Gemini、Copilot | AI；可以各选不同节点 | 扩展 |
| Netflix、Spotify、AppleTV、AppleNews | Proxies | 扩展 |
| Microsoft | 🎯Direct | 扩展 |

标准版 11 组，扩展版 20 组。全部使用静态手动选择，客户端可能保留同名组
之前的选择，导入后请确认实际选择。服务组提供全部订阅节点，可以直接为 AI 选择一个
可用节点，同时让 YouTube 使用另一个节点；Proxies 的默认选择不必随之改变。
节点名称请避免与策略组同名。

**减少独立组不等于停用服务规则。** 未选择独立组的 ChatGPT / Claude / Gemini / Copilot，若有
AI 组就跟随 AI，否则跟随 Proxies；YouTube 优先跟随已有的 Google 组，其他海外服务跟随 Proxies。Apple / Microsoft
没有独立组时仍跟随 🎯Direct。国内 China 列表、中国 IP 和局域网绑定内置 `direct`，
不创建 LAN 或 China 策略组。
🎯Direct 本身也只有 direct 候选，不会把选择直连的服务连带切换为代理。

AdBlock 控制上游 AdvertisingLite 广告列表；Hijacking 独立控制上游防劫持列表。两个组默认
reject，切换其中一个不会改变另一个的设置。选择 direct 时，对应
列表匹配到的请求会直连，不会重新交给后续代理规则；需要让某个误拦域名走代理时，
在 `[filter_local]` 添加精确域名与对应策略，或禁用命中的资源后对照验证。
拦截范围是域名 / IP 规则，不能承诺去除 YouTube 视频广告等同域名广告。

## 厂商特殊服务

标准版已启用 AppleTV / AppleNews 独立服务规则并绑定 Proxies，Apple 通用服务仍默认直连。
扩展版显示 AppleTV、AppleNews 两个独立组，默认 Proxies，可分别选择节点。
它们的远程列表排在 Apple 通用列表之前；具体匹配仍以客户端日志为准。

Copilot 直接使用上游 Copilot.list。标准版默认跟随 AI；扩展版有 Copilot 独立组，默认跟随 AI。
自定义配置若没有 AI 组则跟随 Proxies。OpenAI、Claude、Gemini 排在 Copilot 前，Copilot
排在 Microsoft 通用列表前。上游 Copilot 包含共享 OpenAI 域名及 IP-ASN 范围，可能覆盖
其他服务，分组不能保证按应用完全隔离，请根据实际命中调整资源或策略。

来源：[AppleTV](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/QuantumultX/AppleTV/AppleTV.list)、
[AppleNews](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/QuantumultX/AppleNews/AppleNews.list)、
[Copilot](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/QuantumultX/Copilot/Copilot.list)。
客户端需支持引用列表中的规则类型，包括 IP-ASN；使用当前版本并确认资源加载无错误。

拦截列表可能重叠，放行一个列表不保证其他列表也会放行相同域名。出现误拦请根据
日志确认命中来源，为具体域名设置所需策略。Apple 服务可能共享接口；独立组不保证
绕过地区、账号或设备限制。

## 按需组合策略组

不需要编程即可从两种预设中选一份导入。需要其他组合的用户，在下载本仓库后，
使用 Node.js 22 或更新版本运行自带的 JavaScript 生成器；无需安装第三方依赖。
以下命令在仓库根目录执行，输出到仓库外的新文件：

```bash
node scripts/generate_profiles.js --interactive > ../my-quantumultx.conf
```

按提示输入组名，如 `AI,Telegram,YouTube`，就会生成基础 5 组加这 3 个独立组。
也可以直接指定：

```bash
node scripts/generate_profiles.js --groups AI,Telegram,YouTube > ../my-quantumultx.conf
```

可选组名：`AI,ChatGPT,Claude,Gemini,Copilot,YouTube,Telegram,TikTok,Netflix,Spotify,AppleTV,AppleNews,Microsoft,Apple,Google`。
`--groups none` 只保留基础组。未知名称或重复组名会报错。
生成器只处理本地配置，不获取订阅、不联网、不收集使用数据。生成后导入文件，再在
设备上添加自己的订阅。此工具是维护及生成工具，不是放进 `resource_parser_url` 的客户端解析器。

## 分流来源与网络默认值

配置中的资源组织顺序：局域网 → 防劫持 / 广告 → AI 等具体服务 → Google 等厂商 →
Global → China → 中国 IP 区域规则，未命中使用 Final。它表达配置组织意图，不能替代
Quantumult X 的实际匹配逻辑；域名 / IP 规则、客户端优化和重叠资源都可能影响结果。

- 服务上游：OpenAI、Claude、Gemini、Copilot、YouTube、Telegram、TikTok、Netflix、Spotify、AppleTV、AppleNews、Microsoft、Apple、Google。
- 广告和防劫持上游：AdvertisingLite、Hijacking；通用分流上游：Global、China。
- 以上均直接引用 [blackmatrix7](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/QuantumultX)，不在仓库内复制或维护其规则正文。
- AI 是汇总策略组，不依赖一个名为 AI 的规则文件；当前汇总上述四个 AI 服务列表。其他 AI 网站可能命中 Global 或 Final，不保证归入 AI 组。
- 局域网使用内置 `FILTER_LAN`，中国 IP 使用内置 `FILTER_REGION`，均绑定 direct，没有对应策略组。
  配置保留私网排除路由；IP 归属数据不等于服务所在国家，结果以请求日志为准。
- `[filter_local]` 默认只有 Final，用户可以在设备上添加自己的例外。
- DNS 保留系统 DNS，并添加 223.5.5.5 / 119.29.29.29；`no-ipv6` 让隧道 DNS 的 AAAA 查询失败，
  不代表禁用设备全部 IPv6。需要 IPv6 时可在设备配置中删除该项并重新验证。
- 保留私网排除路由，不限制 UDP 端口，也不强制把不支持 UDP 的代理流量改为直连。
- rewrite、task、mitm 留空；导入和分流不需要生成、安装或信任解密证书。

语法及默认行为参考 [Quantumult X 官方配置示例](https://github.com/crossutility/Quantumult-X/blob/master/sample.conf)。
所有远程规则每日请求更新，实际刷新由客户端控制。上游解析器和列表跟随各自 master；
即使导入 release 标签下的配置，内部这些地址仍会更新。
需要固定快照时，分别把每个资源 URL 的分支替换为已核对的提交 SHA。
上游资源直接引用，版权和许可证属于原作者，不计为本项目自维护规则。

## 更新、迁移与问题处理

full.conf / daily.conf 是 recommended.conf 的兼容入口，内容保持一致，同样直接加载上游。
迁移或更新完整配置时，备份后复制自己的订阅与
必要的精确域名例外，刷新全部资源，并检查同名策略组的实际选择。
规则订阅可以自动刷新；整体配置的结构更新需用户主动导入或合并。
升级时确认 🎯Direct 只有 direct 候选；AdBlock 和 Hijacking 分别选择 reject 或 direct，
并核对 YouTube 跟随 Google，以及 AppleTV、AppleNews、Copilot 的实际命中。
完整配置的规则覆盖遵循上游。上游广告列表的覆盖范围较广，出现误拦时检查对应拦截组。
不要把带有自己订阅的配置设置为未经检查的整份覆盖更新。

若 AI / 视频失败，先检查选用节点及实际匹配规则；地区和账号限制无法靠分流规则消除。
若节点为空，确认订阅链接、解析器下载和 opt-parser 参数；若国内访问异常，检查 DNS
和命中的规则。误拦优先根据请求日志添加精确例外，恢复原本需要的策略；有问题可恢复备份。

## 维护与验证范围

原创生成逻辑在 [config-builder.js](../scripts/config-builder.js)，命令入口在
[generate_profiles.js](../scripts/generate_profiles.js)。维护者修改目录或默认策略后执行：

```bash
node scripts/generate_profiles.js --write
node scripts/generate_profiles.js --check
node --test tests/config-builder.test.js
python scripts/validate_rules.py
python scripts/generate_readme.py --check
python scripts/generate_compat.py --check
python scripts/generate_daily.py --check
python scripts/check_routing.py
python -m unittest discover -s tests -v
```

CI 检查生成内容、全部 32768 种策略组组合的有效引用与循环、规则保留、默认绑定和命令行错误。
定时 / 手动网络检查覆盖所有配置中的外部 URL。34 个路由样例用于 tests/fixtures/standalone.conf 中的独立规则兼容测试；
新预设没有模拟上游全部规则、DNS、区域数据或客户端匹配引擎。

**尚未完成 Quantumult X 实机验证。** 使用有效订阅完成首次导入、资源刷新、国内直连、
AI / 视频独立节点、IPv6 场景、广告误拦恢复和配置升级后，再记录客户端版本及验证结果。
自动检查通过不代表已经实测服务可用。
