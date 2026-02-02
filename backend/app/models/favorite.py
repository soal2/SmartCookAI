"""
Favorite Model
收藏数据模型
"""
from datetime import datetime
from app.database import db

class FavoriteGroup(db.Model):
    """收藏分组表"""
    __tablename__ = 'favorite_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联关系
    favorites = db.relationship('Favorite', backref='group', lazy=True)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'favorites_count': len(self.favorites)
        }

    def __repr__(self):
        return f'<FavoriteGroup {self.name}>'


class Favorite(db.Model):
    """收藏表"""
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('favorite_groups.id'))
    notes = db.Column(db.Text)  # 用户备注
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, include_recipe=True):
        """转换为字典"""
        result = {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'group_id': self.group_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_recipe and self.recipe:
            result['recipe'] = self.recipe.to_dict()

        return result

    def __repr__(self):
        return f'<Favorite recipe_id={self.recipe_id}>'
