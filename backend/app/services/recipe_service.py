"""
AI Recipe Generation Service
使用 LangChain + Dashscope (Qwen) 生成食谱
"""
import os
import logging
import time
from typing import List, Dict, Any, Optional
from langchain_community.chat_models import ChatTongyi
from langchain.schema import HumanMessage, SystemMessage
from config import Config
from app.database import db
from app.models.recipe import Recipe

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RecipeGenerationService:
    """食谱生成服务"""

    def __init__(self):
        """初始化 LangChain 和 Dashscope 模型"""
        try:
            self.model = ChatTongyi(
                model_name=Config.MODEL_NAME,
                dashscope_api_key=Config.DASHSCOPE_API_KEY,
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS
            )
            logger.info(f"✅ AI 模型初始化成功: {Config.MODEL_NAME}")
        except Exception as e:
            logger.error(f"❌ AI 模型初始化失败: {e}")
            raise

    def generate_recipes(
        self,
        ingredients: List[Dict[str, Any]],
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        根据食材和筛选条件生成食谱

        Args:
            ingredients: 食材列表 [{"name": "鸡蛋", "quantity": "6个", "state": "新鲜"}]
            filters: 筛选条件 {"cuisine": "中式", "taste": "清淡", "scenario": "快手菜", "skill": "新手"}

        Returns:
            食谱列表
        """
        start_time = time.time()
        logger.info(f"🔄 开始生成食谱 - 食材数: {len(ingredients)}, 筛选条件: {filters}")

        # 构建 Prompt
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(ingredients, filters)

        # 调用 LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        try:
            # 记录请求
            logger.debug(f"📤 AI 请求 - 食材: {[ing['name'] for ing in ingredients]}")

            response = self.model.invoke(messages)
            elapsed = time.time() - start_time

            logger.info(f"✅ AI 响应成功 - 耗时: {elapsed:.2f}秒")
            logger.debug(f"📥 AI 响应内容长度: {len(response.content)} 字符")

            recipes = self._parse_response(response.content)

            if not recipes:
                logger.warning("⚠️  AI 响应解析失败，使用备用食谱")
                return self._get_fallback_recipes(ingredients)

            # 保存到数据库
            saved_recipes = []
            for i, recipe_data in enumerate(recipes, 1):
                saved_recipe = self.save_recipe_to_history(recipe_data)
                if saved_recipe:
                    saved_recipes.append(saved_recipe.to_dict())
                    logger.info(f"💾 食谱 {i} 已保存: {recipe_data.get('name', 'N/A')}")
                else:
                    logger.warning(f"⚠️  食谱 {i} 保存失败")

            total_time = time.time() - start_time
            logger.info(f"✅ 食谱生成完成 - 总耗时: {total_time:.2f}秒, 生成数量: {len(saved_recipes)}")

            return saved_recipes if saved_recipes else recipes

        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"❌ AI 生成失败 - 耗时: {elapsed:.2f}秒, 错误: {str(e)}", exc_info=True)
            return self._get_fallback_recipes(ingredients)

    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        return """你是一位专业的美食顾问和创意厨师，擅长根据现有食材创造美味且可执行的食谱。

你的任务：
1. 根据用户提供的食材，生成 3 个创意食谱
2. 每个食谱必须包含：创意菜名、所需食材（标注[已有]和[需补充]）、难度等级、烹饪时间、大致热量、详细步骤
3. 食谱必须合理可行，避免奇怪的食材组合（除非用户明确要求）
4. 优先使用用户已有的食材，尽量减少需要补充的食材
5. 菜名要有创意和吸引力，例如"黄金满屋蛋炒饭"而不是"蛋炒饭"

输出格式（JSON）：
```json
[
  {
    "name": "创意菜名",
    "description": "简短描述",
    "difficulty": "新手/进阶",
    "time": "15分钟",
    "calories": "约450卡",
    "ingredients": [
      {"name": "鸡蛋", "quantity": "2个", "status": "已有"},
      {"name": "酱油", "quantity": "1勺", "status": "需补充"}
    ],
    "steps": [
      "步骤1：...",
      "步骤2：..."
    ],
    "tags": ["快手菜", "营养丰富"]
  }
]
```

重要约束：
- 不要生成"西瓜炒月饼"等不合理组合
- 考虑食材的新鲜度和状态（冷冻、新鲜等）
- 步骤要清晰具体，适合烹饪新手"""

    def _build_user_prompt(
        self,
        ingredients: List[Dict[str, Any]],
        filters: Dict[str, Any] = None
    ) -> str:
        """构建用户提示词"""
        # 食材列表
        ingredients_text = "\n".join([
            f"- {ing['name']} ({ing.get('quantity', '适量')}) - {ing.get('state', '常温')}"
            for ing in ingredients
        ])

        prompt = f"""我的冰箱里有以下食材：
{ingredients_text}

"""

        # 添加筛选条件
        if filters:
            filter_text = []
            if filters.get('cuisine'):
                filter_text.append(f"菜系：{filters['cuisine']}")
            if filters.get('taste'):
                filter_text.append(f"口味：{filters['taste']}")
            if filters.get('scenario'):
                filter_text.append(f"场景：{filters['scenario']}")
            if filters.get('skill'):
                filter_text.append(f"技能水平：{filters['skill']}")

            if filter_text:
                prompt += "我的偏好：\n" + "\n".join(filter_text) + "\n\n"

        prompt += "请根据这些食材，为我生成 3 个创意食谱。请严格按照 JSON 格式输出。"

        return prompt

    def _parse_response(self, response_text: str) -> List[Dict[str, Any]]:
        """解析 LLM 响应"""
        import json
        import re

        logger.debug("🔍 开始解析 AI 响应")

        # 提取 JSON 部分 - 支持多种格式
        json_patterns = [
            r'```json\s*(.*?)\s*```',  # 标准 markdown json 代码块
            r'```\s*(.*?)\s*```',       # 普通代码块
            r'\[\s*\{.*?\}\s*\]',       # 直接的 JSON 数组
        ]

        json_text = None
        for pattern in json_patterns:
            match = re.search(pattern, response_text, re.DOTALL)
            if match:
                json_text = match.group(1) if '```' in pattern else match.group(0)
                logger.debug(f"✅ 使用模式匹配到 JSON: {pattern}")
                break

        if not json_text:
            # 尝试直接解析整个响应
            json_text = response_text
            logger.debug("⚠️  未找到代码块，尝试直接解析")

        try:
            recipes = json.loads(json_text)
            recipe_list = recipes if isinstance(recipes, list) else [recipes]
            logger.info(f"✅ JSON 解析成功 - 食谱数量: {len(recipe_list)}")
            return recipe_list
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON 解析失败: {e}")
            logger.debug(f"原始响应 (前500字符): {response_text[:500]}")
            return []

    def _get_fallback_recipes(self, ingredients: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """备用食谱（当 AI 生成失败时）"""
        return [
            {
                "name": "经典家常炒饭",
                "description": "简单快手的美味炒饭",
                "difficulty": "新手",
                "time": "15分钟",
                "calories": "约500卡",
                "ingredients": [
                    {"name": "米饭", "quantity": "1碗", "status": "已有"},
                    {"name": "鸡蛋", "quantity": "2个", "status": "已有"},
                    {"name": "酱油", "quantity": "1勺", "status": "需补充"}
                ],
                "steps": [
                    "将鸡蛋打散，加少许盐",
                    "热锅下油，炒散鸡蛋后盛出",
                    "下米饭翻炒，加入鸡蛋和酱油",
                    "翻炒均匀即可出锅"
                ],
                "tags": ["快手菜", "经典美味"]
            }
        ]

    def save_recipe_to_history(self, recipe_data: Dict[str, Any]) -> Optional[Recipe]:
        """保存食谱到历史记录"""
        try:
            # 标准化字段名
            normalized_data = {
                'name': recipe_data.get('name', ''),
                'description': recipe_data.get('description', ''),
                'difficulty': recipe_data.get('difficulty', ''),
                'cooking_time': recipe_data.get('time', recipe_data.get('cooking_time', '')),
                'calories': recipe_data.get('calories', ''),
                'cuisine': recipe_data.get('cuisine', ''),
                'taste': recipe_data.get('taste', ''),
                'scenario': recipe_data.get('scenario', ''),
                'skill_level': recipe_data.get('skill_level', recipe_data.get('difficulty', '')),
                'ingredients': recipe_data.get('ingredients', []),
                'steps': recipe_data.get('steps', []),
                'tags': recipe_data.get('tags', [])
            }

            recipe = Recipe.from_ai_response(normalized_data)
            db.session.add(recipe)
            db.session.commit()
            logger.debug(f"✅ 食谱已保存到数据库: ID={recipe.id}, Name={recipe.name}")
            return recipe
        except Exception as e:
            logger.error(f"❌ 保存食谱失败: {e}", exc_info=True)
            db.session.rollback()
            return None

    def get_recipe_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取历史记录（最近N条）"""
        try:
            recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(limit).all()
            logger.debug(f"📖 查询历史记录: {len(recipes)} 条")
            return [recipe.to_dict() for recipe in recipes]
        except Exception as e:
            logger.error(f"❌ 获取历史记录失败: {e}", exc_info=True)
            return []

    def get_recipe_by_id(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取单个食谱"""
        try:
            recipe = Recipe.query.get(recipe_id)
            if recipe:
                logger.debug(f"📖 查询食谱: ID={recipe_id}, Name={recipe.name}")
            else:
                logger.warning(f"⚠️  食谱不存在: ID={recipe_id}")
            return recipe.to_dict(include_progress=True) if recipe else None
        except Exception as e:
            logger.error(f"❌ 获取食谱失败: {e}", exc_info=True)
            return None

    def delete_recipe(self, recipe_id: int) -> bool:
        """删除食谱"""
        try:
            recipe = Recipe.query.get(recipe_id)
            if recipe:
                db.session.delete(recipe)
                db.session.commit()
                logger.info(f"🗑️  食谱已删除: ID={recipe_id}, Name={recipe.name}")
                return True
            logger.warning(f"⚠️  食谱不存在: ID={recipe_id}")
            return False
        except Exception as e:
            logger.error(f"❌ 删除食谱失败: {e}", exc_info=True)
            db.session.rollback()
            return False


# 创建全局服务实例
recipe_service = RecipeGenerationService()
