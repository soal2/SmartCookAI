"""
API Testing Script
测试所有 API 端点
"""
import sys
sys.path.insert(0, '/Users/eversse/Documents/codes/VibeCoding/SmartCookAI/backend')

from app import create_app
from app.services.ingredient_service import ingredient_service
from app.services.favorite_service import favorite_service
from app.services.shopping_list_service import shopping_list_service
from app.services.recipe_service import recipe_service

def test_ingredients():
    """测试食材管理"""
    print("\n" + "="*50)
    print("📦 测试食材管理")
    print("="*50)

    # 获取所有食材
    ingredients = ingredient_service.get_all_ingredients()
    print(f"✅ 获取所有食材: {len(ingredients)} 个")

    # 获取常用食材
    common = ingredient_service.get_common_ingredients()
    print(f"✅ 常用食材: {len(common)} 个")

    # 按存储位置获取
    fridge = ingredient_service.get_ingredients_by_storage('fridge')
    print(f"✅ 冰箱食材: {len(fridge)} 个")

    # 添加新食材
    new_ing = ingredient_service.add_ingredient({
        'name': '测试食材',
        'quantity': '1个',
        'state': '新鲜',
        'category': '蔬菜',
        'storage_location': 'fridge'
    })
    print(f"✅ 添加食材: {new_ing['name']}")

    # 更新食材
    updated = ingredient_service.update_ingredient(new_ing['id'], {'quantity': '2个'})
    print(f"✅ 更新食材: {updated['name']} -> {updated['quantity']}")

    # 删除食材
    deleted = ingredient_service.delete_ingredient(new_ing['id'])
    print(f"✅ 删除食材: {deleted}")

def test_favorites():
    """测试收藏功能"""
    print("\n" + "="*50)
    print("⭐ 测试收藏功能")
    print("="*50)

    # 获取所有分组
    groups = favorite_service.get_all_groups()
    print(f"✅ 收藏分组: {len(groups)} 个")
    for group in groups:
        print(f"  - {group['name']}: {group['description']}")

    # 创建新分组
    new_group = favorite_service.create_group({
        'name': '测试分组',
        'description': '这是一个测试分组'
    })
    print(f"✅ 创建分组: {new_group['name']}")

    # 删除分组
    deleted = favorite_service.delete_group(new_group['id'])
    print(f"✅ 删除分组: {deleted}")

def test_shopping_list():
    """测试购物清单"""
    print("\n" + "="*50)
    print("🛒 测试购物清单")
    print("="*50)

    # 获取购物清单
    items = shopping_list_service.get_shopping_list()
    print(f"✅ 购物清单项目: {len(items)} 个")

    # 添加项目
    new_item = shopping_list_service.add_item({
        'ingredient_name': '测试食材',
        'quantity': '1kg',
        'category': '蔬菜'
    })
    print(f"✅ 添加购物项: {new_item['ingredient_name']}")

    # 标记为已购买
    purchased = shopping_list_service.mark_as_purchased(new_item['id'])
    print(f"✅ 标记已购买: {purchased['is_purchased']}")

    # 清除已购买
    cleared = shopping_list_service.clear_purchased()
    print(f"✅ 清除已购买项目: {cleared}")

def test_recipes():
    """测试食谱功能"""
    print("\n" + "="*50)
    print("🍳 测试食谱功能")
    print("="*50)

    # 获取历史记录
    history = recipe_service.get_recipe_history(limit=10)
    print(f"✅ 历史记录: {len(history)} 条")

    # 保存测试食谱
    test_recipe = {
        'name': '测试食谱',
        'description': '这是一个测试食谱',
        'difficulty': '新手',
        'time': '15分钟',
        'calories': '300卡',
        'ingredients': [
            {'name': '鸡蛋', 'quantity': '2个', 'status': '已有'}
        ],
        'steps': ['步骤1', '步骤2'],
        'tags': ['快手菜']
    }
    saved = recipe_service.save_recipe_to_history(test_recipe)
    if saved:
        print(f"✅ 保存食谱: {saved.name}")

        # 获取单个食谱
        recipe = recipe_service.get_recipe_by_id(saved.id)
        print(f"✅ 获取食谱: {recipe['name']}")

        # 删除食谱
        deleted = recipe_service.delete_recipe(saved.id)
        print(f"✅ 删除食谱: {deleted}")

def main():
    """运行所有测试"""
    app = create_app()

    with app.app_context():
        print("\n🧪 开始测试 SmartCook AI 数据库功能")

        test_ingredients()
        test_favorites()
        test_shopping_list()
        test_recipes()

        print("\n" + "="*50)
        print("✅ 所有测试完成！")
        print("="*50)

if __name__ == '__main__':
    main()
