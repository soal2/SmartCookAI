"""
Favorites Routes
收藏夹 API 端点
"""
from flask import Blueprint, request, jsonify
from app.services.favorite_service import favorite_service

bp = Blueprint('favorites', __name__, url_prefix='/api/favorites')


@bp.route('/', methods=['GET'])
def get_favorites():
    """
    获取所有收藏
    GET /api/favorites
    """
    try:
        favorites = favorite_service.get_all_favorites()
        return jsonify({
            'success': True,
            'favorites': favorites,
            'count': len(favorites)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/groups', methods=['GET'])
def get_groups():
    """
    获取所有分组
    GET /api/favorites/groups
    """
    try:
        groups = favorite_service.get_all_groups()
        return jsonify({
            'success': True,
            'groups': groups,
            'count': len(groups)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/groups', methods=['POST'])
def create_group():
    """
    创建分组
    POST /api/favorites/groups
    Body: {"name": "减脂餐", "description": "健康低卡"}
    """
    try:
        data = request.get_json()
        if not data.get('name'):
            return jsonify({'error': '分组名称不能为空'}), 400

        group = favorite_service.create_group(data)
        if not group:
            return jsonify({'error': '创建分组失败'}), 500

        return jsonify({
            'success': True,
            'group': group
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/groups/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    """
    更新分组
    PUT /api/favorites/groups/:id
    Body: {"name": "新名称", "description": "新描述"}
    """
    try:
        data = request.get_json()
        group = favorite_service.update_group(group_id, data)

        if not group:
            return jsonify({'error': '分组不存在'}), 404

        return jsonify({
            'success': True,
            'group': group
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """
    删除分组
    DELETE /api/favorites/groups/:id
    """
    try:
        success = favorite_service.delete_group(group_id)
        if not success:
            return jsonify({'error': '分组不存在'}), 404

        return jsonify({
            'success': True,
            'message': '分组已删除'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/by-group/<int:group_id>', methods=['GET'])
def get_by_group(group_id):
    """
    按分组获取收藏
    GET /api/favorites/by-group/:id
    """
    try:
        favorites = favorite_service.get_favorites_by_group(group_id)
        return jsonify({
            'success': True,
            'favorites': favorites,
            'count': len(favorites)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/', methods=['POST'])
def add_favorite():
    """
    添加收藏
    POST /api/favorites
    Body: {"recipe_id": 1, "group_id": 1, "notes": "很好吃"}
    """
    try:
        data = request.get_json()
        if not data.get('recipe_id'):
            return jsonify({'error': '食谱ID不能为空'}), 400

        favorite = favorite_service.add_to_favorites(data)
        if not favorite:
            return jsonify({'error': '添加收藏失败'}), 500

        return jsonify({
            'success': True,
            'favorite': favorite
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    """
    移除收藏
    DELETE /api/favorites/:id
    """
    try:
        success = favorite_service.remove_from_favorites(favorite_id)
        if not success:
            return jsonify({'error': '收藏不存在'}), 404

        return jsonify({
            'success': True,
            'message': '已取消收藏'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
