# 司库官网

纯静态响应式官网，无构建依赖，可由 Nginx 直接托管。

## 页面

- `/`：产品官网
- `/privacy/`：隐私政策
- `/terms/`：用户协议
- `/sdk/`：第三方服务与 SDK 清单

## 本地预览

在仓库根目录运行：

```powershell
python -m http.server 8088 -d website
```

访问 `http://localhost:8088/`。正式域名为 `https://www.equitick.top/`。

## 部署

官网已接入统一部署流程：

- 双击根目录 `部署服务.bat`，选择“仅官网”或“API + Admin + 官网”。
- 也可双击 `部署官网.bat`，只发布官网。
- 服务器目录为 `/opt/siku/website`，Nginx 配置为 `/etc/nginx/conf.d/siku.conf`。

正式域名使用独立站点 `https://www.equitick.top/`，不会占用 API/Admin 的
`https://finance.equitick.top/` 路由。

## HTTPS 证书

`www.equitick.top` 当前使用 Let's Encrypt 证书。由于首次签发使用 DNS TXT 校验，证书到期前需重新执行
DNS 校验续期，再重载 Nginx；可用 `certbot certificates` 查看有效期。
