"""
Ingredient Service
食材管理服务
"""
import logging
from typing import List, Dict, Any, Optional
from app.database import db
from app.models.ingredient import Ingredient

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IngredientService:
    """食材服务"""

    @staticmethod
    def get_all_ingredients() -> List[Dict[str, Any]]:
        """获取所有食材"""
        try:
            ingredients = Ingredient.query.order_by(Ingredient.created_at.desc()).all()
            logger.info(f"✅ 获取所有食材成功，共 {len(ingredients)} 个")
            return [ing.to_dict() for ing in ingredients]
        except Exception as e:
            logger.error(f"❌ 获取食材失败: {e}")
            return []

    @staticmethod
    def get_ingredients_by_category(category: str) -> List[Dict[str, Any]]:
        """按分类获取食材"""
        try:
            ingredients = Ingredient.query.filter_by(category=category).all()
            logger.info(f"✅ 按分类 '{category}' 获取食材成功，共 {len(ingredients)} 个")
            return [ing.to_dict() for ing in ingredients]
        except Exception as e:
            logger.error(f"❌ 按分类获取食材失败: {e}")
            return []

    @staticmethod
    def get_ingredients_by_storage(storage: str) -> List[Dict[str, Any]]:
        """按存储位置获取食材"""
        try:
            ingredients = Ingredient.query.filter_by(storage_location=storage).all()
            logger.info(f"✅ 按存储位置 '{storage}' 获取食材成功，共 {len(ingredients)} 个")
            return [ing.to_dict() for ing in ingredients]
        except Exception as e:
            logger.error(f"❌ 按存储位置获取食材失败: {e}")
            return []

    @staticmethod
    def get_common_ingredients() -> List[Dict[str, Any]]:
        """获取常用食材"""
        try:
            ingredients = Ingredient.query.filter_by(is_common=True).all()
            logger.info(f"✅ 获取常用食材成功，共 {len(ingredients)} 个")
            return [ing.to_dict() for ing in ingredients]
        except Exception as e:
            logger.error(f"❌ 获取常用食材失败: {e}")
            return []

    @staticmethod
    def add_ingredient(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """添加食材"""
        try:
            ingredient = Ingredient(
                name=data.get('name'),
                quantity=data.get('quantity'),
                state=data.get('state'),
                category=data.get('category'),
                storage_location=data.get('storage_location'),
                is_common=data.get('is_common', False)
            )
            db.session.add(ingredient)
            db.session.commit()
            logger.info(f"✅ 添加食材成功: {ingredient.name}")
            return ingredient.to_dict()
        except Exception as e:
            logger.error(f"❌ 添加食材失败: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def update_ingredient(ingredient_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新食材"""
        try:
            ingredient = Ingredient.query.get(ingredient_id)
            if not ingredient:
                return None

            if 'name' in data:
                ingredient.name = data['name']
            if 'quantity' in data:
                ingredient.quantity = data['quantity']
            if 'state' in data:
                ingredient.state = data['state']
            if 'category' in data:
                ingredient.category = data['category']
            if 'storage_location' in data:
                ingredient.storage_location = data['storage_location']
            if 'is_common' in data:
                ingredient.is_common = data['is_common']

            db.session.commit()
            logger.info(f"✅ 更新食材成功: {ingredient.name}")
            return ingredient.to_dict()
        except Exception as e:
            logger.error(f"❌ 更新食材失败: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def delete_ingredient(ingredient_id: int) -> bool:
        """删除食材"""
        try:
            ingredient = Ingredient.query.get(ingredient_id)
            if ingredient:
                db.session.delete(ingredient)
                db.session.commit()
                logger.info(f"✅ 删除食材成功: ID {ingredient_id}")
                return True
            logger.warning(f"⚠️  食材不存在: ID {ingredient_id}")
            return False
        except Exception as e:
            logger.error(f"❌ 删除食材失败: {e}")
            db.session.rollback()
            return False

    @staticmethod
    def mark_as_common(ingredient_id: int) -> Optional[Dict[str, Any]]:
        """标记为常用食材"""
        try:
            ingredient = Ingredient.query.get(ingredient_id)
            if ingredient:
                ingredient.is_common = True
                db.session.commit()
                logger.info(f"✅ 标记常用食材成功: {ingredient.name}")
                return ingredient.to_dict()
            logger.warning(f"⚠️  食材不存在: ID {ingredient_id}")
            return None
        except Exception as e:
            logger.error(f"❌ 标记常用食材失败: {e}")
            db.session.rollback()
            return None


# 创建全局服务实例
ingredient_service = IngredientService()
