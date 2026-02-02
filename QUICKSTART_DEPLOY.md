# 🚀 GitHub Pages 快速配置清单

## ✅ 第一步：启用 GitHub Pages

1. 访问仓库设置页面：
   ```
   https://github.com/soal2/SmartCookAI/settings/pages
   ```

2. 在 **"Build and deployment"** 部分：
   - **Source**: 选择 `GitHub Actions` （不是 Deploy from a branch）

3. 保存设置

## ✅ 第二步：配置后端 API 地址

编辑 `frontend/.env.production` 文件，将后端 API 地址改为实际地址：

```env
# 默认配置（需要修改）
VITE_API_BASE_URL=https://your-backend-api.com/api

# 修改为您的实际后端地址，例如：
VITE_API_BASE_URL=https://api.smartcook.com/api
```

如果暂时没有部署后端，可以先使用本地地址测试：
```env
VITE_API_BASE_URL=http://localhost:5001/api
```

## ✅ 第三步：推送更改触发部署

```bash
# 如果修改了 .env.production
git add frontend/.env.production
git commit -m "配置生产环境 API 地址"
git push origin main
```

代码推送后会自动触发部署！

## ✅ 第四步：查看部署状态

1. 访问 Actions 页面：
   ```
   https://github.com/soal2/SmartCookAI/actions
   ```

2. 查看 **"Deploy to GitHub Pages"** workflow

3. 等待部署完成（通常需要 2-3 分钟）

## ✅ 第五步：访问您的应用

部署成功后访问：
```
https://soal2.github.io/SmartCookAI/
```

---

## 📝 注意事项

### ⚠️ 后端部署
GitHub Pages 只能部署静态网站（前端），后端需要单独部署到：
- 阿里云 / 腾讯云服务器
- Vercel / Railway 等云平台
- 使用 Docker 容器化部署

### ⚠️ CORS 配置
确保后端允许来自 GitHub Pages 的跨域请求：

```python
# backend/config.py
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://soal2.github.io').split(',')
```

或在 `.env` 文件中配置：
```env
CORS_ORIGINS=https://soal2.github.io,http://localhost:5173
```

### ⚠️ API Key 安全
不要在前端代码或 `.env.production` 中暴露敏感信息（如 DASHSCOPE_API_KEY），API Key 应该只在后端使用。

---

## 🔄 自动部署流程

每次推送到 `main` 分支时：
1. GitHub Actions 自动触发
2. 安装依赖并构建前端
3. 部署到 GitHub Pages
4. 更新线上应用

手动触发部署：
1. 访问 Actions 页面
2. 选择 "Deploy to GitHub Pages" workflow
3. 点击 "Run workflow"

---

## 🐛 常见问题

### 问题：页面显示 404
**解决方案**：
- 确认 GitHub Pages 已启用
- 确认 Source 选择了 "GitHub Actions"
- 查看 Actions 页面确认部署成功

### 问题：API 请求失败
**解决方案**：
- 检查 `.env.production` 中的 API 地址
- 确认后端已部署且可访问
- 检查后端 CORS 配置
- 使用浏览器开发者工具查看具体错误

### 问题：样式或资源加载失败
**解决方案**：
- 检查 `vite.config.ts` 中的 `base` 配置
- 确保设置为 `/SmartCookAI/`
- 重新构建并部署

---

## 📚 相关文档

- [完整部署指南](DEPLOYMENT.md)
- [GitHub Pages 官方文档](https://docs.github.com/en/pages)
- [Vite 部署指南](https://vitejs.dev/guide/static-deploy.html)

---

配置完成后，您的应用就可以在线访问了！🎉
