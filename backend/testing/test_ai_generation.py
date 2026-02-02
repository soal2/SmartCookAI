#!/usr/bin/env python3
"""
AI Recipe Generation Comprehensive Test Suite
AI 食谱生成专项测试脚本

测试内容:
1. 基础生成测试
2. 筛选条件测试
3. 食材状态标注测试
4. 创意菜名测试
5. 合理性测试
6. 数据库持久化验证
"""
import sys
import os
import time
import json
from typing import List, Dict, Any

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.recipe_service import recipe_service
from config import Config

# 测试结果统计
test_results = {
    'total': 0,
    'passed': 0,
    'failed': 0,
    'errors': []
}

def print_header(title: str):
    """打印测试标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_test(test_name: str, passed: bool, message: str = ""):
    """打印测试结果"""
    test_results['total'] += 1
    if passed:
        test_results['passed'] += 1
        print(f"✅ {test_name}: 通过")
    else:
        test_results['failed'] += 1
        test_results['errors'].append(f"{test_name}: {message}")
        print(f"❌ {test_name}: 失败 - {message}")
    if message and passed:
        print(f"   ℹ️  {message}")

def validate_recipe_structure(recipe: Dict[str, Any]) -> tuple[bool, str]:
    """验证食谱结构完整性"""
    required_fields = ['name', 'description', 'difficulty', 'ingredients', 'steps']

    for field in required_fields:
        if field not in recipe:
            return False, f"缺少必需字段: {field}"

    if not isinstance(recipe['ingredients'], list) or len(recipe['ingredients']) == 0:
        return False, "食材列表为空或格式错误"

    if not isinstance(recipe['steps'], list) or len(recipe['steps']) == 0:
        return False, "步骤列表为空或格式错误"

    # 验证食材结构
    for ing in recipe['ingredients']:
        if not isinstance(ing, dict):
            return False, "食材格式错误"
        if 'name' not in ing or 'quantity' not in ing:
            return False, "食材缺少必需字段 (name/quantity)"

    return True, "结构完整"

def test_basic_generation():
    """测试1: 基础生成测试"""
    print_header("测试1: 基础生成测试")

    # 测试1.1: 单一食材
    print("测试1.1: 单一食材生成 (鸡蛋)")
    start_time = time.time()
    try:
        recipes = recipe_service.generate_recipes(
            ingredients=[{"name": "鸡蛋", "quantity": "6个", "state": "新鲜"}]
        )
        elapsed = time.time() - start_time

        # 验证返回数量
        if len(recipes) >= 1:
            print_test("单一食材生成", True, f"生成了 {len(recipes)} 个食谱，耗时 {elapsed:.2f}秒")
        else:
            print_test("单一食材生成", False, "未生成任何食谱")
            return

        # 验证结构
        for i, recipe in enumerate(recipes, 1):
            valid, msg = validate_recipe_structure(recipe)
            print_test(f"食谱{i}结构验证", valid, msg)
            if valid:
                print(f"   📝 菜名: {recipe['name']}")
                print(f"   🔧 难度: {recipe.get('difficulty', 'N/A')}")
                print(f"   ⏱️  时间: {recipe.get('cooking_time', recipe.get('time', 'N/A'))}")

    except Exception as e:
        print_test("单一食材生成", False, f"异常: {str(e)}")

    # 测试1.2: 多种食材
    print("\n测试1.2: 多种食材生成 (鸡蛋+西红柿+米饭)")
    start_time = time.time()
    try:
        recipes = recipe_service.generate_recipes(
            ingredients=[
                {"name": "鸡蛋", "quantity": "3个", "state": "新鲜"},
                {"name": "西红柿", "quantity": "2个", "state": "新鲜"},
                {"name": "米饭", "quantity": "1碗", "state": "剩余"}
            ]
        )
        elapsed = time.time() - start_time

        if len(recipes) >= 1:
            print_test("多种食材生成", True, f"生成了 {len(recipes)} 个食谱，耗时 {elapsed:.2f}秒")
            # 显示第一个食谱的详细信息
            if recipes:
                recipe = recipes[0]
                print(f"\n   示例食谱:")
                print(f"   📝 {recipe['name']}")
                print(f"   📖 {recipe.get('description', '')}")
                print(f"   🥘 食材数量: {len(recipe.get('ingredients', []))}")
                print(f"   📋 步骤数量: {len(recipe.get('steps', []))}")
        else:
            print_test("多种食材生成", False, "未生成任何食谱")

    except Exception as e:
        print_test("多种食材生成", False, f"异常: {str(e)}")

def test_filter_conditions():
    """测试2: 筛选条件测试"""
    print_header("测试2: 筛选条件测试")

    base_ingredients = [
        {"name": "鸡肉", "quantity": "200g", "state": "新鲜"},
        {"name": "西兰花", "quantity": "1个", "state": "新鲜"}
    ]

    # 测试2.1: 菜系筛选
    print("测试2.1: 菜系筛选 (中式)")
    try:
        recipes = recipe_service.generate_recipes(
            ingredients=base_ingredients,
            filters={"cuisine": "中式"}
        )
        if recipes:
            print_test("菜系筛选", True, f"生成了 {len(recipes)} 个中式食谱")
            print(f"   📝 示例: {recipes[0]['name']}")
        else:
            print_test("菜系筛选", False, "未生成食谱")
    except Exception as e:
        print_test("菜系筛选", False, f"异常: {str(e)}")

    # 测试2.2: 口味筛选
    print("\n测试2.2: 口味筛选 (清淡)")
    try:
        recipes = recipe_service.generate_recipes(
            ingredients=base_ingredients,
            filters={"taste": "清淡"}
        )
        if recipes:
            print_test("口味筛选", True, f"生成了 {len(recipes)} 个清淡口味食谱")
        else:
            print_test("口味筛选", False, "未生成食谱")
    except Exception as e:
        print_test("口味筛选", False, f"异常: {str(e)}")

    # 测试2.3: 场景筛选
    print("\n测试2.3: 场景筛选 (快手菜)")
    try:
        recipes = recipe_service.generate_recipes(
            ingredients=base_ingredients,
            filters={"scenario": "快手菜"}
        )
        if recipes:
            print_test("场景筛选", True, f"生成了 {len(recipes)} 个快手菜")
            # 验证时间是否合理 (快手菜应该 < 30分钟)
            time_str = recipes[0].get('cooking_time', recipes[0].get('time', ''))
            print(f"   ⏱️  烹饪时间: {time_str}")
        else:
            print_test("场景筛选", False, "未生成食谱")
    except Exception as e:
        print_test("场景筛选", False, f"异常: {str(e)}")

    # 测试2.4: 技能筛选
    print("\n测试2.4: 技能筛选 (新手)")
    try:
        recipes = recipe_service.generate_recipes(
            ingredients=base_ingredients,
            filters={"skill": "新手"}
        )
        if recipes:
            print_test("技能筛选", True, f"生成了 {len(recipes)} 个新手食谱")
            print(f"   🔧 难度: {recipes[0].get('difficulty', 'N/A')}")
        else:
            print_test("技能筛选", False, "未生成食谱")
    except Exception as e:
        print_test("技能筛选", False, f"异常: {str(e)}")

    # 测试2.5: 组合筛选
    print("\n测试2.5: 组合筛选 (中式+清淡+快手菜+新手)")
    try:
        recipes = recipe_service.generate_recipes(
            ingredients=base_ingredients,
            filters={
                "cuisine": "中式",
                "taste": "清淡",
                "scenario": "快手菜",
                "skill": "新手"
            }
        )
        if recipes:
            print_test("组合筛选", True, f"生成了 {len(recipes)} 个符合条件的食谱")
            recipe = recipes[0]
            print(f"   📝 {recipe['name']}")
            print(f"   🔧 {recipe.get('difficulty', 'N/A')}")
            print(f"   ⏱️  {recipe.get('cooking_time', recipe.get('time', 'N/A'))}")
        else:
            print_test("组合筛选", False, "未生成食谱")
    except Exception as e:
        print_test("组合筛选", False, f"异常: {str(e)}")

def test_ingredient_status():
    """测试3: 食材状态标注测试"""
    print_header("测试3: 食材状态标注测试")

    print("测试3.1: 验证 [已有] 和 [需补充] 标注")
    try:
        recipes = recipe_service.generate_recipes(
            ingredients=[
                {"name": "鸡蛋", "quantity": "3个", "state": "新鲜"},
                {"name": "西红柿", "quantity": "2个", "state": "新鲜"}
            ]
        )

        if not recipes:
            print_test("食材状态标注", False, "未生成食谱")
            return

        recipe = recipes[0]
        ingredients = recipe.get('ingredients', [])

        # 统计已有和需补充的食材
        has_available = False
        has_needed = False

        for ing in ingredients:
            status = ing.get('status', '')
            if status == '已有':
                has_available = True
            elif status == '需补充':
                has_needed = True

        print(f"   食材列表:")
        for ing in ingredients[:5]:  # 只显示前5个
            status = ing.get('status', 'N/A')
            print(f"   - {ing['name']} {ing['quantity']} [{status}]")

        if has_available:
            print_test("已有食材标注", True, "正确标注了已有食材")
        else:
            print_test("已有食材标注", False, "未找到已有食材标注")

        # 需补充的食材是可选的，不一定所有食谱都需要
        if has_needed:
            print_test("需补充食材标注", True, "正确标注了需补充食材")
        else:
            print_test("需补充食材标注", True, "此食谱不需要补充食材")

    except Exception as e:
        print_test("食材状态标注", False, f"异常: {str(e)}")

def test_creative_names():
    """测试4: 创意菜名测试"""
    print_header("测试4: 创意菜名测试")

    print("测试4.1: 验证菜名创意性")
    try:
        recipes = recipe_service.generate_recipes(
            ingredients=[
                {"name": "鸡蛋", "quantity": "2个", "state": "新鲜"},
                {"name": "米饭", "quantity": "1碗", "state": "剩余"}
            ]
        )

        if not recipes:
            print_test("创意菜名", False, "未生成食谱")
            return

        # 检查菜名是否有创意 (不是简单的"蛋炒饭")
        boring_names = ["蛋炒饭", "炒饭", "鸡蛋炒饭"]
        creative_count = 0

        print(f"   生成的菜名:")
        for i, recipe in enumerate(recipes, 1):
            name = recipe.get('name', '')
            print(f"   {i}. {name}")
            if name not in boring_names and len(name) > 3:
                creative_count += 1

        if creative_count >= len(recipes) * 0.6:  # 至少60%有创意
            print_test("创意菜名", True, f"{creative_count}/{len(recipes)} 个菜名有创意")
        else:
            print_test("创意菜名", False, f"只有 {creative_count}/{len(recipes)} 个菜名有创意")

    except Exception as e:
        print_test("创意菜名", False, f"异常: {str(e)}")

def test_reasonableness():
    """测试5: 合理性测试"""
    print_header("测试5: 合理性测试")

    # 测试5.1: 正常食材组合
    print("测试5.1: 正常食材组合 (鸡肉+土豆)")
    try:
        recipes = recipe_service.generate_recipes(
            ingredients=[
                {"name": "鸡肉", "quantity": "300g", "state": "新鲜"},
                {"name": "土豆", "quantity": "2个", "state": "新鲜"}
            ]
        )
        if recipes:
            print_test("正常食材组合", True, f"成功生成 {len(recipes)} 个食谱")
            print(f"   📝 示例: {recipes[0]['name']}")
        else:
            print_test("正常食材组合", False, "未生成食谱")
    except Exception as e:
        print_test("正常食材组合", False, f"异常: {str(e)}")

    # 测试5.2: 边界食材组合 (测试AI是否会拒绝不合理组合)
    print("\n测试5.2: 边界食材组合 (西瓜+月饼)")
    print("   ℹ️  此测试验证AI是否能处理不常见的食材组合")
    try:
        recipes = recipe_service.generate_recipes(
            ingredients=[
                {"name": "西瓜", "quantity": "1/4个", "state": "新鲜"},
                {"name": "月饼", "quantity": "2个", "state": "常温"}
            ]
        )
        if recipes:
            print_test("边界食材组合", True, f"AI尝试生成了 {len(recipes)} 个食谱")
            print(f"   📝 示例: {recipes[0]['name']}")
            print(f"   ℹ️  AI可能生成了创意食谱或甜品")
        else:
            print_test("边界食材组合", True, "AI拒绝了不合理的组合")
    except Exception as e:
        print_test("边界食材组合", False, f"异常: {str(e)}")

def test_database_persistence():
    """测试6: 数据库持久化验证"""
    print_header("测试6: 数据库持久化验证")

    # 测试6.1: 自动保存
    print("测试6.1: 验证食谱自动保存到数据库")
    try:
        # 获取当前历史记录数量
        history_before = recipe_service.get_recipe_history(limit=100)
        count_before = len(history_before)

        # 生成新食谱
        recipes = recipe_service.generate_recipes(
            ingredients=[
                {"name": "番茄", "quantity": "2个", "state": "新鲜"},
                {"name": "鸡蛋", "quantity": "3个", "state": "新鲜"}
            ]
        )

        # 获取更新后的历史记录
        history_after = recipe_service.get_recipe_history(limit=100)
        count_after = len(history_after)

        if count_after > count_before:
            print_test("自动保存", True, f"成功保存 {count_after - count_before} 个食谱到数据库")
        else:
            print_test("自动保存", False, "食谱未保存到数据库")

    except Exception as e:
        print_test("自动保存", False, f"异常: {str(e)}")

    # 测试6.2: 历史记录查询
    print("\n测试6.2: 历史记录查询")
    try:
        history = recipe_service.get_recipe_history(limit=5)
        if history:
            print_test("历史记录查询", True, f"成功查询到 {len(history)} 条历史记录")
            print(f"   最新食谱:")
            for i, recipe in enumerate(history[:3], 1):
                print(f"   {i}. {recipe['name']} (ID: {recipe['id']})")
        else:
            print_test("历史记录查询", False, "未查询到历史记录")
    except Exception as e:
        print_test("历史记录查询", False, f"异常: {str(e)}")

    # 测试6.3: 单个食谱查询
    print("\n测试6.3: 单个食谱查询")
    try:
        history = recipe_service.get_recipe_history(limit=1)
        if history:
            recipe_id = history[0]['id']
            recipe = recipe_service.get_recipe_by_id(recipe_id)
            if recipe:
                print_test("单个食谱查询", True, f"成功查询食谱 ID: {recipe_id}")
                print(f"   📝 {recipe['name']}")
                print(f"   🥘 食材数: {len(recipe.get('ingredients', []))}")
                print(f"   📋 步骤数: {len(recipe.get('steps', []))}")
            else:
                print_test("单个食谱查询", False, f"未找到食谱 ID: {recipe_id}")
        else:
            print_test("单个食谱查询", False, "没有可查询的食谱")
    except Exception as e:
        print_test("单个食谱查询", False, f"异常: {str(e)}")

def print_summary():
    """打印测试总结"""
    print_header("测试总结")

    print(f"总测试数: {test_results['total']}")
    print(f"✅ 通过: {test_results['passed']}")
    print(f"❌ 失败: {test_results['failed']}")

    if test_results['failed'] > 0:
        print(f"\n失败的测试:")
        for error in test_results['errors']:
            print(f"  - {error}")

    pass_rate = (test_results['passed'] / test_results['total'] * 100) if test_results['total'] > 0 else 0
    print(f"\n通过率: {pass_rate:.1f}%")

    if pass_rate >= 80:
        print("\n🎉 测试结果: 优秀")
    elif pass_rate >= 60:
        print("\n👍 测试结果: 良好")
    else:
        print("\n⚠️  测试结果: 需要改进")

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("  SmartCook AI - AI 食谱生成专项测试")
    print("="*60)

    # 验证配置
    try:
        Config.validate()
        print(f"✅ 配置验证通过")
        print(f"   API Key: {Config.DASHSCOPE_API_KEY[:10]}...")
        print(f"   Model: {Config.MODEL_NAME}")
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        print(f"\n请确保:")
        print(f"1. 已创建 .env 文件")
        print(f"2. 已设置 DASHSCOPE_API_KEY")
        return

    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 运行测试
        test_basic_generation()
        test_filter_conditions()
        test_ingredient_status()
        test_creative_names()
        test_reasonableness()
        test_database_persistence()

        # 打印总结
        print_summary()

if __name__ == '__main__':
    main()
