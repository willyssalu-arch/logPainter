本目录用于存放本地 JS/CSS 依赖，供完全离线环境使用。

请在「有网络」时在项目根目录执行：
  .\fetch-vendor.ps1

脚本会将以下文件下载到此目录：
  - jquery.min.js
  - bootstrap.bundle.min.js
  - bootstrap.min.css
  - docx.min.js
  - FileSaver.min.js

下载完成后，index.html 将不再请求任何外网资源（除用户主动点击的链接外）。
