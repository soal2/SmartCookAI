"""
Database Initialization Script
数据库初始化脚本
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.database import db
from app.models.ingredient import Ingredient
from app.models.favorite import FavoriteGroup
from app.models.substitution import IngredientSubstitution

def init_database():
    """初始化数据库并创建示例数据"""
    app = create_app()

    with app.app_context():
        # 创建所有表
        print("🔧 正在创建数据库表...")
        db.create_all()
        print("✅ 数据库表创建成功")

        # 检查是否已有数据
        if Ingredient.query.first():
            print("ℹ️  数据库已包含数据，跳过示例数据创建")
            return

        # 创建示例食材
        print("📦 正在创建示例食材...")
        sample_ingredients = [
            Ingredient(
                name="新鲜鸡蛋",
                quantity="6个",
                state="新鲜",
                category="主食",
                storage_location="fridge",
                is_common=True
            ),
            Ingredient(
                name="全脂牛奶",
                quantity="2盒",
                state="新鲜",
                category="主食",
                storage_location="fridge",
                is_common=True
            ),
            Ingredient(
                name="西红柿",
                quantity="4个",
                state="新鲜",
                category="蔬菜",
                storage_location="fridge"
            ),
            Ingredient(
                name="肥牛卷",
                quantity="1盒",
                state="冷冻",
                category="肉禽",
                storage_location="freezer"
            ),
            Ingredient(
                name="大米",
                quantity="5kg",
                state="常温",
                category="主食",
                storage_location="pantry",
                is_common=True
            ),
            Ingredient(
                name="酱油",
                quantity="1瓶",
                state="常温",
                category="调料",
                storage_location="pantry",
                is_common=True
            )
        ]

        for ing in sample_ingredients:
            db.session.add(ing)

        # 创建示例收藏分组
        print("📁 正在创建示例收藏分组...")
        sample_groups = [
            FavoriteGroup(name="减脂餐", description="健康低卡路里食谱"),
            FavoriteGroup(name="快手菜", description="15分钟快速料理"),
            FavoriteGroup(name="家常菜", description="经典家常美味")
        ]

        for group in sample_groups:
            db.session.add(group)

        # 创建食材替代关系数据
        print("🔄 正在创建食材替代关系...")
        sample_substitutions = [
            # 调料类替代
            IngredientSubstitution(
                original_ingredient="柠檬汁",
                substitute_ingredient="白醋",
                similarity_score=0.85,
                substitution_ratio="1:1",
                notes="酸味替代，适合凉拌菜和腌制",
                category="调料"
            ),
            IngredientSubstitution(
                original_ingredient="柠檬汁",
                substitute_ingredient="青柠汁",
                similarity_score=0.95,
                substitution_ratio="1:1",
                notes="风味相近，可直接替代",
                category="调料"
            ),
            IngredientSubstitution(
                original_ingredient="黄油",
                substitute_ingredient="植物油",
                similarity_score=0.75,
                substitution_ratio="1:0.8",
                notes="减少用量，口感略有差异",
                category="调料"
            ),
            IngredientSubstitution(
                original_ingredient="黄油",
                substitute_ingredient="椰子油",
                similarity_score=0.80,
                substitution_ratio="1:1",
                notes="健康替代，带有椰香",
                category="调料"
            ),
            IngredientSubstitution(
                original_ingredient="生抽",
                substitute_ingredient="老抽",
                similarity_score=0.70,
                substitution_ratio="1:0.5",
                notes="颜色更深，减少用量",
                category="调料"
            ),
            IngredientSubstitution(
                original_ingredient="料酒",
                substitute_ingredient="白葡萄酒",
                similarity_score=0.85,
                substitution_ratio="1:1",
                notes="去腥效果相似",
                category="调料"
            ),
            IngredientSubstitution(
                original_ingredient="蚝油",
                substitute_ingredient="生抽+糖",
                similarity_score=0.70,
                substitution_ratio="1勺蚝油=1勺生抽+少许糖",
                notes="鲜味略有差异",
                category="调料"
            ),
            # 奶制品类替代
            IngredientSubstitution(
                original_ingredient="牛奶",
                substitute_ingredient="豆浆",
                similarity_score=0.80,
                substitution_ratio="1:1",
                notes="植物蛋白替代，适合乳糖不耐受",
                category="蛋奶"
            ),
            IngredientSubstitution(
                original_ingredient="牛奶",
                substitute_ingredient="椰奶",
                similarity_score=0.75,
                substitution_ratio="1:1",
                notes="带有椰香，适合东南亚菜",
                category="蛋奶"
            ),
            IngredientSubstitution(
                original_ingredient="淡奶油",
                substitute_ingredient="牛奶+黄油",
                similarity_score=0.80,
                substitution_ratio="1杯奶油=3/4杯牛奶+1/4杯黄油",
                notes="口感相似",
                category="蛋奶"
            ),
            # 主食类替代
            IngredientSubstitution(
                original_ingredient="面粉",
                substitute_ingredient="玉米淀粉",
                similarity_score=0.60,
                substitution_ratio="1:0.5",
                notes="仅适合勾芡，不适合做面食",
                category="主食"
            ),
            IngredientSubstitution(
                original_ingredient="白米",
                substitute_ingredient="糙米",
                similarity_score=0.85,
                substitution_ratio="1:1",
                notes="更健康，需要更长烹饪时间",
                category="主食"
            ),
            IngredientSubstitution(
                original_ingredient="意大利面",
                substitute_ingredient="荞麦面",
                similarity_score=0.75,
                substitution_ratio="1:1",
                notes="口感略有不同，更健康",
                category="主食"
            ),
            # 蔬菜类替代
            IngredientSubstitution(
                original_ingredient="洋葱",
                substitute_ingredient="大葱",
                similarity_score=0.75,
                substitution_ratio="1:1",
                notes="辛辣味相似，适合炒菜",
                category="蔬菜"
            ),
            IngredientSubstitution(
                original_ingredient="西兰花",
                substitute_ingredient="菜花",
                similarity_score=0.90,
                substitution_ratio="1:1",
                notes="口感和营养相似",
                category="蔬菜"
            ),
            IngredientSubstitution(
                original_ingredient="菠菜",
                substitute_ingredient="小白菜",
                similarity_score=0.80,
                substitution_ratio="1:1",
                notes="绿叶菜替代",
                category="蔬菜"
            ),
            # 肉类替代
            IngredientSubstitution(
                original_ingredient="鸡胸肉",
                substitute_ingredient="鸡腿肉",
                similarity_score=0.85,
                substitution_ratio="1:1",
                notes="鸡腿肉更嫩，脂肪含量稍高",
                category="肉禽"
            ),
            IngredientSubstitution(
                original_ingredient="猪肉",
                substitute_ingredient="牛肉",
                similarity_score=0.70,
                substitution_ratio="1:1",
                notes="口感不同，烹饪时间可能需要调整",
                category="肉禽"
            ),
            IngredientSubstitution(
                original_ingredient="虾",
                substitute_ingredient="鱿鱼",
                similarity_score=0.75,
                substitution_ratio="1:1",
                notes="海鲜类替代，口感略有不同",
                category="海鲜"
            ),
            # 调味品类替代
            IngredientSubstitution(
                original_ingredient="白糖",
                substitute_ingredient="蜂蜜",
                similarity_score=0.80,
                substitution_ratio="1:0.75",
                notes="蜂蜜更甜，减少用量",
                category="调料"
            ),
            IngredientSubstitution(
                original_ingredient="盐",
                substitute_ingredient="酱油",
                similarity_score=0.70,
                substitution_ratio="1勺盐=2勺酱油",
                notes="会增加颜色和鲜味",
                category="调料"
            ),
            IngredientSubstitution(
                original_ingredient="大蒜",
                substitute_ingredient="蒜粉",
                similarity_score=0.75,
                substitution_ratio="1瓣蒜=1/8勺蒜粉",
                notes="风味略有差异",
                category="调料"
            ),
            IngredientSubstitution(
                original_ingredient="生姜",
                substitute_ingredient="姜粉",
                similarity_score=0.70,
                substitution_ratio="1片姜=1/4勺姜粉",
                notes="新鲜生姜风味更佳",
                category="调料"
            ),
            IngredientSubstitution(
                original_ingredient="香菜",
                substitute_ingredient="葱花",
                similarity_score=0.65,
                substitution_ratio="1:1",
                notes="提香作用相似",
                category="蔬菜"
            ),
            IngredientSubstitution(
                original_ingredient="番茄酱",
                substitute_ingredient="番茄+糖",
                similarity_score=0.75,
                substitution_ratio="1勺番茄酱=2个番茄+少许糖",
                notes="需要煮制浓缩",
                category="调料"
            )
        ]

        for sub in sample_substitutions:
            db.session.add(sub)

        # 提交所有更改
        db.session.commit()
        print("✅ 示例数据创建成功")

        # 显示统计信息
        print("\n📊 数据库统计:")
        print(f"  - 食材数量: {Ingredient.query.count()}")
        print(f"  - 收藏分组: {FavoriteGroup.query.count()}")
        print(f"  - 替代关系: {IngredientSubstitution.query.count()}")
        print("\n🎉 数据库初始化完成！")

if __name__ == '__main__':
    init_database()
