"""
Recipe Progress Model
食谱步骤进度数据模型
"""
from datetime import datetime
from app.database import db

class RecipeStepProgress(db.Model):
    """步骤完成状态表"""
    __tablename__ = 'recipe_step_progress'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    step_index = db.Column(db.Integer, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'step_index': self.step_index,
            'is_completed': self.is_completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    def __repr__(self):
        return f'<RecipeStepProgress recipe_id={self.recipe_id} step={self.step_index}>'
