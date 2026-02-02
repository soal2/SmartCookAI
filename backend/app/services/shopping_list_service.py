"""
Shopping List Service
购物清单管理服务
"""
import logging
from typing import List, Dict, Any, Optional
from app.database import db
from app.models.shopping_list import ShoppingListItem
from app.models.recipe import Recipe
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ShoppingListService:
    """购物清单服务"""

    @staticmethod
    def get_shopping_list() -> List[Dict[str, Any]]:
        """获取购物清单"""
        try:
            items = ShoppingListItem.query.order_by(ShoppingListItem.created_at.desc()).all()
            logger.info(f"✅ 获取购物清单成功，共 {len(items)} 个项目")
            return [item.to_dict() for item in items]
        except Exception as e:
            logger.error(f"❌ 获取购物清单失败: {e}")
            return []

    @staticmethod
    def add_item(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """添加项目"""
        try:
            item = ShoppingListItem(
                ingredient_name=data.get('ingredient_name'),
                quantity=data.get('quantity'),
                category=data.get('category'),
                recipe_id=data.get('recipe_id')
            )
            db.session.add(item)
            db.session.commit()
            logger.info(f"✅ 添加购物项目成功: {item.ingredient_name}")
            return item.to_dict()
        except Exception as e:
            logger.error(f"❌ 添加购物项目失败: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def update_item(item_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新项目"""
        try:
            item = ShoppingListItem.query.get(item_id)
            if not item:
                return None

            if 'ingredient_name' in data:
                item.ingredient_name = data['ingredient_name']
            if 'quantity' in data:
                item.quantity = data['quantity']
            if 'category' in data:
                item.category = data['category']
            if 'is_purchased' in data:
                item.is_purchased = data['is_purchased']

            db.session.commit()
            logger.info(f"✅ 更新购物项目成功: {item.ingredient_name}")
            return item.to_dict()
        except Exception as e:
            logger.error(f"❌ 更新购物项目失败: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def delete_item(item_id: int) -> bool:
        """删除项目"""
        try:
            item = ShoppingListItem.query.get(item_id)
            if item:
                db.session.delete(item)
                db.session.commit()
                logger.info(f"✅ 删除购物项目成功: ID {item_id}")
                return True
            logger.warning(f"⚠️  购物项目不存在: ID {item_id}")
            return False
        except Exception as e:
            logger.error(f"❌ 删除购物项目失败: {e}")
            db.session.rollback()
            return False

    @staticmethod
    def mark_as_purchased(item_id: int) -> Optional[Dict[str, Any]]:
        """标记为已购买"""
        try:
            item = ShoppingListItem.query.get(item_id)
            if item:
                item.is_purchased = True
                db.session.commit()
                logger.info(f"✅ 标记已购买成功: {item.ingredient_name}")
                return item.to_dict()
            logger.warning(f"⚠️  购物项目不存在: ID {item_id}")
            return None
        except Exception as e:
            logger.error(f"❌ 标记已购买失败: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def generate_from_recipe(recipe_id: int) -> List[Dict[str, Any]]:
        """从菜谱生成购物清单"""
        try:
            recipe = Recipe.query.get(recipe_id)
            if not recipe:
                return []

            ingredients = json.loads(recipe.ingredients_json) if recipe.ingredients_json else []
            added_items = []

            for ing in ingredients:
                # 只添加需要补充的食材
                if ing.get('status') == '需补充':
                    item = ShoppingListItem(
                        ingredient_name=ing.get('name'),
                        quantity=ing.get('quantity'),
                        category=ing.get('category', ''),
                        recipe_id=recipe_id
                    )
                    db.session.add(item)
                    added_items.append(item)

            db.session.commit()
            logger.info(f"✅ 从菜谱 {recipe_id} 生成购物清单成功，添加 {len(added_items)} 个项目")
            return [item.to_dict() for item in added_items]
        except Exception as e:
            logger.error(f"❌ 从菜谱生成购物清单失败: {e}")
            db.session.rollback()
            return []

    @staticmethod
    def clear_purchased() -> bool:
        """清除已购买项目"""
        try:
            count = ShoppingListItem.query.filter_by(is_purchased=True).count()
            ShoppingListItem.query.filter_by(is_purchased=True).delete()
            db.session.commit()
            logger.info(f"✅ 清除已购买项目成功，共清除 {count} 个")
            return True
        except Exception as e:
            logger.error(f"❌ 清除已购买项目失败: {e}")
            db.session.rollback()
            return False


# 创建全局服务实例
shopping_list_service = ShoppingListService()
