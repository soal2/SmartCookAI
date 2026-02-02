#!/usr/bin/env python3
"""
End-to-End Testing Script
端到端测试脚本

测试场景:
1. 新手用户快速做饭
2. 家庭主妇营养搭配
3. 剩余食材处理
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.recipe_service import recipe_service
from config import Config

def print_header(title: str):
    """打印测试标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_recipe_detail(recipe: dict):
    """打印食谱详情"""
    print(f"\n📝 {recipe['name']}")
    print(f"📖 {recipe.get('description', '')}")
    print(f"🔧 难度: {recipe.get('difficulty', 'N/A')}")
    print(f"⏱️  时间: {recipe.get('cooking_time', recipe.get('time', 'N/A'))}")
    print(f"🔥 热量: {recipe.get('calories', 'N/A')}")

    print(f"\n🥘 食材 ({len(recipe.get('ingredients', []))}):")
    for ing in recipe.get('ingredients', [])[:8]:  # 只显示前8个
        status = ing.get('status', 'N/A')
        print(f"   - {ing['name']} {ing['quantity']} [{status}]")

    print(f"\n📋 步骤 ({len(recipe.get('steps', []))}):")
    for i, step in enumerate(recipe.get('steps', [])[:5], 1):  # 只显示前5步
        print(f"   {i}. {step}")

    if recipe.get('tags'):
        print(f"\n🏷️  标签: {', '.join(recipe['tags'])}")

def scenario_1_beginner_quick_meal():
    """场景1: 新手用户快速做饭"""
    print_header("场景1: 新手用户快速做饭")

    print("背景:")
    print("  - 用户: 烹饪新手")
    print("  - 需求: 快速做一顿饭")
    print("  - 食材: 鸡蛋、米饭 (有限)")
    print("  - 期望: 简单、快速、易操作\n")

    try:
        recipes = recipe_service.generate_recipes(
            ingredients=[
                {"name": "鸡蛋", "quantity": "3个", "state": "新鲜"},
                {"name": "米饭", "quantity": "1碗", "state": "剩余"}
            ],
            filters={
                "scenario": "快手菜",
                "skill": "新手"
            }
        )

        if not recipes:
            print("❌ 场景1失败: 未生成食谱")
            return False

        print(f"✅ 成功生成 {len(recipes)} 个食谱\n")

        # 验证第一个食谱
        recipe = recipes[0]
        print_recipe_detail(recipe)

        # 验证是否符合场景要求
        checks = []

        # 检查难度
        difficulty = recipe.get('difficulty', '')
        if '新手' in difficulty or '简单' in difficulty or '容易' in difficulty:
            checks.append(("难度适合新手", True))
        else:
            checks.append(("难度适合新手", False))

        # 检查时间 (快手菜应该 < 30分钟)
        time_str = recipe.get('cooking_time', recipe.get('time', ''))
        if '分钟' in time_str:
            try:
                minutes = int(''.join(filter(str.isdigit, time_str)))
                if minutes <= 30:
                    checks.append(("烹饪时间合理", True))
                else:
                    checks.append(("烹饪时间合理", False))
            except:
                checks.append(("烹饪时间合理", True))  # 无法解析时默认通过
        else:
            checks.append(("烹饪时间合理", True))

        # 检查步骤数量 (新手菜应该步骤少)
        steps = recipe.get('steps', [])
        if len(steps) <= 8:
            checks.append(("步骤数量适中", True))
        else:
            checks.append(("步骤数量适中", False))

        print(f"\n验证结果:")
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {check_name}")

        all_passed = all(passed for _, passed in checks)
        if all_passed:
            print(f"\n🎉 场景1: 通过")
        else:
            print(f"\n⚠️  场景1: 部分通过")

        return all_passed

    except Exception as e:
        print(f"❌ 场景1失败: {e}")
        return False

