
# 背景

先吐个槽，dnsmasq很轻盈，但dnsmasq记录不能动态更新。if你懂golang，你可以考虑使用dnsmasq＋skydns方案，k8s用的就是这个方案。但目前本人不会golang。。。（尴尬）

so, skydns对我来说，不太好搞。基于以上背景，写了一个python的dns——ParasiticDNS。Parasitic本意是寄生的意思，当然也就意味着不建议独立使用本dns做域名解析服务。不是不能胜任，而是没有dnsmasq那么稳定高效（我不是在粉dnsmasq）。建议与dnsmasq配合使用（好吧还是粉了一下dnsmasq），ParasiticDNS作为dnsmasq的上游dns。

---

# 用法

### 运行

`docker-compose up -d`


### 停止

`docker-compose down --rmi all` or `docker-compose down`


---

# 参考&鸣谢

* [apple_dns](https://github.com/anpengapple/apple_dns)

