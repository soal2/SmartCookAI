"""
Recipe Model
食谱数据模型
"""
import json
from datetime import datetime
from app.database import db

class Recipe(db.Model):
    """食谱历史表"""
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(20))  # 新手/进阶
    cooking_time = db.Column(db.String(50))
    calories = db.Column(db.String(50))
    cuisine = db.Column(db.String(50))  # 中式/西式/日韩/东南亚
    taste = db.Column(db.String(50))  # 酸/甜/苦/辣/咸/清淡
    scenario = db.Column(db.String(50))  # 早餐/快手菜/硬菜
    skill_level = db.Column(db.String(20))  # 新手/进阶
    ingredients_json = db.Column(db.Text)  # JSON 格式存储食材列表
    steps_json = db.Column(db.Text)  # JSON 格式存储步骤
    tags_json = db.Column(db.Text)  # JSON 格式存储标签
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联关系
    favorites = db.relationship('Favorite', backref='recipe', lazy=True, cascade='all, delete-orphan')
    shopping_items = db.relationship('ShoppingListItem', backref='recipe', lazy=True)
    step_progress = db.relationship('RecipeStepProgress', backref='recipe', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_progress=False):
        """转换为字典"""
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'difficulty': self.difficulty,
            'cooking_time': self.cooking_time,
            'calories': self.calories,
            'cuisine': self.cuisine,
            'taste': self.taste,
            'scenario': self.scenario,
            'skill_level': self.skill_level,
            'ingredients': json.loads(self.ingredients_json) if self.ingredients_json else [],
            'steps': json.loads(self.steps_json) if self.steps_json else [],
            'tags': json.loads(self.tags_json) if self.tags_json else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_progress:
            result['step_progress'] = [
                {
                    'step_index': p.step_index,
                    'is_completed': p.is_completed,
                    'completed_at': p.completed_at.isoformat() if p.completed_at else None
                }
                for p in self.step_progress
            ]

        return result

    @staticmethod
    def from_ai_response(recipe_data):
        """从 AI 响应创建 Recipe 对象"""
        return Recipe(
            name=recipe_data.get('name', ''),
            description=recipe_data.get('description', ''),
            difficulty=recipe_data.get('difficulty', ''),
            cooking_time=recipe_data.get('cooking_time', ''),
            calories=recipe_data.get('calories', ''),
            cuisine=recipe_data.get('cuisine', ''),
            taste=recipe_data.get('taste', ''),
            scenario=recipe_data.get('scenario', ''),
            skill_level=recipe_data.get('skill_level', ''),
            ingredients_json=json.dumps(recipe_data.get('ingredients', []), ensure_ascii=False),
            steps_json=json.dumps(recipe_data.get('steps', []), ensure_ascii=False),
            tags_json=json.dumps(recipe_data.get('tags', []), ensure_ascii=False)
        )

    def __repr__(self):
        return f'<Recipe {self.name}>'