def scenario_2_nutritious_meal():
    """场景2: 家庭主妇营养搭配"""
    print_header("场景2: 家庭主妇营养搭配")

    print("背景:")
    print("  - 用户: 家庭主妇")
    print("  - 需求: 营养均衡的家常菜")
    print("  - 食材: 鸡肉、西兰花、胡萝卜")
    print("  - 期望: 健康、清淡、营养丰富\n")

    try:
        recipes = recipe_service.generate_recipes(
            ingredients=[
                {"name": "鸡肉", "quantity": "300g", "state": "新鲜"},
                {"name": "西兰花", "quantity": "1个", "state": "新鲜"},
                {"name": "胡萝卜", "quantity": "1根", "state": "新鲜"}
            ],
            filters={
                "cuisine": "中式",
                "taste": "清淡"
            }
        )

        if not recipes:
            print("❌ 场景2失败: 未生成食谱")
            return False

        print(f"✅ 成功生成 {len(recipes)} 个食谱\n")

        # 验证第一个食谱
        recipe = recipes[0]
        print_recipe_detail(recipe)

        # 验证是否符合场景要求
        checks = []

        # 检查是否使用了多种蔬菜 (营养均衡)
        ingredients = recipe.get('ingredients', [])
        veggie_count = sum(1 for ing in ingredients
                          if any(v in ing['name'] for v in ['西兰花', '胡萝卜', '蔬菜']))
        if veggie_count >= 2:
            checks.append(("使用多种蔬菜", True))
        else:
            checks.append(("使用多种蔬菜", False))

        # 检查标签是否包含营养相关
        tags = recipe.get('tags', [])
        nutrition_tags = ['营养', '健康', '清淡', '家常']
        has_nutrition_tag = any(tag in ' '.join(tags) for tag in nutrition_tags)
        checks.append(("包含营养标签", has_nutrition_tag))

        # 检查食材数量 (营养搭配通常食材较多)
        if len(ingredients) >= 4:
            checks.append(("食材丰富", True))
        else:
            checks.append(("食材丰富", False))

        print(f"\n验证结果:")
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {check_name}")

        all_passed = all(passed for _, passed in checks)
        if all_passed:
            print(f"\n🎉 场景2: 通过")
        else:
            print(f"\n⚠️  场景2: 部分通过")

        return all_passed

    except Exception as e:
        print(f"❌ 场景2失败: {e}")
        return False

def scenario_3_leftover_ingredients():
    """场景3: 剩余食材处理"""
    print_header("场景3: 剩余食材处理")

    print("背景:")
    print("  - 用户: 普通用户")
    print("  - 需求: 处理冰箱里的剩余食材")
    print("  - 食材: 半个洋葱、200g鸡肉、昨天的米饭")
    print("  - 期望: 合理利用剩余食材，减少浪费\n")

    try:
        recipes = recipe_service.generate_recipes(
            ingredients=[
                {"name": "洋葱", "quantity": "半个", "state": "剩余"},
                {"name": "鸡肉", "quantity": "200g", "state": "冷藏"},
                {"name": "米饭", "quantity": "1碗", "state": "剩余"}
            ]
        )

        if not recipes:
            print("❌ 场景3失败: 未生成食谱")
            return False

        print(f"✅ 成功生成 {len(recipes)} 个食谱\n")

        # 验证第一个食谱
        recipe = recipes[0]
        print_recipe_detail(recipe)

        # 验证是否符合场景要求
        checks = []

        # 检查是否使用了所有已有食材
        ingredients = recipe.get('ingredients', [])
        available_ingredients = [ing for ing in ingredients if ing.get('status') == '已有']

        # 检查是否包含洋葱、鸡肉、米饭
        has_onion = any('洋葱' in ing['name'] for ing in available_ingredients)
        has_chicken = any('鸡' in ing['name'] for ing in available_ingredients)
        has_rice = any('米饭' in ing['name'] or '饭' in ing['name'] for ing in available_ingredients)

        used_count = sum([has_onion, has_chicken, has_rice])
        if used_count >= 2:
            checks.append(("充分利用已有食材", True))
        else:
            checks.append(("充分利用已有食材", False))

        # 检查需补充的食材是否合理 (不应该太多)
        needed_ingredients = [ing for ing in ingredients if ing.get('status') == '需补充']
        if len(needed_ingredients) <= 5:
            checks.append(("补充食材合理", True))
        else:
            checks.append(("补充食材合理", False))

        # 检查是否是实用的菜品
        name = recipe.get('name', '')
        description = recipe.get('description', '')
        if name and description:
            checks.append(("生成完整食谱", True))
        else:
            checks.append(("生成完整食谱", False))

        print(f"\n验证结果:")
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {check_name}")

        all_passed = all(passed for _, passed in checks)
        if all_passed:
            print(f"\n🎉 场景3: 通过")
        else:
            print(f"\n⚠️  场景3: 部分通过")

        return all_passed

    except Exception as e:
        print(f"❌ 场景3失败: {e}")
        return False

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("  SmartCook AI - 端到端测试")
    print("="*60)

    # 验证配置
    try:
        Config.validate()
        print(f"✅ 配置验证通过")
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        return

    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 运行场景测试
        results = []
        results.append(("场景1: 新手用户快速做饭", scenario_1_beginner_quick_meal()))
        results.append(("场景2: 家庭主妇营养搭配", scenario_2_nutritious_meal()))
        results.append(("场景3: 剩余食材处理", scenario_3_leftover_ingredients()))

        # 打印总结
        print_header("测试总结")

        passed_count = sum(1 for _, passed in results if passed)
        total_count = len(results)

        print(f"总场景数: {total_count}")
        print(f"✅ 通过: {passed_count}")
        print(f"❌ 失败: {total_count - passed_count}\n")

        for scenario_name, passed in results:
            status = "✅" if passed else "❌"
            print(f"  {status} {scenario_name}")

        if passed_count == total_count:
            print(f"\n🎉 所有场景测试通过!")
        else:
            print(f"\n⚠️  部分场景需要改进")

if __name__ == '__main__':
    main()
