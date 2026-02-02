# GitHub Pages 部署指南

## 前端自动部署配置

本项目已配置 GitHub Actions 自动部署前端到 GitHub Pages。

### 部署流程

1. **启用 GitHub Pages**
   - 访问仓库设置: https://github.com/soal2/SmartCookAI/settings/pages
   - 在 "Build and deployment" 部分
   - Source 选择: **GitHub Actions**

2. **配置后端 API 地址**
   
   编辑 `frontend/.env.production` 文件：
   ```env
   VITE_API_BASE_URL=https://your-backend-api.com/api
   ```
   
   将 `https://your-backend-api.com/api` 替换为您的实际后端地址。

3. **推送代码触发部署**
   ```bash
   git add .
   git commit -m "配置 GitHub Pages 部署"
   git push origin main
   ```

4. **查看部署状态**
   - 访问 Actions 页面: https://github.com/soal2/SmartCookAI/actions
   - 查看 "Deploy to GitHub Pages" workflow 的运行状态
   - 部署成功后，访问: https://soal2.github.io/SmartCookAI/

### 配置详情

#### Vite 配置 (frontend/vite.config.ts)
```typescript
base: process.env.NODE_ENV === 'production' ? '/SmartCookAI/' : '/'
```
- 生产环境使用 `/SmartCookAI/` 作为 base path
- 开发环境使用 `/` 根路径

#### GitHub Actions Workflow (.github/workflows/deploy.yml)
- **触发条件**: 推送到 `main` 分支或手动触发
- **构建步骤**: 
  1. 检出代码
  2. 安装 Node.js 20
  3. 安装依赖 (`npm ci`)
  4. 构建项目 (`npm run build`)
  5. 上传构建产物
- **部署步骤**: 部署到 GitHub Pages

### 环境变量

开发环境 (`frontend/.env`):
```env
VITE_API_BASE_URL=http://localhost:5001/api
```

生产环境 (`frontend/.env.production`):
```env
VITE_API_BASE_URL=https://your-backend-api.com/api
```

### 后端部署建议

由于 GitHub Pages 只能部署静态网站，后端需要单独部署。推荐方案：

1. **阿里云 ECS / 腾讯云**
   - 部署 Flask 应用
   - 配置 Nginx 反向代理
   - 启用 HTTPS

2. **Vercel / Railway**
   - 支持 Python Flask 应用
   - 自动 HTTPS
   - 免费额度

3. **Docker 容器化部署**
   ```bash
   # 创建 Dockerfile（在 backend 目录）
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "run.py"]
   ```

### CORS 配置

确保后端允许来自 GitHub Pages 的跨域请求：

```python
# backend/config.py
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://soal2.github.io').split(',')
```

### 故障排查

#### 问题 1: 页面 404
- 确认 GitHub Pages 已启用且 Source 选择了 "GitHub Actions"
- 检查 Actions 部署是否成功

#### 问题 2: API 请求失败
- 检查 `.env.production` 中的 API 地址是否正确
- 确认后端 CORS 配置允许来自 `soal2.github.io` 的请求
- 使用浏览器开发者工具检查网络请求

#### 问题 3: 刷新页面 404
这是 SPA 应用在 GitHub Pages 上的常见问题。解决方案：
1. 使用 Hash Router 替代 Browser Router（简单但 URL 不美观）
2. 添加 404.html 重定向（推荐）

#### 问题 4: 资源加载失败
- 检查 `vite.config.ts` 中的 `base` 配置
- 确保生产环境使用正确的 base path

### 手动部署

如果需要手动部署：

```bash
cd frontend
npm run build
# 将 dist 目录的内容上传到 GitHub Pages
```

### 自定义域名（可选）

1. 在仓库根目录创建 `frontend/public/CNAME` 文件
2. 添加您的域名，如: `smartcook.example.com`
3. 在域名提供商配置 DNS 记录指向 GitHub Pages

---

更新时间: 2026-02-02
