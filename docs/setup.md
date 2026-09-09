# 配置与独立规则使用

新用户使用 [完整配置指南](profiles.md)：选择标准版或扩展版，添加自己的订阅，刷新资源并选择节点。
所有完整配置直接加载上游规则。full.conf、daily.conf 与标准版内容一致。

## 向自己的配置添加独立规则

已有用户仍可使用 [兼容目录](legacy-rule-files.md) 中的独立规则文件。它们不属于完整配置的上游加载链路。
添加前先查看文件内部的策略名称，并将资源绑定到自己配置中已有的组：

```ini
[filter_remote]
https://raw.githubusercontent.com/lonecoding/QuantumultX-Rules/main/rules/YouTube/YouTube.list, tag=YouTube, force-policy=YouTube, update-interval=86400, enabled=true
```

`force-policy` 会覆盖文件内部的策略标签；已有组名不同时，修改为你的实际组名。
不要仅因添加了规则文件，就重复创建一个不需要的策略组。
LAN 地址规则可以绑定 `force-policy=direct`，不需要 LAN 策略组。

## 误拦和精确例外

先查看请求日志，确认实际命中的资源。需要直连的域名明确指定 direct，需要代理的域名指定
已有的服务组。示例仅使用保留域名，不对应真实问题：

```ini
[filter_local]
host, ads.example.com, direct
host, assets.example.net, AI
final, ✈️Final
```

将例外放在 Final 之前，不要重复添加 `[filter_local]` 区段；替换成已确认的域名和实际策略组。
必要时禁用日志中命中的资源进行对照，恢复需要的策略后再次检查。
具体匹配以 Quantumult X 日志为准，静态规则检查不能替代实测。

## 升级与固定版本

备份已有配置，再导入新配置，或合并所需区段；确认个人订阅与例外仍在，刷新资源并检查策略选择。
仅刷新远程规则不会同步策略组定义。需要回退时恢复设备备份。

可以使用发布标签下的配置，但内部上游 master 地址仍会更新。需要固定全部资源时，分别把
每个 URL 的分支替换成已核对的提交 SHA，并确认文件可以下载。
请勿把带有订阅链接、账号或密钥的配置提交到仓库。
