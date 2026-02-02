"""
Ingredient Model
食材数据模型
"""
from datetime import datetime
from app.database import db

class Ingredient(db.Model):
    """食材表"""
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50))
    state = db.Column(db.String(20))  # 新鲜/冷冻/常温
    category = db.Column(db.String(50))  # 蔬菜/肉禽/海鲜/主食/调料
    storage_location = db.Column(db.String(20))  # fridge/freezer/pantry
    is_common = db.Column(db.Boolean, default=False)  # 是否常用食材
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'state': self.state,
            'category': self.category,
            'storage_location': self.storage_location,
            'is_common': self.is_common,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Ingredient {self.name}>'
