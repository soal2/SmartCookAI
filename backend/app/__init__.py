"""
SmartCook AI Backend Application
应用初始化和配置
"""
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

# 创建速率限制器实例
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

def create_app():
    """创建并配置 Flask 应用"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # 验证配置
    try:
        Config.validate()
    except ValueError as e:
        print(f"[WARNING] Configuration error: {e}")
        print("Please copy .env.example to .env and configure DASHSCOPE_API_KEY")

    # 初始化数据库
    from app.database import init_db
    init_db(app)

    # 配置 CORS - 允许所有来源（开发环境）
    CORS(app, resources={r"/*": {"origins": "*"}})

    # 初始化速率限制器
    limiter.init_app(app)

    # 注册路由
    from app.routes import recipes, ingredients, favorites, shopping_list, substitutions

    app.register_blueprint(recipes.bp)
    app.register_blueprint(ingredients.bp)
    app.register_blueprint(favorites.bp)
    app.register_blueprint(shopping_list.bp)
    app.register_blueprint(substitutions.bp)

    # 健康检查端点
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'SmartCook AI Backend'}

    return app
