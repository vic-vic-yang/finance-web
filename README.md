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

`www.equitick.top` 使用 Let's Encrypt 证书，当前已改为 webroot 验证并由 Certbot 定时器自动续期，不需要手工添加 DNS TXT 记录。

服务器检查命令：

```bash
certbot certificates
systemctl status certbot-renew.timer
certbot renew --dry-run
```

Nginx 必须保留 `/.well-known/acme-challenge/` 到 `/var/www/certbot` 的公开访问规则，不能返回 403 或被重定向到业务鉴权页面。

## 发布前检查

- 首页、下载二维码与 APK 下载链接可用。
- `/privacy/`、`/terms/`、`/sdk/` 可直接访问。
- `robots.txt` 与 `sitemap.xml` 中使用正式 HTTPS 域名。
- 页面未公开个人住址、身份证号、私人电话等敏感信息。
