# SmartCook AI - API 接口文档

## 目录

- [基础信息](#基础信息)
- [通用说明](#通用说明)
- [健康检查](#健康检查)
- [1. 食谱管理 API](#1-食谱管理-api)
- [2. 食材管理 API](#2-食材管理-api)
- [3. 收藏夹管理 API](#3-收藏夹管理-api)
- [4. 购物清单 API](#4-购物清单-api)
- [数据模型](#数据模型)
- [错误处理](#错误处理)

---

## 基础信息

**Base URL**: `http://localhost:5000`

**API 前缀**: `/api`

**Content-Type**: `application/json`

**字符编码**: UTF-8

---

## 通用说明

### 响应格式

所有成功的响应都遵循以下格式：

```json
{
  "success": true,
  "data": {},  // 或 "items": [], "recipe": {}, 等
  "count": 0   // 可选，列表类接口会返回
}
```

### 错误响应

```json
{
  "error": "错误信息描述"
}
```

HTTP 状态码：
- `200` - 成功
- `201` - 创建成功
- `400` - 请求参数错误
- `404` - 资源不存在
- `500` - 服务器内部错误

---

## 健康检查

### 检查服务状态

**接口**: `GET /health`

**响应示例**:
```json
{
  "status": "healthy",
  "service": "SmartCook AI Backend"
}
```

---

## 1. 食谱管理 API

### 1.1 生成食谱

使用 AI 根据食材和筛选条件生成创意食谱。生成的食谱会自动保存到历史记录。

**接口**: `POST /api/recipes/generate`

**请求体**:
```json
{
  "ingredients": [
    {
      "name": "鸡蛋",
      "quantity": "6个",
      "state": "新鲜"
    },
    {
      "name": "番茄",
      "quantity": "2个",
      "state": "新鲜"
    }
  ],
  "filters": {
    "cuisine": "中式",
    "taste": "清淡",
    "scenario": "快手菜",
    "skill": "新手"
  }
}
```

**参数说明**:
- `ingredients` (必填): 食材列表
  - `name`: 食材名称
  - `quantity`: 数量
  - `state`: 状态（新鲜/冷冻/常温）
- `filters` (可选): 筛选条件
  - `cuisine`: 菜系（中式/西式/日韩/东南亚）
  - `taste`: 口味（酸/甜/苦/辣/咸/清淡）
  - `scenario`: 场景（早餐/快手菜/硬菜）
  - `skill`: 技能等级（新手/进阶）

**响应示例**:
```json
{
  "success": true,
  "recipes": [
    {
      "id": 1,
      "name": "番茄炒蛋",
      "description": "经典家常菜，酸甜可口",
      "difficulty": "新手",
      "cooking_time": "15分钟",
      "calories": "约200千卡",
      "cuisine": "中式",
      "taste": "酸甜",
      "scenario": "快手菜",
      "skill_level": "新手",
      "ingredients": [
        {
          "name": "鸡蛋",
          "quantity": "3个",
          "status": "[已有]"
        },
        {
          "name": "番茄",
          "quantity": "2个",
          "status": "[已有]"
        },
        {
          "name": "盐",
          "quantity": "适量",
          "status": "[需补充]"
        }
      ],
      "steps": [
        "番茄洗净切块",
        "鸡蛋打散",
        "热锅倒油，炒鸡蛋至凝固盛出",
        "锅中加油，炒番茄至软烂",
        "加入鸡蛋翻炒均匀，加盐调味"
      ],
      "tags": ["家常菜", "快手", "下饭"],
      "created_at": "2026-01-30T10:00:00"
    }
  ],
  "count": 1
}
```

### 1.2 获取历史记录

获取所有生成过的食谱历史。

**接口**: `GET /api/recipes/history`

**查询参数**:
- `limit` (可选): 返回数量限制，默认 20

**请求示例**:
```
GET /api/recipes/history?limit=10
```

**响应示例**:
```json
{
  "success": true,
  "history": [
    {
      "id": 1,
      "name": "番茄炒蛋",
      "description": "经典家常菜",
      "difficulty": "新手",
      "cooking_time": "15分钟",
      "calories": "约200千卡",
      "created_at": "2026-01-30T10:00:00"
    }
  ],
  "count": 1
}
```

### 1.3 获取单个食谱详情

获取指定食谱的完整信息，包括步骤完成进度。

**接口**: `GET /api/recipes/<id>`

**路径参数**:
- `id`: 食谱 ID

**请求示例**:
```
GET /api/recipes/1
```

**响应示例**:
```json
{
  "success": true,
  "recipe": {
    "id": 1,
    "name": "番茄炒蛋",
    "description": "经典家常菜",
    "difficulty": "新手",
    "cooking_time": "15分钟",
    "calories": "约200千卡",
    "cuisine": "中式",
    "taste": "酸甜",
    "scenario": "快手菜",
    "skill_level": "新手",
    "ingredients": [...],
    "steps": [...],
    "tags": ["家常菜", "快手", "下饭"],
    "created_at": "2026-01-30T10:00:00",
    "step_progress": [
      {
        "step_index": 0,
        "is_completed": true,
        "completed_at": "2026-01-30T10:05:00"
      }
    ]
  }
}
```

### 1.4 删除食谱

从历史记录中删除指定食谱。

**接口**: `DELETE /api/recipes/<id>`

**路径参数**:
- `id`: 食谱 ID

**响应示例**:
```json
{
  "success": true,
  "message": "删除成功"
}
```

### 1.5 获取步骤完成状态

获取食谱的烹饪步骤完成进度。

**接口**: `GET /api/recipes/<id>/progress`

**路径参数**:
- `id`: 食谱 ID

**响应示例**:
```json
{
  "success": true,
  "progress": [
    {
      "id": 1,
      "recipe_id": 1,
      "step_index": 0,
      "is_completed": true,
      "completed_at": "2026-01-30T10:05:00"
    },
    {
      "id": 2,
      "recipe_id": 1,
      "step_index": 1,
      "is_completed": false,
      "completed_at": null
    }
  ]
}
```

### 1.6 更新步骤完成状态

标记某个烹饪步骤为已完成或未完成。

**接口**: `POST /api/recipes/<id>/progress`

**路径参数**:
- `id`: 食谱 ID

**请求体**:
```json
{
  "step_index": 0,
  "is_completed": true
}
```

**参数说明**:
- `step_index` (必填): 步骤索引（从 0 开始）
- `is_completed` (必填): 是否完成

**响应示例**:
```json
{
  "success": true,
  "progress": {
    "id": 1,
    "recipe_id": 1,
    "step_index": 0,
    "is_completed": true,
    "completed_at": "2026-01-30T10:05:00"
  }
}
```

---

## 2. 食材管理 API

### 2.1 获取所有食材

获取用户所有的食材列表。

**接口**: `GET /api/ingredients`

**响应示例**:
```json
{
  "success": true,
  "ingredients": [
    {
      "id": 1,
      "name": "鸡蛋",
      "quantity": "6个",
      "state": "新鲜",
      "category": "主食",
      "storage_location": "fridge",
      "is_common": true,
      "created_at": "2026-01-30T09:00:00",
      "updated_at": "2026-01-30T09:00:00"
    }
  ],
  "count": 1
}
```

### 2.2 获取常用食材

获取标记为常用的食材列表。

**接口**: `GET /api/ingredients/common`

**响应示例**:
```json
{
  "success": true,
  "ingredients": [
    {
      "id": 1,
      "name": "鸡蛋",
      "quantity": "6个",
      "state": "新鲜",
      "category": "主食",
      "storage_location": "fridge",
      "is_common": true,
      "created_at": "2026-01-30T09:00:00",
      "updated_at": "2026-01-30T09:00:00"
    }
  ],
  "count": 1
}
```

### 2.3 按分类获取食材

根据食材分类筛选。

**接口**: `GET /api/ingredients/by-category`

**查询参数**:
- `category` (必填): 分类名称（蔬菜/肉禽/海鲜/主食/调料）

**请求示例**:
```
GET /api/ingredients/by-category?category=蔬菜
```

**响应示例**:
```json
{
  "success": true,
  "ingredients": [
    {
      "id": 2,
      "name": "番茄",
      "quantity": "2个",
      "state": "新鲜",
      "category": "蔬菜",
      "storage_location": "fridge",
      "is_common": false,
      "created_at": "2026-01-30T09:00:00",
      "updated_at": "2026-01-30T09:00:00"
    }
  ],
  "count": 1
}
```

### 2.4 按存储位置获取食材

根据存储位置筛选食材。

**接口**: `GET /api/ingredients/by-storage`

**查询参数**:
- `storage` (必填): 存储位置（fridge/freezer/pantry）

**请求示例**:
```
GET /api/ingredients/by-storage?storage=fridge
```

**响应示例**:
```json
{
  "success": true,
  "ingredients": [
    {
      "id": 1,
      "name": "鸡蛋",
      "quantity": "6个",
      "state": "新鲜",
      "category": "主食",
      "storage_location": "fridge",
      "is_common": true,
      "created_at": "2026-01-30T09:00:00",
      "updated_at": "2026-01-30T09:00:00"
    }
  ],
  "count": 1
}
```

### 2.5 添加食材

添加新的食材到库存。

**接口**: `POST /api/ingredients`

**请求体**:
```json
{
  "name": "鸡蛋",
  "quantity": "6个",
  "state": "新鲜",
  "category": "主食",
  "storage_location": "fridge"
}
```

**参数说明**:
- `name` (必填): 食材名称
- `quantity` (可选): 数量
- `state` (可选): 状态（新鲜/冷冻/常温）
- `category` (可选): 分类（蔬菜/肉禽/海鲜/主食/调料）
- `storage_location` (可选): 存储位置（fridge/freezer/pantry）

**响应示例**:
```json
{
  "success": true,
  "ingredient": {
    "id": 1,
    "name": "鸡蛋",
    "quantity": "6个",
    "state": "新鲜",
    "category": "主食",
    "storage_location": "fridge",
    "is_common": false,
    "created_at": "2026-01-30T09:00:00",
    "updated_at": "2026-01-30T09:00:00"
  }
}
```

### 2.6 更新食材

更新指定食材的信息。

**接口**: `PUT /api/ingredients/<id>`

**路径参数**:
- `id`: 食材 ID

**请求体**:
```json
{
  "quantity": "8个",
  "state": "新鲜"
}
```

**响应示例**:
```json
{
  "success": true,
  "ingredient": {
    "id": 1,
    "name": "鸡蛋",
    "quantity": "8个",
    "state": "新鲜",
    "category": "主食",
    "storage_location": "fridge",
    "is_common": false,
    "created_at": "2026-01-30T09:00:00",
    "updated_at": "2026-01-30T10:00:00"
  }
}
```

### 2.7 删除食材

从库存中删除指定食材。

**接口**: `DELETE /api/ingredients/<id>`

**路径参数**:
- `id`: 食材 ID

**响应示例**:
```json
{
  "success": true,
  "message": "食材已删除"
}
```

### 2.8 标记为常用食材

将指定食材标记为常用。

**接口**: `POST /api/ingredients/<id>/mark-common`

**路径参数**:
- `id`: 食材 ID

**响应示例**:
```json
{
  "success": true,
  "ingredient": {
    "id": 1,
    "name": "鸡蛋",
    "quantity": "6个",
    "state": "新鲜",
    "category": "主食",
    "storage_location": "fridge",
    "is_common": true,
    "created_at": "2026-01-30T09:00:00",
    "updated_at": "2026-01-30T10:00:00"
  }
}
```

---

## 3. 收藏夹管理 API

### 3.1 获取所有收藏

获取用户所有收藏的食谱。

**接口**: `GET /api/favorites`

**响应示例**:
```json
{
  "success": true,
  "favorites": [
    {
      "id": 1,
      "recipe_id": 1,
      "group_id": 1,
      "notes": "很好吃",
      "created_at": "2026-01-30T10:00:00",
      "recipe": {
        "id": 1,
        "name": "番茄炒蛋",
        "description": "经典家常菜"
      }
    }
  ],
  "count": 1
}
```

### 3.2 获取所有分组

获取所有收藏分组。

**接口**: `GET /api/favorites/groups`

**响应示例**:
```json
{
  "success": true,
  "groups": [
    {
      "id": 1,
      "name": "减脂餐",
      "description": "健康低卡",
      "created_at": "2026-01-30T09:00:00"
    }
  ],
  "count": 1
}
```

### 3.3 创建分组

创建新的收藏分组。

**接口**: `POST /api/favorites/groups`

**请求体**:
```json
{
  "name": "减脂餐",
  "description": "健康低卡"
}
```

**参数说明**:
- `name` (必填): 分组名称
- `description` (可选): 分组描述

**响应示例**:
```json
{
  "success": true,
  "group": {
    "id": 1,
    "name": "减脂餐",
    "description": "健康低卡",
    "created_at": "2026-01-30T09:00:00"
  }
}
```

### 3.4 更新分组

更新指定分组的信息。

**接口**: `PUT /api/favorites/groups/<id>`

**路径参数**:
- `id`: 分组 ID

**请求体**:
```json
{
  "name": "新名称",
  "description": "新描述"
}
```

**响应示例**:
```json
{
  "success": true,
  "group": {
    "id": 1,
    "name": "新名称",
    "description": "新描述",
    "created_at": "2026-01-30T09:00:00"
  }
}
```

### 3.5 删除分组

删除指定的收藏分组。

**接口**: `DELETE /api/favorites/groups/<id>`

**路径参数**:
- `id`: 分组 ID

**响应示例**:
```json
{
  "success": true,
  "message": "分组已删除"
}
```

### 3.6 按分组获取收藏

获取指定分组下的所有收藏。

**接口**: `GET /api/favorites/by-group/<id>`

**路径参数**:
- `id`: 分组 ID

**响应示例**:
```json
{
  "success": true,
  "favorites": [
    {
      "id": 1,
      "recipe_id": 1,
      "group_id": 1,
      "notes": "很好吃",
      "created_at": "2026-01-30T10:00:00",
      "recipe": {
        "id": 1,
        "name": "番茄炒蛋",
        "description": "经典家常菜"
      }
    }
  ],
  "count": 1
}
```

### 3.7 添加收藏

将食谱添加到收藏夹。

**接口**: `POST /api/favorites`

**请求体**:
```json
{
  "recipe_id": 1,
  "group_id": 1,
  "notes": "很好吃"
}
```

**参数说明**:
- `recipe_id` (必填): 食谱 ID
- `group_id` (可选): 分组 ID
- `notes` (可选): 备注

**响应示例**:
```json
{
  "success": true,
  "favorite": {
    "id": 1,
    "recipe_id": 1,
    "group_id": 1,
    "notes": "很好吃",
    "created_at": "2026-01-30T10:00:00"
  }
}
```

### 3.8 移除收藏

从收藏夹中移除指定食谱。

**接口**: `DELETE /api/favorites/<id>`

**路径参数**:
- `id`: 收藏 ID

**响应示例**:
```json
{
  "success": true,
  "message": "已取消收藏"
}
```

---

## 4. 购物清单 API

### 4.1 获取购物清单

获取所有购物清单项目。

**接口**: `GET /api/shopping-list`

**响应示例**:
```json
{
  "success": true,
  "items": [
    {
      "id": 1,
      "ingredient_name": "鸡蛋",
      "quantity": "6个",
      "category": "主食",
      "is_purchased": false,
      "recipe_id": 1,
      "created_at": "2026-01-30T10:00:00"
    }
  ],
  "count": 1
}
```

### 4.2 添加购物项

手动添加购物项到清单。

**接口**: `POST /api/shopping-list`

**请求体**:
```json
{
  "ingredient_name": "鸡蛋",
  "quantity": "6个",
  "category": "主食"
}
```

**参数说明**:
- `ingredient_name` (必填): 食材名称
- `quantity` (可选): 数量
- `category` (可选): 分类

**响应示例**:
```json
{
  "success": true,
  "item": {
    "id": 1,
    "ingredient_name": "鸡蛋",
    "quantity": "6个",
    "category": "主食",
    "is_purchased": false,
    "recipe_id": null,
    "created_at": "2026-01-30T10:00:00"
  }
}
```

### 4.3 更新购物项

更新指定购物项的信息。

**接口**: `PUT /api/shopping-list/<id>`

**路径参数**:
- `id`: 购物项 ID

**请求体**:
```json
{
  "quantity": "8个",
  "is_purchased": true
}
```

**响应示例**:
```json
{
  "success": true,
  "item": {
    "id": 1,
    "ingredient_name": "鸡蛋",
    "quantity": "8个",
    "category": "主食",
    "is_purchased": true,
    "recipe_id": null,
    "created_at": "2026-01-30T10:00:00"
  }
}
```

### 4.4 删除购物项

从购物清单中删除指定项目。

**接口**: `DELETE /api/shopping-list/<id>`

**路径参数**:
- `id`: 购物项 ID

**响应示例**:
```json
{
  "success": true,
  "message": "购物项已删除"
}
```

### 4.5 标记为已购买

将指定购物项标记为已购买。

**接口**: `POST /api/shopping-list/<id>/purchase`

**路径参数**:
- `id`: 购物项 ID

**响应示例**:
```json
{
  "success": true,
  "item": {
    "id": 1,
    "ingredient_name": "鸡蛋",
    "quantity": "6个",
    "category": "主食",
    "is_purchased": true,
    "recipe_id": null,
    "created_at": "2026-01-30T10:00:00"
  }
}
```

### 4.6 从菜谱生成购物清单

根据食谱中标记为"需补充"的食材自动生成购物清单。

**接口**: `POST /api/shopping-list/generate`

**请求体**:
```json
{
  "recipe_id": 1
}
```

**参数说明**:
- `recipe_id` (必填): 食谱 ID

**响应示例**:
```json
{
  "success": true,
  "items": [
    {
      "id": 2,
      "ingredient_name": "盐",
      "quantity": "适量",
      "category": "调料",
      "is_purchased": false,
      "recipe_id": 1,
      "created_at": "2026-01-30T10:00:00"
    }
  ],
  "count": 1
}
```

### 4.7 清除已购买项目

批量删除所有已购买的购物项。

**接口**: `DELETE /api/shopping-list/purchased`

**响应示例**:
```json
{
  "success": true,
  "message": "已购买项目已清除"
}
```

---

## 数据模型

### Recipe (食谱)

```typescript
{
  id: number;
  name: string;
  description: string;
  difficulty: string;  // "新手" | "进阶"
  cooking_time: string;
  calories: string;
  cuisine: string;  // "中式" | "西式" | "日韩" | "东南亚"
  taste: string;  // "酸" | "甜" | "苦" | "辣" | "咸" | "清淡"
  scenario: string;  // "早餐" | "快手菜" | "硬菜"
  skill_level: string;  // "新手" | "进阶"
  ingredients: Array<{
    name: string;
    quantity: string;
    status: string;  // "[已有]" | "[需补充]"
  }>;
  steps: string[];
  tags: string[];
  created_at: string;  // ISO 8601 格式
  step_progress?: Array<{
    step_index: number;
    is_completed: boolean;
    completed_at: string | null;
  }>;
}
```

### Ingredient (食材)

```typescript
{
  id: number;
  name: string;
  quantity: string;
  state: string;  // "新鲜" | "冷冻" | "常温"
  category: string;  // "蔬菜" | "肉禽" | "海鲜" | "主食" | "调料"
  storage_location: string;  // "fridge" | "freezer" | "pantry"
  is_common: boolean;
  created_at: string;  // ISO 8601 格式
  updated_at: string;  // ISO 8601 格式
}
```

### Favorite (收藏)

```typescript
{
  id: number;
  recipe_id: number;
  group_id: number | null;
  notes: string;
  created_at: string;  // ISO 8601 格式
  recipe?: Recipe;  // 关联的食谱信息
}
```

### FavoriteGroup (收藏分组)

```typescript
{
  id: number;
  name: string;
  description: string;
  created_at: string;  // ISO 8601 格式
}
```

### ShoppingListItem (购物清单项)

```typescript
{
  id: number;
  ingredient_name: string;
  quantity: string;
  category: string;
  is_purchased: boolean;
  recipe_id: number | null;
  created_at: string;  // ISO 8601 格式
}
```

### RecipeStepProgress (步骤进度)

```typescript
{
  id: number;
  recipe_id: number;
  step_index: number;
  is_completed: boolean;
  completed_at: string | null;  // ISO 8601 格式
}
```

---

## 错误处理

### 常见错误码

| 状态码 | 说明 | 示例 |
|--------|------|------|
| 400 | 请求参数错误 | `{"error": "请提供至少一种食材"}` |
| 404 | 资源不存在 | `{"error": "食谱不存在"}` |
| 500 | 服务器内部错误 | `{"error": "数据库连接失败"}` |

### 错误响应格式

所有错误响应都遵循以下格式：

```json
{
  "error": "具体的错误信息描述"
}
```

### 调试建议

1. **检查请求格式**: 确保 Content-Type 为 `application/json`
2. **验证必填参数**: 确保所有必填字段都已提供
3. **查看后端日志**: 运行 `python run.py` 时查看控制台输出
4. **使用健康检查**: 访问 `/health` 确认服务正常运行
5. **CORS 问题**: 确保前端请求来自配置的允许源（默认 `http://localhost:5174`）

---

## 开发环境配置

### 后端启动

```bash
cd backend
python run.py
```

服务将运行在 `http://localhost:5000`

### 前端配置

在 `frontend/.env` 中配置：

```
VITE_API_BASE_URL=http://localhost:5000/api
```

### 数据库初始化

```bash
cd backend
python init_db.py
```

### API 测试

```bash
cd backend
python test_api.py
```

---

## 更新日志

### v1.0.0 (2026-01-30)

- 初始版本
- 实现食谱生成、食材管理、收藏夹、购物清单功能
- 支持 AI 食谱生成
- 支持步骤进度跟踪
- 完整的 CRUD 操作

---

**文档版本**: 1.0.0
**最后更新**: 2026-01-30
**维护者**: SmartCook AI Team
