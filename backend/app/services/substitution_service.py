"""
Ingredient Substitution Service
食材替代推荐服务
"""
import logging
from typing import List, Dict, Any, Optional
from app.database import db
from app.models.substitution import IngredientSubstitution

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SubstitutionService:
    """食材替代服务"""

    @staticmethod
    def get_substitutes(ingredient_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        获取某食材的替代建议

        Args:
            ingredient_name: 食材名称
            limit: 返回结果数量限制

        Returns:
            替代建议列表
        """
        try:
            # 模糊匹配食材名称
            substitutions = IngredientSubstitution.query.filter(
                IngredientSubstitution.original_ingredient.like(f'%{ingredient_name}%')
            ).order_by(
                IngredientSubstitution.similarity_score.desc()
            ).limit(limit).all()

            logger.info(f"✅ 查询食材 '{ingredient_name}' 的替代建议成功，找到 {len(substitutions)} 个")
            return [sub.to_dict() for sub in substitutions]
        except Exception as e:
            logger.error(f"❌ 查询食材替代建议失败: {e}")
            return []

    @staticmethod
    def get_recipe_substitutions(ingredients: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        获取菜谱中所有缺失食材的替代建议

        Args:
            ingredients: 食材列表，包含 name 和 status 字段

        Returns:
            字典，key 为食材名称，value 为替代建议列表
        """
        try:
            result = {}
            missing_ingredients = [
                ing for ing in ingredients
                if ing.get('status') == '需补充'
            ]

            for ingredient in missing_ingredients:
                name = ingredient.get('name', '')
                substitutes = SubstitutionService.get_substitutes(name)
                if substitutes:
                    result[name] = substitutes

            logger.info(f"✅ 获取菜谱替代建议成功，共 {len(result)} 个缺失食材有替代方案")
            return result
        except Exception as e:
            logger.error(f"❌ 获取菜谱替代建议失败: {e}")
            return {}

    @staticmethod
    def add_substitution(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        添加食材替代关系

        Args:
            data: 替代关系数据

        Returns:
            创建的替代关系字典
        """
        try:
            substitution = IngredientSubstitution(
                original_ingredient=data.get('original_ingredient'),
                substitute_ingredient=data.get('substitute_ingredient'),
                similarity_score=data.get('similarity_score', 0.8),
                substitution_ratio=data.get('substitution_ratio', '1:1'),
                notes=data.get('notes'),
                category=data.get('category')
            )
            db.session.add(substitution)
            db.session.commit()
            logger.info(f"✅ 添加替代关系成功: {substitution.original_ingredient} -> {substitution.substitute_ingredient}")
            return substitution.to_dict()
        except Exception as e:
            logger.error(f"❌ 添加替代关系失败: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def get_all_substitutions() -> List[Dict[str, Any]]:
        """获取所有替代关系"""
        try:
            substitutions = IngredientSubstitution.query.order_by(
                IngredientSubstitution.original_ingredient
            ).all()
            logger.info(f"✅ 获取所有替代关系成功，共 {len(substitutions)} 条")
            return [sub.to_dict() for sub in substitutions]
        except Exception as e:
            logger.error(f"❌ 获取所有替代关系失败: {e}")
            return []

    @staticmethod
    def delete_substitution(substitution_id: int) -> bool:
        """删除替代关系"""
        try:
            substitution = IngredientSubstitution.query.get(substitution_id)
            if substitution:
                db.session.delete(substitution)
                db.session.commit()
                logger.info(f"✅ 删除替代关系成功: ID {substitution_id}")
                return True
            logger.warning(f"⚠️  替代关系不存在: ID {substitution_id}")
            return False
        except Exception as e:
            logger.error(f"❌ 删除替代关系失败: {e}")
            db.session.rollback()
            return False


# 创建全局服务实例
substitution_service = SubstitutionService()
