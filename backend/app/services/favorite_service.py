"""
Favorite Service
收藏管理服务
"""
import logging
from typing import List, Dict, Any, Optional
from app.database import db
from app.models.favorite import Favorite, FavoriteGroup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FavoriteService:
    """收藏服务"""

    @staticmethod
    def get_all_favorites() -> List[Dict[str, Any]]:
        """获取所有收藏"""
        try:
            favorites = Favorite.query.order_by(Favorite.created_at.desc()).all()
            logger.info(f"✅ 获取所有收藏成功，共 {len(favorites)} 个")
            return [fav.to_dict(include_recipe=True) for fav in favorites]
        except Exception as e:
            logger.error(f"❌ 获取收藏失败: {e}")
            return []

    @staticmethod
    def get_favorites_by_group(group_id: int) -> List[Dict[str, Any]]:
        """按分组获取收藏"""
        try:
            favorites = Favorite.query.filter_by(group_id=group_id).all()
            logger.info(f"✅ 按分组 {group_id} 获取收藏成功，共 {len(favorites)} 个")
            return [fav.to_dict(include_recipe=True) for fav in favorites]
        except Exception as e:
            logger.error(f"❌ 按分组获取收藏失败: {e}")
            return []

    @staticmethod
    def add_to_favorites(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """添加收藏"""
        try:
            favorite = Favorite(
                recipe_id=data.get('recipe_id'),
                group_id=data.get('group_id'),
                notes=data.get('notes')
            )
            db.session.add(favorite)
            db.session.commit()
            logger.info(f"✅ 添加收藏成功: Recipe ID {favorite.recipe_id}")
            return favorite.to_dict(include_recipe=True)
        except Exception as e:
            logger.error(f"❌ 添加收藏失败: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def remove_from_favorites(favorite_id: int) -> bool:
        """移除收藏"""
        try:
            favorite = Favorite.query.get(favorite_id)
            if favorite:
                db.session.delete(favorite)
                db.session.commit()
                logger.info(f"✅ 移除收藏成功: ID {favorite_id}")
                return True
            logger.warning(f"⚠️  收藏不存在: ID {favorite_id}")
            return False
        except Exception as e:
            logger.error(f"❌ 移除收藏失败: {e}")
            db.session.rollback()
            return False

    @staticmethod
    def get_all_groups() -> List[Dict[str, Any]]:
        """获取所有分组"""
        try:
            groups = FavoriteGroup.query.order_by(FavoriteGroup.created_at.desc()).all()
            logger.info(f"✅ 获取所有分组成功，共 {len(groups)} 个")
            return [group.to_dict() for group in groups]
        except Exception as e:
            logger.error(f"❌ 获取分组失败: {e}")
            return []

    @staticmethod
    def create_group(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """创建分组"""
        try:
            group = FavoriteGroup(
                name=data.get('name'),
                description=data.get('description')
            )
            db.session.add(group)
            db.session.commit()
            logger.info(f"✅ 创建分组成功: {group.name}")
            return group.to_dict()
        except Exception as e:
            logger.error(f"❌ 创建分组失败: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def update_group(group_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新分组"""
        try:
            group = FavoriteGroup.query.get(group_id)
            if not group:
                return None

            if 'name' in data:
                group.name = data['name']
            if 'description' in data:
                group.description = data['description']

            db.session.commit()
            logger.info(f"✅ 更新分组成功: {group.name}")
            return group.to_dict()
        except Exception as e:
            logger.error(f"❌ 更新分组失败: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def delete_group(group_id: int) -> bool:
        """删除分组"""
        try:
            group = FavoriteGroup.query.get(group_id)
            if group:
                db.session.delete(group)
                db.session.commit()
                logger.info(f"✅ 删除分组成功: ID {group_id}")
                return True
            logger.warning(f"⚠️  分组不存在: ID {group_id}")
            return False
        except Exception as e:
            logger.error(f"❌ 删除分组失败: {e}")
            db.session.rollback()
            return False


# 创建全局服务实例
favorite_service = FavoriteService()
