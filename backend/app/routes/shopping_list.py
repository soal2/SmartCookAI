"""
Shopping List Routes
购物清单 API 端点
"""
from flask import Blueprint, request, jsonify
from app.services.shopping_list_service import shopping_list_service

bp = Blueprint('shopping_list', __name__, url_prefix='/api/shopping-list')


@bp.route('/', methods=['GET'])
def get_shopping_list():
    """
    获取购物清单
    GET /api/shopping-list
    """
    try:
        items = shopping_list_service.get_shopping_list()
        return jsonify({
            'success': True,
            'items': items,
            'count': len(items)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/', methods=['POST'])
def add_item():
    """
    添加购物项
    POST /api/shopping-list
    Body: {"ingredient_name": "鸡蛋", "quantity": "6个", "category": "主食"}
    """
    try:
        data = request.get_json()
        if not data.get('ingredient_name'):
            return jsonify({'error': '食材名称不能为空'}), 400

        item = shopping_list_service.add_item(data)
        if not item:
            return jsonify({'error': '添加购物项失败'}), 500

        return jsonify({
            'success': True,
            'item': item
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """
    更新购物项
    PUT /api/shopping-list/:id
    Body: {"quantity": "8个", "is_purchased": true}
    """
    try:
        data = request.get_json()
        item = shopping_list_service.update_item(item_id, data)

        if not item:
            return jsonify({'error': '购物项不存在'}), 404

        return jsonify({
            'success': True,
            'item': item
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    删除购物项
    DELETE /api/shopping-list/:id
    """
    try:
        success = shopping_list_service.delete_item(item_id)
        if not success:
            return jsonify({'error': '购物项不存在'}), 404

        return jsonify({
            'success': True,
            'message': '购物项已删除'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:item_id>/purchase', methods=['POST'])
def mark_purchased(item_id):
    """
    标记为已购买
    POST /api/shopping-list/:id/purchase
    """
    try:
        item = shopping_list_service.mark_as_purchased(item_id)
        if not item:
            return jsonify({'error': '购物项不存在'}), 404

        return jsonify({
            'success': True,
            'item': item
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/generate', methods=['POST'])
def generate_from_recipe():
    """
    从菜谱生成购物清单
    POST /api/shopping-list/generate
    Body: {"recipe_id": 1}
    """
    try:
        data = request.get_json()
        recipe_id = data.get('recipe_id')

        if not recipe_id:
            return jsonify({'error': '请提供食谱ID'}), 400

        items = shopping_list_service.generate_from_recipe(recipe_id)

        return jsonify({
            'success': True,
            'items': items,
            'count': len(items)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/purchased', methods=['DELETE'])
def clear_purchased():
    """
    清除已购买项目
    DELETE /api/shopping-list/purchased
    """
    try:
        success = shopping_list_service.clear_purchased()
        if not success:
            return jsonify({'error': '清除失败'}), 500

        return jsonify({
            'success': True,
            'message': '已购买项目已清除'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
