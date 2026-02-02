"""
Ingredients Routes
食材管理 API 端点
"""
from flask import Blueprint, request, jsonify
from app.services.ingredient_service import ingredient_service
from config import Config

bp = Blueprint('ingredients', __name__, url_prefix='/api/ingredients')


@bp.route('/', methods=['GET'])
def get_ingredients():
    """
    获取所有食材
    GET /api/ingredients
    """
    try:
        ingredients = ingredient_service.get_all_ingredients()
        return jsonify({
            'success': True,
            'ingredients': ingredients,
            'count': len(ingredients)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/common', methods=['GET'])
def get_common_ingredients():
    """
    获取常用食材
    GET /api/ingredients/common
    """
    try:
        ingredients = ingredient_service.get_common_ingredients()
        return jsonify({
            'success': True,
            'ingredients': ingredients,
            'count': len(ingredients)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/by-category', methods=['GET'])
def get_by_category():
    """
    按分类获取食材
    GET /api/ingredients/by-category?category=蔬菜
    """
    try:
        category = request.args.get('category')
        if not category:
            return jsonify({'error': '请提供分类参数'}), 400

        # 验证分类
        if category not in Config.ALLOWED_CATEGORIES:
            return jsonify({'error': f'无效的分类: {category}，允许的分类: {", ".join(Config.ALLOWED_CATEGORIES)}'}), 400

        ingredients = ingredient_service.get_ingredients_by_category(category)
        return jsonify({
            'success': True,
            'ingredients': ingredients,
            'count': len(ingredients)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/by-storage', methods=['GET'])
def get_by_storage():
    """
    按存储位置获取食材
    GET /api/ingredients/by-storage?storage=fridge
    """
    try:
        storage = request.args.get('storage')
        if not storage:
            return jsonify({'error': '请提供存储位置参数'}), 400

        # 验证存储位置
        if storage not in Config.ALLOWED_STORAGE:
            return jsonify({'error': f'无效的存储位置: {storage}，允许的位置: {", ".join(Config.ALLOWED_STORAGE)}'}), 400

        ingredients = ingredient_service.get_ingredients_by_storage(storage)
        return jsonify({
            'success': True,
            'ingredients': ingredients,
            'count': len(ingredients)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/', methods=['POST'])
def add_ingredient():
    """
    添加食材
    POST /api/ingredients
    Body: {"name": "鸡蛋", "quantity": "6个", "state": "新鲜", "category": "主食", "storage_location": "fridge"}
    """
    try:
        data = request.get_json()
        if not data.get('name'):
            return jsonify({'error': '食材名称不能为空'}), 400

        # 验证分类
        if 'category' in data and data['category'] not in Config.ALLOWED_CATEGORIES:
            return jsonify({'error': f'无效的分类: {data["category"]}'}), 400

        # 验证存储位置
        if 'storage_location' in data and data['storage_location'] not in Config.ALLOWED_STORAGE:
            return jsonify({'error': f'无效的存储位置: {data["storage_location"]}'}), 400

        ingredient = ingredient_service.add_ingredient(data)
        if not ingredient:
            return jsonify({'error': '添加食材失败'}), 500

        return jsonify({
            'success': True,
            'ingredient': ingredient
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    """
    更新食材
    PUT /api/ingredients/:id
    Body: {"quantity": "8个", "state": "新鲜"}
    """
    try:
        data = request.get_json()
        ingredient = ingredient_service.update_ingredient(ingredient_id, data)

        if not ingredient:
            return jsonify({'error': '食材不存在'}), 404

        return jsonify({
            'success': True,
            'ingredient': ingredient
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    """
    删除食材
    DELETE /api/ingredients/:id
    """
    try:
        success = ingredient_service.delete_ingredient(ingredient_id)
        if not success:
            return jsonify({'error': '食材不存在'}), 404

        return jsonify({
            'success': True,
            'message': '食材已删除'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:ingredient_id>/mark-common', methods=['POST'])
def mark_as_common(ingredient_id):
    """
    标记为常用食材
    POST /api/ingredients/:id/mark-common
    """
    try:
        ingredient = ingredient_service.mark_as_common(ingredient_id)
        if not ingredient:
            return jsonify({'error': '食材不存在'}), 404

        return jsonify({
            'success': True,
            'ingredient': ingredient
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
