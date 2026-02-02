"""
Shopping List Model
购物清单数据模型
"""
from datetime import datetime
from app.database import db

class ShoppingListItem(db.Model):
    """购物清单表"""
    __tablename__ = 'shopping_list'

    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50))
    category = db.Column(db.String(50))
    is_purchased = db.Column(db.Boolean, default=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))  # 可为空
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'ingredient_name': self.ingredient_name,
            'quantity': self.quantity,
            'category': self.category,
            'is_purchased': self.is_purchased,
            'recipe_id': self.recipe_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<ShoppingListItem {self.ingredient_name}>'
