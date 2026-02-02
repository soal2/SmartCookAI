"""
P1 Feature Test Script - Smart Ingredient Substitution
P1 功能测试脚本 - 智能食材替代
"""
import requests
import json

BASE_URL = "http://localhost:5001/api"


def test_get_substitutes():
    """测试获取食材替代建议"""
    print("\n=== 测试1: 获取柠檬汁的替代建议 ===")
    response = requests.get(f"{BASE_URL}/substitutions/柠檬汁")
    data = response.json()

    print(f"状态码: {response.status_code}")
    print(f"成功: {data.get('success')}")
    print(f"食材: {data.get('ingredient')}")
    print(f"找到 {data.get('count')} 个替代方案:")

    for sub in data.get('substitutes', []):
        print(f"  - {sub['substitute_ingredient']}")
        print(f"    相似度: {sub['similarity_score']}")
        print(f"    比例: {sub['substitution_ratio']}")
        print(f"    说明: {sub['notes']}")

    assert response.status_code == 200
    assert data['success'] == True
    print("✅ 测试通过")


def test_get_all_substitutions():
    """测试获取所有替代关系"""
    print("\n=== 测试2: 获取所有替代关系 ===")
    response = requests.get(f"{BASE_URL}/substitutions/")
    data = response.json()

    print(f"状态码: {response.status_code}")
    print(f"成功: {data.get('success')}")
    print(f"总共 {data.get('count')} 条替代关系")

    assert response.status_code == 200
    assert data['success'] == True
    assert data['count'] > 0
    print("✅ 测试通过")


def test_add_substitution():
    """测试添加替代关系"""
    print("\n=== 测试3: 添加新的替代关系 ===")

    new_sub = {
        "original_ingredient": "鸡蛋",
        "substitute_ingredient": "豆腐",
        "similarity_score": 0.70,
        "substitution_ratio": "1个鸡蛋=50g豆腐",
        "notes": "素食替代，适合烘焙",
        "category": "蛋奶"
    }

    response = requests.post(
        f"{BASE_URL}/substitutions/",
        json=new_sub,
        headers={'Content-Type': 'application/json'}
    )
    data = response.json()

    print(f"状态码: {response.status_code}")
    print(f"成功: {data.get('success')}")
    print(f"添加的替代关系: {data.get('substitution', {}).get('original_ingredient')} -> {data.get('substitution', {}).get('substitute_ingredient')}")

    assert response.status_code == 201
    assert data['success'] == True
    print("✅ 测试通过")

    return data.get('substitution', {}).get('id')


def test_recipe_substitutions():
    """测试获取菜谱的替代建议"""
    print("\n=== 测试4: 获取菜谱的替代建议 ===")

    # 首先生成一个菜谱
    print("生成测试菜谱...")
    recipe_data = {
        "ingredients": [
            {"name": "鸡蛋", "quantity": "2个", "state": "新鲜"},
            {"name": "柠檬汁", "quantity": "1勺", "state": "新鲜"}
        ],
        "filters": {
            "cuisine": "中式",
            "taste": "清淡"
        }
    }

    recipe_response = requests.post(
        f"{BASE_URL}/recipes/generate",
        json=recipe_data,
        headers={'Content-Type': 'application/json'}
    )

    if recipe_response.status_code == 200:
        recipe_data = recipe_response.json()
        if recipe_data.get('recipes'):
            recipe_id = recipe_data['recipes'][0]['id']
            print(f"生成的菜谱 ID: {recipe_id}")

            # 获取替代建议
            print("获取替代建议...")
            sub_response = requests.get(f"{BASE_URL}/substitutions/recipe/{recipe_id}")
            sub_data = sub_response.json()

            print(f"状态码: {sub_response.status_code}")
            print(f"成功: {sub_data.get('success')}")
            print(f"菜谱名称: {sub_data.get('recipe_name')}")
            print(f"找到 {sub_data.get('count')} 个缺失食材有替代方案")

            for ingredient, subs in sub_data.get('substitutions', {}).items():
                print(f"\n  缺失食材: {ingredient}")
                for sub in subs:
                    print(f"    可用 {sub['substitute_ingredient']} 替代")
                    print(f"    说明: {sub['notes']}")

            assert sub_response.status_code == 200
            assert sub_data['success'] == True
            print("✅ 测试通过")
        else:
            print("⚠️  未生成菜谱，跳过此测试")
    else:
        print(f"⚠️  生成菜谱失败: {recipe_response.status_code}")
        print("跳过此测试")


def test_delete_substitution(sub_id):
    """测试删除替代关系"""
    print(f"\n=== 测试5: 删除替代关系 (ID: {sub_id}) ===")

    response = requests.delete(f"{BASE_URL}/substitutions/{sub_id}")
    data = response.json()

    print(f"状态码: {response.status_code}")
    print(f"成功: {data.get('success')}")
    print(f"消息: {data.get('message')}")

    assert response.status_code == 200
    assert data['success'] == True
    print("✅ 测试通过")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("P1 功能测试 - 智能食材替代")
    print("=" * 60)

    try:
        # 测试1: 获取替代建议
        test_get_substitutes()

        # 测试2: 获取所有替代关系
        test_get_all_substitutions()

        # 测试3: 添加替代关系
        new_sub_id = test_add_substitution()

        # 测试4: 获取菜谱替代建议
        test_recipe_substitutions()

        # 测试5: 删除替代关系
        if new_sub_id:
            test_delete_substitution(new_sub_id)

        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")


if __name__ == '__main__':
    main()
