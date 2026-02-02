"""
SmartCook AI Database
数据库实例和初始化
"""
from flask_sqlalchemy import SQLAlchemy

# 创建数据库实例
db = SQLAlchemy()

def init_db(app):
    """初始化数据库"""
    db.init_app(app)

    with app.app_context():
        # 导入所有模型以确保表被创建
        from app.models import ingredient, recipe, favorite, shopping_list, recipe_progress

        # 创建所有表
        db.create_all()
        print("[OK] Database tables created successfully")
