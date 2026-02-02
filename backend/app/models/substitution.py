"""
Ingredient Substitution Model
食材替代关系模型
"""
from app.database import db
from datetime import datetime


class IngredientSubstitution(db.Model):
    """食材替代关系表"""
    __tablename__ = 'ingredient_substitutions'

    id = db.Column(db.Integer, primary_key=True)
    original_ingredient = db.Column(db.String(100), nullable=False, index=True)
    substitute_ingredient = db.Column(db.String(100), nullable=False)
    similarity_score = db.Column(db.Float, default=0.8)  # 相似度评分 0-1
    substitution_ratio = db.Column(db.String(50), default='1:1')  # 替代比例
    notes = db.Column(db.Text)  # 替代说明
    category = db.Column(db.String(50))  # 食材分类
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'original_ingredient': self.original_ingredient,
            'substitute_ingredient': self.substitute_ingredient,
            'similarity_score': self.similarity_score,
            'substitution_ratio': self.substitution_ratio,
            'notes': self.notes,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
