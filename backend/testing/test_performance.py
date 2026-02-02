#!/usr/bin/env python3
"""
Performance Testing Script
性能测试脚本

测试指标:
1. 响应时间测试 (首字生成 < 3秒, 完整生成 < 15秒)
2. 不同食材数量的响应时间
3. 不同筛选条件的响应时间
"""
import sys
import os
import time
from typing import List, Dict, Any

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

def test_response_time():
    """测试1: 响应时间测试"""
    print_header("测试1: 响应时间测试")

    # 测试1.1: 基础响应时间
    print("测试1.1: 基础响应时间 (3个食材)")
    ingredients = [
        {"name": "鸡蛋", "quantity": "3个", "state": "新鲜"},
        {"name": "西红柿", "quantity": "2个", "state": "新鲜"},
        {"name": "米饭", "quantity": "1碗", "state": "剩余"}
    ]

    try:
        start_time = time.time()
        recipes = recipe_service.generate_recipes(ingredients=ingredients)
        total_time = time.time() - start_time

        print(f"⏱️  完整生成时间: {total_time:.2f}秒")

        if total_time < 15:
            print(f"✅ 性能达标 (< 15秒)")
        else:
            print(f"⚠️  性能未达标 (> 15秒)")

        if recipes:
            print(f"📊 生成食谱数: {len(recipes)}")
            print(f"📊 平均每个食谱: {total_time/len(recipes):.2f}秒")

    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_ingredient_count_performance():
    """测试2: 不同食材数量的性能"""
    print_header("测试2: 不同食材数量的性能")

    test_cases = [
        {
            "name": "1个食材",
            "ingredients": [
                {"name": "鸡蛋", "quantity": "6个", "state": "新鲜"}
            ]
        },
        {
            "name": "3个食材",
            "ingredients": [
                {"name": "鸡蛋", "quantity": "3个", "state": "新鲜"},
                {"name": "西红柿", "quantity": "2个", "state": "新鲜"},
                {"name": "米饭", "quantity": "1碗", "state": "剩余"}
            ]
        },
        {
            "name": "5个食材",
            "ingredients": [
                {"name": "鸡肉", "quantity": "300g", "state": "新鲜"},
                {"name": "土豆", "quantity": "2个", "state": "新鲜"},
                {"name": "胡萝卜", "quantity": "1根", "state": "新鲜"},
                {"name": "洋葱", "quantity": "半个", "state": "新鲜"},
                {"name": "酱油", "quantity": "适量", "state": "常温"}
            ]
        }
    ]

    results = []
    for test_case in test_cases:
        print(f"\n测试: {test_case['name']}")
        try:
            start_time = time.time()
            recipes = recipe_service.generate_recipes(
                ingredients=test_case['ingredients']
            )
            elapsed = time.time() - start_time

            results.append({
                "name": test_case['name'],
                "time": elapsed,
                "count": len(recipes) if recipes else 0
            })

            print(f"⏱️  耗时: {elapsed:.2f}秒")
            print(f"📊 生成: {len(recipes) if recipes else 0} 个食谱")

        except Exception as e:
            print(f"❌ 失败: {e}")
            results.append({
                "name": test_case['name'],
                "time": 0,
                "count": 0
            })

    # 打印汇总
    print(f"\n{'='*60}")
    print("性能汇总:")
    print(f"{'食材数量':<15} {'耗时':<15} {'生成数量':<15}")
    print(f"{'-'*60}")
    for result in results:
        print(f"{result['name']:<15} {result['time']:.2f}秒{'':<10} {result['count']:<15}")

def test_filter_performance():
    """测试3: 筛选条件对性能的影响"""
    print_header("测试3: 筛选条件对性能的影响")

    base_ingredients = [
        {"name": "鸡肉", "quantity": "200g", "state": "新鲜"},
        {"name": "西兰花", "quantity": "1个", "state": "新鲜"}
    ]

    test_cases = [
        {"name": "无筛选", "filters": None},
        {"name": "单一筛选", "filters": {"cuisine": "中式"}},
        {"name": "组合筛选", "filters": {
            "cuisine": "中式",
            "taste": "清淡",
            "scenario": "快手菜",
            "skill": "新手"
        }}
    ]

    results = []
    for test_case in test_cases:
        print(f"\n测试: {test_case['name']}")
        try:
            start_time = time.time()
            recipes = recipe_service.generate_recipes(
                ingredients=base_ingredients,
                filters=test_case['filters']
            )
            elapsed = time.time() - start_time

            results.append({
                "name": test_case['name'],
                "time": elapsed
            })

            print(f"⏱️  耗时: {elapsed:.2f}秒")

        except Exception as e:
            print(f"❌ 失败: {e}")
            results.append({
                "name": test_case['name'],
                "time": 0
            })

    # 打印汇总
    print(f"\n{'='*60}")
    print("筛选条件性能汇总:")
    print(f"{'筛选类型':<20} {'耗时':<15}")
    print(f"{'-'*60}")
    for result in results:
        print(f"{result['name']:<20} {result['time']:.2f}秒")

def test_concurrent_requests():
    """测试4: 并发请求测试 (简单版)"""
    print_header("测试4: 并发请求测试")

    print("ℹ️  此测试模拟连续多次请求")
    print("ℹ️  完整的并发测试建议使用 locust 或 ab 工具\n")

    ingredients = [
        {"name": "鸡蛋", "quantity": "3个", "state": "新鲜"},
        {"name": "西红柿", "quantity": "2个", "state": "新鲜"}
    ]

    num_requests = 3
    times = []

    print(f"执行 {num_requests} 次连续请求...")
    for i in range(num_requests):
        try:
            start_time = time.time()
            recipes = recipe_service.generate_recipes(ingredients=ingredients)
            elapsed = time.time() - start_time
            times.append(elapsed)
            print(f"  请求 {i+1}: {elapsed:.2f}秒")
        except Exception as e:
            print(f"  请求 {i+1}: 失败 - {e}")

    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"\n统计:")
        print(f"  平均响应时间: {avg_time:.2f}秒")
        print(f"  最快响应时间: {min_time:.2f}秒")
        print(f"  最慢响应时间: {max_time:.2f}秒")

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("  SmartCook AI - 性能测试")
    print("="*60)

    # 验证配置
    try:
        Config.validate()
        print(f"✅ 配置验证通过")
        print(f"   Model: {Config.MODEL_NAME}")
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        return

    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 运行测试
        test_response_time()
        test_ingredient_count_performance()
        test_filter_performance()
        test_concurrent_requests()

        print_header("性能测试完成")
        print("✅ 所有性能测试已完成")
        print("\n建议:")
        print("1. 如需完整的并发测试，使用 locust 或 ab 工具")
        print("2. 监控 API 调用的实际响应时间")
        print("3. 注意 Dashscope API 的调用限制")

if __name__ == '__main__':
    main()
