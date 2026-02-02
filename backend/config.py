"""
SmartCook AI Backend Configuration
配置文件：管理环境变量和应用配置
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置类"""

    # Flask 配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

    # 数据库配置
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(BASE_DIR, "smartcook.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Dashscope API 配置
    DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')

    # CORS 配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')

    # AI 模型配置
    MODEL_NAME = 'qwen-turbo'  # 可选: qwen-turbo, qwen-plus, qwen-max
    MAX_TOKENS = 2000
    TEMPERATURE = 0.8

    # 食谱生成配置
    RECIPES_PER_REQUEST = 3  # 每次生成3-5个食谱
    MIN_INGREDIENTS = 1
    MAX_INGREDIENTS = 20

    # 分页配置
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    # 允许的值 - 用于输入验证
    ALLOWED_CATEGORIES = ['蔬菜', '肉禽', '海鲜', '主食', '调料', '水果', '豆制品', '蛋奶']
    ALLOWED_STORAGE = ['fridge', 'freezer', 'pantry']
    ALLOWED_STATES = ['新鲜', '冷冻', '常温', '剩余']
    ALLOWED_CUISINES = ['中式', '西式', '日韩', '东南亚', '其他']
    ALLOWED_TASTES = ['酸', '甜', '苦', '辣', '咸', '清淡']
    ALLOWED_SCENARIOS = ['早餐', '快手菜', '硬菜', '宴客菜', '夜宵']
    ALLOWED_SKILLS = ['新手', '进阶', '专业']

    # SQLAlchemy 连接池配置
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,  # 使用前验证连接
        'max_overflow': 20
    }

    @staticmethod
    def validate():
        """验证必需的配置项"""
        if not Config.DASHSCOPE_API_KEY:
            raise ValueError("DASHSCOPE_API_KEY 未设置，请在 .env 文件中配置")

        # 验证 API key 不是占位符
        if Config.DASHSCOPE_API_KEY == 'your_api_key_here':
            raise ValueError("请在 .env 文件中设置真实的 DASHSCOPE_API_KEY")
