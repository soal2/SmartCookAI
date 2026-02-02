# 🍳 SmartCook AI - 智能食谱生成器

> 通过 AI 将剩余食材转化为创意食谱

<div align="center">

[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB?style=flat-square&logo=react)](https://reactjs.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-121212?style=flat-square)](https://langchain.com/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.1-06B6D4?style=flat-square&logo=tailwindcss)](https://tailwindcss.com/)

</div>

## 📖 项目简介

SmartCook AI 是一个智能食谱生成器，旨在解决"不知道吃什么"和"食材浪费"的痛点。通过输入手头的食材，AI 会为您生成创意且可执行的美味食谱。

### 核心功能

- 🤖 **AI 智能生成**: 基于 Dashscope (Qwen) + LangChain，生成个性化食谱
- 🥗 **食材管理**: 支持快速录入、分类和状态管理
- 📝 **多维筛选**: 按菜系、口味、场景、技能等级筛选
- ⭐ **收藏夹**: 自定义分组管理喜爱的食谱
- 🛒 **购物清单**: 智能生成缺失食材的购物清单
- 🔄 **食材替代**: AI 推荐相似食材替代方案

## 🏗️ 技术架构

### 后端 (Flask)
- **框架**: Flask 3.0 + SQLAlchemy
- **AI 引擎**: LangChain + Dashscope (Qwen)
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **API**: RESTful API + Flask-CORS

### 前端 (React)
- **框架**: React 19 + TypeScript
- **构建工具**: Vite 7
- **样式**: TailwindCSS 4
- **路由**: React Router DOM 7
- **HTTP 客户端**: Axios

### 架构特点
- 前后端分离
- 三层架构 (Routes → Services → Models)
- 速率限制 (Flask-Limiter)
- 统一的 API 响应格式

## 🚀 快速开始

### 前置要求
- Python 3.8+
- Node.js 18+
- Dashscope API Key ([获取地址](https://dashscope.console.aliyun.com/))

### 后端启动

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加 DASHSCOPE_API_KEY

# 初始化数据库
python init_db.py

# 启动服务 (默认端口 5000)
python run.py
```

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器 (端口 5173)
npm run dev
```

访问 http://localhost:5173 开始使用！

## 📚 项目文档

- [API 接口文档](backend/docs/API_DOCUMENTATION.md)
- [产品需求文档 PRD](backend/SmartCookAI.md)
- [P0 实现总结](backend/docs/P0_IMPLEMENTATION_SUMMARY.md)
- [测试文档](backend/docs/TESTING_README.md)
- [AI Agent 开发指南](.github/copilot-instructions.md)

## 🧪 测试

```bash
cd backend

# 快速 AI 功能测试
./quick_test.sh

# 完整测试套件
cd testing && python run_all_tests.py
```

## 📁 项目结构

```
SmartCookAI/
├── backend/              # Flask 后端
│   ├── app/
│   │   ├── models/       # SQLAlchemy 数据模型
│   │   ├── routes/       # API 路由
│   │   └── services/     # 业务逻辑层
│   ├── docs/            # 技术文档
│   └── testing/         # 测试文件
├── frontend/            # React 前端
│   ├── src/
│   │   ├── components/  # React 组件
│   │   ├── pages/       # 页面组件
│   │   ├── services/    # API 调用层
│   │   └── utils/       # 工具函数
└── .github/            # GitHub 配置
    └── copilot-instructions.md
```

## 🎯 核心特性

### 1. AI 食谱生成
- 单次生成 3-5 个创意方案
- 明确标注[已有]和[需补充]的食材
- 结构化展示难度/时间/热量

### 2. 智能筛选
- **菜系**: 中式/西式/日韩/东南亚
- **口味**: 酸/甜/苦/辣/咸/清淡
- **场景**: 早餐/快手菜(15min)/硬菜(1h+)
- **技能**: 新手/进阶

### 3. 食材管理
- 分类选择面板 (蔬菜/肉禽/海鲜/主食/调料)
- 智能搜索和模糊匹配
- 量词与状态标注 (新鲜/冷冻/常温/剩余)

## 🔧 配置说明

### 环境变量 (backend/.env)
```env
DASHSCOPE_API_KEY=sk-your-api-key
FLASK_DEBUG=True
FLASK_PORT=5000
```

### 环境变量 (frontend/.env)
```env
VITE_API_BASE_URL=http://localhost:5001/api
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m '添加某个特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 开源协议

本项目采用 MIT 协议 - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

**soal2** - [GitHub](https://github.com/soal2)

## 🙏 致谢

- [Dashscope (Qwen)](https://dashscope.console.aliyun.com/) - AI 模型支持
- [LangChain](https://langchain.com/) - LLM 框架
- [Flask](https://flask.palletsprojects.com/) - 后端框架
- [React](https://reactjs.org/) - 前端框架

---

<div align="center">
Made with ❤️ by soal2
</div>
