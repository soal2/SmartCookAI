"""
AI Recipe Generation Service
使用 LangChain + Dashscope (Qwen) 生成食谱
"""
import os
import json
import logging
import re
import time
from typing import List, Dict, Any, Optional
from langchain_community.chat_models import ChatTongyi
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import LLMChain, SequentialChain, TransformChain
from langchain.prompts import PromptTemplate
from config import Config
from app.database import db
from app.models.recipe import Recipe
from app.services.substitution_service import substitution_service

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
        try:
            self.chain_service = RecipeChainService(self)
            logger.info("✅ 链式服务初始化成功")
        except Exception as e:
            logger.error(f"❌ 链式服务初始化失败: {e}")
            raise

    def process_chain(self, user_input: str) -> Dict[str, Any]:
        """执行链式流程"""
        return self.chain_service.process_chain(user_input)

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


class RecipeChainService:
    """链式食谱服务"""

    def __init__(self, recipe_service: 'RecipeGenerationService'):
        """初始化链与模型"""
        self.recipe_service = recipe_service
        self.model = recipe_service.model
        self.analysis_chain = self._build_analysis_chain()
        self.substitution_chain = self._build_substitution_chain()
        self.chain = self._build_full_chain()

    def _build_analysis_chain(self) -> LLMChain:
        """构建食材分析链"""
        allowed_cuisines = '、'.join(Config.ALLOWED_CUISINES)
        allowed_tastes = '、'.join(Config.ALLOWED_TASTES)
        allowed_scenarios = '、'.join(Config.ALLOWED_SCENARIOS)
        allowed_skills = '、'.join(Config.ALLOWED_SKILLS)
        allowed_states = '、'.join(Config.ALLOWED_STATES)

        prompt = PromptTemplate(
            input_variables=['user_input'],
            template=(
                "你是专业的食材分析与烹饪意图识别助手。请从用户的模糊输入中提取信息。\n"
                "可选菜系: {allowed_cuisines}\n"
                "可选口味: {allowed_tastes}\n"
                "可选场景: {allowed_scenarios}\n"
                "可选技能: {allowed_skills}\n"
                "可选食材状态: {allowed_states}\n\n"
                "输出严格 JSON：\n"
                "{{\n"
                "  \"intent\": \"食谱生成/替代方案/食材分析/其他\",\n"
                "  \"ingredients\": [\n"
                "    {{\"name\": \"食材名\", \"quantity\": \"数量(可空)\", \"state\": \"状态(可空)\"}}\n"
                "  ],\n"
                "  \"filters\": {{\n"
                "    \"cuisine\": \"菜系(可空)\",\n"
                "    \"taste\": \"口味(可空)\",\n"
                "    \"scenario\": \"场景(可空)\",\n"
                "    \"skill\": \"技能(可空)\"\n"
                "  }},\n"
                "  \"constraints\": [\"忌口/过敏/限制(可空)\"]\n"
                "}}\n\n"
                "用户输入：{user_input}\n"
                "只输出 JSON。"
            ),
            partial_variables={
                'allowed_cuisines': allowed_cuisines,
                'allowed_tastes': allowed_tastes,
                'allowed_scenarios': allowed_scenarios,
                'allowed_skills': allowed_skills,
                'allowed_states': allowed_states
            }
        )
        return LLMChain(llm=self.model, prompt=prompt, output_key='analysis_text')

    def _build_substitution_chain(self) -> LLMChain:
        """构建替代方案推荐链"""
        prompt = PromptTemplate(
            input_variables=['user_input', 'missing_ingredients', 'substitution_candidates'],
            template=(
                "你是专业的食材替代方案顾问。请结合数据库检索结果，生成完整替代方案。\n"
                "要求：优先使用数据库候选项；若不足，可补充常见替代。\n"
                "输出严格 JSON：\n"
                "{{\n"
                "  \"summary\": \"整体说明\",\n"
                "  \"items\": [\n"
                "    {{\n"
                "      \"ingredient\": \"缺失食材\",\n"
                "      \"reason\": \"替代原因\",\n"
                "      \"recommendations\": [\n"
                "        {{\"name\": \"替代品\", \"ratio\": \"比例\", \"note\": \"说明\", \"source\": \"数据库/补充建议\"}}\n"
                "      ]\n"
                "    }}\n"
                "  ]\n"
                "}}\n\n"
                "用户输入：{user_input}\n"
                "缺失食材：{missing_ingredients}\n"
                "数据库候选：{substitution_candidates}\n"
                "只输出 JSON。"
            )
        )
        return LLMChain(llm=self.model, prompt=prompt, output_key='substitution_text')

    def _build_full_chain(self) -> SequentialChain:
        """构建完整业务链"""
        parse_analysis_chain = TransformChain(
            input_variables=['analysis_text', 'user_input'],
            output_variables=['analysis'],
            transform=self._parse_analysis_transform
        )
        recipe_chain = TransformChain(
            input_variables=['analysis'],
            output_variables=['recipes'],
            transform=self._generate_recipes_transform
        )
        candidates_chain = TransformChain(
            input_variables=['recipes', 'analysis'],
            output_variables=['missing_ingredients', 'substitution_candidates'],
            transform=self._collect_substitution_candidates
        )
        parse_substitution_chain = TransformChain(
            input_variables=['substitution_text', 'missing_ingredients', 'substitution_candidates'],
            output_variables=['substitutions'],
            transform=self._parse_substitution_transform
        )

        return SequentialChain(
            chains=[
                self.analysis_chain,
                parse_analysis_chain,
                recipe_chain,
                candidates_chain,
                self.substitution_chain,
                parse_substitution_chain
            ],
            input_variables=['user_input'],
            output_variables=['analysis', 'recipes', 'substitutions', 'missing_ingredients', 'substitution_candidates'],
            verbose=False
        )

    def process_chain(self, user_input: str) -> Dict[str, Any]:
        """执行链式流程"""
        start_time = time.time()
        logger.info(f"🔄 开始链式处理: {user_input}")

        result = self.chain.invoke({'user_input': user_input})

        elapsed = time.time() - start_time
        logger.info(f"✅ 链式处理完成 - 耗时: {elapsed:.2f}秒")
        return result

    def _parse_json_from_text(self, text: str) -> Optional[Any]:
        """从文本中解析 JSON"""
        json_patterns = [
            r'```json\s*(\{.*?\}|\[.*?\])\s*```',
            r'```\s*(\{.*?\}|\[.*?\])\s*```',
            r'(\{.*\})',
            r'(\[.*\])'
        ]

        for pattern in json_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                candidate = match.group(1)
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError:
                    continue

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("⚠️  JSON 解析失败")
            return None

    def _parse_analysis_transform(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """解析食材分析结果"""
        analysis_text = inputs.get('analysis_text', '')
        user_input = inputs.get('user_input', '')
        parsed = self._parse_json_from_text(analysis_text)

        if not isinstance(parsed, dict):
            logger.warning("⚠️  分析结果格式异常，使用启发式解析")
            parsed = self._heuristic_analysis(user_input)

        ingredients = self._normalize_ingredients(parsed.get('ingredients', []))
        filters = self._normalize_filters(parsed.get('filters', {}))
        constraints = parsed.get('constraints', []) if isinstance(parsed.get('constraints', []), list) else []
        intent = parsed.get('intent', '').strip() if isinstance(parsed.get('intent'), str) else ''
        if not intent:
            intent = self._infer_intent(user_input)

        analysis = {
            'intent': intent,
            'ingredients': ingredients,
            'filters': filters,
            'constraints': constraints
        }

        logger.info(f"✅ 食材分析完成 - 食材数: {len(ingredients)}")
        return {'analysis': analysis}

    def _generate_recipes_transform(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """生成食谱"""
        analysis = inputs.get('analysis', {})
        ingredients = analysis.get('ingredients', [])
        filters = analysis.get('filters', {})

        if not ingredients:
            logger.warning("⚠️  未识别到食材，跳过食谱生成")
            return {'recipes': []}

        recipes = self.recipe_service.generate_recipes(ingredients, filters or None)
        logger.info(f"✅ 食谱生成完成 - 数量: {len(recipes)}")
        return {'recipes': recipes}

    def _collect_substitution_candidates(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """收集替代方案候选"""
        recipes = inputs.get('recipes', []) or []
        analysis = inputs.get('analysis', {}) or {}
        intent = str(analysis.get('intent', '')).strip()
        analysis_ingredients = analysis.get('ingredients', []) if isinstance(analysis, dict) else []

        if intent == '替代方案' and analysis_ingredients:
            missing_ingredients = sorted({
                ing.get('name', '').strip()
                for ing in analysis_ingredients
                if isinstance(ing, dict) and ing.get('name')
            })
        else:
            missing_ingredients = self._extract_missing_ingredients(recipes)

        substitution_candidates: Dict[str, List[Dict[str, Any]]] = {}

        for ingredient_name in missing_ingredients:
            substitutes = substitution_service.get_substitutes(ingredient_name, limit=5)
            if substitutes:
                substitution_candidates[ingredient_name] = substitutes

        logger.info(f"✅ 替代候选检索完成 - 缺失食材: {len(missing_ingredients)}")
        return {
            'missing_ingredients': missing_ingredients,
            'substitution_candidates': substitution_candidates
        }

    def _parse_substitution_transform(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """解析替代方案结果"""
        missing_ingredients = inputs.get('missing_ingredients', [])
        substitution_candidates = inputs.get('substitution_candidates', {})
        substitution_text = inputs.get('substitution_text', '')

        if not missing_ingredients:
            return {
                'substitutions': {
                    'summary': '当前食谱未包含需补充食材，无需替代方案。',
                    'items': []
                }
            }

        parsed = self._parse_json_from_text(substitution_text)
        if not isinstance(parsed, dict):
            logger.warning("⚠️  替代方案解析失败，使用候选结果兜底")
            parsed = self._fallback_substitutions(missing_ingredients, substitution_candidates)

        if 'items' not in parsed:
            parsed['items'] = []
        if 'summary' not in parsed:
            parsed['summary'] = '已为缺失食材生成替代建议。'

        return {'substitutions': parsed}

    def _normalize_ingredients(self, ingredients: Any) -> List[Dict[str, Any]]:
        """标准化食材列表"""
        normalized = []
        if not isinstance(ingredients, list):
            return normalized

        for ingredient in ingredients:
            if isinstance(ingredient, str):
                name = ingredient.strip()
                item = {'name': name}
            elif isinstance(ingredient, dict):
                name = str(ingredient.get('name', '')).strip()
                item = ingredient
            else:
                continue

            if not name:
                continue

            quantity = str(item.get('quantity', '适量')).strip() or '适量'
            state = str(item.get('state', '常温')).strip() or '常温'
            if state not in Config.ALLOWED_STATES:
                state = '常温'

            normalized.append({
                'name': name,
                'quantity': quantity,
                'state': state
            })

        return normalized

    def _normalize_filters(self, filters: Any) -> Dict[str, Any]:
        """标准化筛选条件"""
        if not isinstance(filters, dict):
            return {}

        normalized = {}
        cuisine = str(filters.get('cuisine', '')).strip()
        taste = str(filters.get('taste', '')).strip()
        scenario = str(filters.get('scenario', '')).strip()
        skill = str(filters.get('skill', '')).strip()

        if cuisine in Config.ALLOWED_CUISINES:
            normalized['cuisine'] = cuisine
        if taste in Config.ALLOWED_TASTES:
            normalized['taste'] = taste
        if scenario in Config.ALLOWED_SCENARIOS:
            normalized['scenario'] = scenario
        if skill in Config.ALLOWED_SKILLS:
            normalized['skill'] = skill

        return normalized

    def _infer_intent(self, user_input: str) -> str:
        """启发式意图识别"""
        if any(keyword in user_input for keyword in ['替代', '没有', '缺少']):
            return '替代方案'
        if any(keyword in user_input for keyword in ['做', '菜', '食谱', '做饭']):
            return '食谱生成'
        return '食材分析'

    def _heuristic_analysis(self, user_input: str) -> Dict[str, Any]:
        """启发式解析"""
        filters = {}
        for cuisine in Config.ALLOWED_CUISINES:
            if cuisine in user_input:
                filters['cuisine'] = cuisine
                break

        for taste in Config.ALLOWED_TASTES:
            if taste in user_input:
                filters['taste'] = taste
                break

        for scenario in Config.ALLOWED_SCENARIOS:
            if scenario in user_input:
                filters['scenario'] = scenario
                break

        for skill in Config.ALLOWED_SKILLS:
            if skill in user_input:
                filters['skill'] = skill
                break

        intent = self._infer_intent(user_input)
        return {
            'intent': intent,
            'ingredients': [],
            'filters': filters,
            'constraints': []
        }

    def _extract_missing_ingredients(self, recipes: List[Dict[str, Any]]) -> List[str]:
        """提取需补充食材"""
        missing_set = set()
        for recipe in recipes:
            for ingredient in recipe.get('ingredients', []):
                status = str(ingredient.get('status', '')).strip()
                if '需补充' in status:
                    name = str(ingredient.get('name', '')).strip()
                    if name:
                        missing_set.add(name)
        return sorted(list(missing_set))

    def _fallback_substitutions(
        self,
        missing_ingredients: List[str],
        substitution_candidates: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """替代方案兜底"""
        items = []
        for ingredient in missing_ingredients:
            candidates = substitution_candidates.get(ingredient, [])
            recommendations = []
            for candidate in candidates:
                recommendations.append({
                    'name': candidate.get('substitute_ingredient', ''),
                    'ratio': candidate.get('substitution_ratio', '1:1'),
                    'note': candidate.get('notes', ''),
                    'source': '数据库'
                })

            items.append({
                'ingredient': ingredient,
                'reason': '根据库存与口味偏好推荐替代。',
                'recommendations': recommendations
            })

        return {
            'summary': '基于数据库替代关系生成建议。',
            'items': items
        }


# 创建全局服务实例
recipe_service = RecipeGenerationService()
