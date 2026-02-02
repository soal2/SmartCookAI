# SmartCook AI - AI Agent 开发指南

## 项目概述
SmartCook AI 是一个智能食谱生成器，通过 AI 将用户的剩余食材转化为创意食谱。采用前后端分离架构，基于阿里云 Dashscope (Qwen) 的 LangChain 集成进行 AI 生成。

**技术栈:**
- 后端: Flask + SQLAlchemy + LangChain + Dashscope (Qwen)
- 前端: React 19 + TypeScript + Vite + TailwindCSS 4
- 数据库: SQLite (开发环境)

## 核心架构模式

### 后端三层架构 (Routes → Services → Models)
遵循严格的职责分离：
- **Routes** (`app/routes/`): API 端点定义，仅负责参数验证和 HTTP 响应
- **Services** (`app/services/`): 业务逻辑和 AI 调用，如 `RecipeGenerationService`
- **Models** (`app/models/`): SQLAlchemy ORM 模型，包含 `to_dict()` 方法用于序列化

**示例：** 添加新功能时，先在 `services/` 实现逻辑，然后在 `routes/` 暴露 API，最后在前端 `services/api.ts` 添加调用方法。

### AI 生成流程
核心服务类 `RecipeGenerationService` 位于 [app/services/recipe_service.py](backend/app/services/recipe_service.py)：
```python
# 关键方法链
generate_recipes() → _build_system_prompt() → _build_user_prompt() → model.invoke() → _parse_response()
```
- 使用 LangChain 的 `ChatTongyi` 模型连接 Qwen
- Prompt 构建采用 System + User 消息分离模式
- 返回 JSON 结构在 `_parse_response()` 中使用正则 + JSON 解析

### 配置管理
所有配置集中在 [backend/config.py](backend/config.py)：
- 环境变量通过 `python-dotenv` 加载（需复制 `.env.example` 为 `.env`）
- **必需配置:** `DASHSCOPE_API_KEY=sk-...`
- 模型参数: `MODEL_NAME='qwen-turbo'`, `TEMPERATURE=0.8`, `MAX_TOKENS=2000`
- 允许值常量用于输入验证：`ALLOWED_CUISINES`, `ALLOWED_STATES` 等

## 关键开发工作流

### 启动服务
```bash
# 后端 (端口 5000/5001)
cd backend
python run.py

# 前端 (端口 5173)
cd frontend
npm run dev
```

### 测试执行
```bash
# 快速 AI 功能测试
cd backend && ./quick_test.sh

# 完整测试套件
cd backend/testing && python run_all_tests.py
```
测试文件位于 `backend/testing/`，包含 AI 生成、性能、端到端测试。

### 数据库操作
```bash
# 初始化/重置数据库
cd backend && python init_db.py
```
使用 SQLAlchemy，迁移需手动修改模型后重新初始化（无 Alembic）。

## 项目特定约定

### API 响应格式
统一返回结构（见 [docs/API_DOCUMENTATION.md](backend/docs/API_DOCUMENTATION.md)）：
```json
{
  "success": true,
  "data": {},      // 或 "items", "recipe" 等语义化键
  "count": 0       // 列表接口返回总数
}
```
错误响应: `{"error": "错误描述"}` + 对应 HTTP 状态码

### 前端状态管理
- **无全局状态库**：使用 React Hooks (`useState`, `useEffect`) 本地管理
- API 调用集中在 [src/services/api.ts](frontend/src/services/api.ts)，使用 Axios 实例
- 环境变量: `VITE_API_BASE_URL` 配置后端地址（默认 `http://localhost:5001/api`）

### 数据模型关联
关键表关系（见 `app/models/`）：
- `Recipe` ←→ `Favorite` (1:N) - 食谱可被多个收藏夹收藏
- `Recipe` ←→ `RecipeStepProgress` (1:N) - 记录步骤完成状态
- `Ingredient` ←→ `ShoppingListItem` (N:M) - 通过 `recipe_id` 关联

### 中文优先
- 所有用户可见文本、日志、API 响应均使用**简体中文**
- 代码注释和文档也优先使用中文，代码标识符使用英文
- Prompt 工程采用中文 Few-shot 示例提升生成质量

## 集成要点

### LangChain + Dashscope 集成
```python
from langchain_community.chat_models import ChatTongyi
model = ChatTongyi(
    model_name=Config.MODEL_NAME,
    dashscope_api_key=Config.DASHSCOPE_API_KEY,
    temperature=Config.TEMPERATURE
)
```
- 使用 `langchain-community` 包而非 `langchain-openai`
- 需要阿里云 Dashscope API Key（免费额度见官网）

### 速率限制
使用 `flask-limiter` 全局限制：
- 默认: `200 per day`, `50 per hour`
- AI 生成端点: `10 per hour`（见 [routes/recipes.py](backend/app/routes/recipes.py#L59)）

### CORS 配置
开发环境允许所有来源（`origins: "*"`），生产环境需在 `Config.CORS_ORIGINS` 配置白名单。

## 常见陷阱

1. **忘记配置 `.env`**: 后端启动会警告但不会阻止，AI 生成会报错 401
2. **端口冲突**: 后端默认 5000，macOS AirPlay 占用时需改用 5001
3. **JSON 字段解析**: 模型存储的 `ingredients_json`, `steps_json` 需在 `to_dict()` 中使用 `json.loads()` 反序列化
4. **前端类型不匹配**: TypeScript 接口定义在 `api.ts` 中，需与后端响应结构一致

## 参考文档
- [产品需求文档 PRD](backend/SmartCookAI.md) - 完整产品功能规划
- [API 接口文档](backend/docs/API_DOCUMENTATION.md) - 所有端点详细说明
- [P0 实现总结](backend/docs/P0_IMPLEMENTATION_SUMMARY.md) - 核心功能实现细节
