# AUTO-DNS

## 前言

[Cloudflare](https://www.cloudflare.com) 提供了 CDN 服务但是默认不能自选 IP，一般默认分配的 IP 超时、丢包严重，下载速度感人，几乎不能用。

通过 [Cloudflare IP 自选](https://www.ipv6s.com/basis/tunnel/202211052905.html) 这篇教程实现 IP 自选，这样你就可以将你的域名解析到你选定的
IP 了。

## 项目介绍

本项目会自动筛选出优质的 IP，然后更新你的域名解析记录，并提供了一些额外的功能。

## 准备工作

前面的教程提到了一些工具和服务，具体如下：

1. IP 选择工具，这里使用 [**XIU2**](https://github.com/XIU2)
   大佬的 [CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest) 这个工具；

2. 支持分运营商解析的 DNS 服务商，这里选择 [青云DNS](https://console.qingcloud.com/dns)。

## 项目配置

1. 下载 [IP 选择工具](https://github.com/XIU2/CloudflareSpeedTest/releases)
   ，根据机器的架构和系统选择合适的包。将压缩包解压到 `lib/cf` 目录下，文件目录结构如下：

```
auto-dns
└──lib
    └── cf
        ├── cfst_hosts.sh
        ├── CloudflareST
        ├── ip.txt
        ├── ipv6.txt
        └── 使用+错误+反馈说明.txt
```

2. 调整配置文件 [config.yml](config.yml) 参数，一些特别配置项：

```yaml
record: # 待更新的记录 id
  ids: !ENV ${RECORD_IDS} 
```

代表青云每个域名解析 IP 记录的 id，参考 [官方文档](https://docsv4.qingcloud.com/user_guide/site/dns/api/record/)。

---

```yaml
force_update:
  enabled: true # 是否启动强制更新
  interval: 7 # 更新间隔, 单位为 day. 默认为 7 天
```

该服务默认每天早上 `10` 点会检查域名当前对应 IP 超时和延迟，如果超时 `>10%` 或者延迟 `>300ms` 会重新选择优质 IP(两个)
并更新你的域名记录。
如果启动强制更新，表示 `7` 天后即使上面条件不满足也会自动更新你的域名记录。

---

```yaml
clash:
  enabled: true # 运行环境是否启动了 OpenClash
  host: !ENV ${CLASH_HOST}
  port: !ENV ${CLASH_PORT}
  user: !ENV ${CLASH_USER}
  passwd: !ENV ${CLASH_PASSWD}
```

表示服务运行环境的网络(一般都是家庭网络，因为这样的环境选出来的 IP 才有意义)是否 `畅通`。以我的环境为例：我是在树莓派里的
Docker
跑这个服务，并且这个 Docker 还跑了 OpenWRT，OpenWRT 里面安装了 OpenClash
服务，也就是说我的树莓派所处的网络环境是畅通的。网络畅通的条件下 [IP 选择工具](https://github.com/XIU2/CloudflareSpeedTest/releases)
给出的结果可能并不准确，所以需要提前将网络`阻塞`，这里将 OpenClash 关闭即可，IP 筛选出来后，OpenClash 将重新启动，这些都是代码自动完成的。

3. 复制 [.env.example](.env.example) 改名为 .env，然后填充这些环境变量，如果是宿主机运行该服务，需添加这些环境变量。

## 一些杂项

- OpenClash 运行模式设置为 Redir-Host，Fake-IP 模式会干扰测速。

## 启动服务

- Docker(推荐)

```shell
sudo docker compose up --build -d
```

## :sparkles: Star History :sparkles:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=doublewinter0/auto-dns&type=Date&theme=dark" />
  <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=doublewinter0/auto-dns&type=Date" />
  <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=doublewinter0/auto-dns&type=Date" />
</picture>

## 支持我
如果这个项目对你有所帮助，请给我一颗 ⭐️ 吧！
