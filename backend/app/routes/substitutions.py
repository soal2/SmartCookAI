"""
Substitution Routes
食材替代 API 端点
"""
from flask import Blueprint, request, jsonify
from app.services.substitution_service import substitution_service
from app.services.recipe_service import recipe_service
import json

bp = Blueprint('substitutions', __name__, url_prefix='/api/substitutions')


@bp.route('/<ingredient_name>', methods=['GET'])
def get_substitutes(ingredient_name):
    """
    获取某食材的替代建议
    GET /api/substitutions/<ingredient_name>?limit=5
    """
    try:
        limit = request.args.get('limit', 5, type=int)
        substitutes = substitution_service.get_substitutes(ingredient_name, limit)

        return jsonify({
            'success': True,
            'ingredient': ingredient_name,
            'substitutes': substitutes,
            'count': len(substitutes)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe_substitutions(recipe_id):
    """
    获取菜谱中所有缺失食材的替代建议
    GET /api/substitutions/recipe/<recipe_id>
    """
    try:
        # 获取菜谱详情
        recipe = recipe_service.get_recipe_by_id(recipe_id)
        if not recipe:
            return jsonify({'error': '菜谱不存在'}), 404

        # 解析食材列表
        ingredients = json.loads(recipe.get('ingredients_json', '[]'))

        # 获取替代建议
        substitutions = substitution_service.get_recipe_substitutions(ingredients)

        return jsonify({
            'success': True,
            'recipe_id': recipe_id,
            'recipe_name': recipe.get('name'),
            'substitutions': substitutions,
            'count': len(substitutions)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/', methods=['GET'])
def get_all_substitutions():
    """
    获取所有替代关系
    GET /api/substitutions
    """
    try:
        substitutions = substitution_service.get_all_substitutions()
        return jsonify({
            'success': True,
            'substitutions': substitutions,
            'count': len(substitutions)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/', methods=['POST'])
def add_substitution():
    """
    添加食材替代关系
    POST /api/substitutions
    Body: {
        "original_ingredient": "柠檬汁",
        "substitute_ingredient": "白醋",
        "similarity_score": 0.85,
        "substitution_ratio": "1:1",
        "notes": "酸味替代，适合凉拌菜",
        "category": "调料"
    }
    """
    try:
        data = request.get_json()

        if not data.get('original_ingredient') or not data.get('substitute_ingredient'):
            return jsonify({'error': '原食材和替代食材不能为空'}), 400

        substitution = substitution_service.add_substitution(data)
        if not substitution:
            return jsonify({'error': '添加替代关系失败'}), 500

        return jsonify({
            'success': True,
            'substitution': substitution
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:substitution_id>', methods=['DELETE'])
def delete_substitution(substitution_id):
    """
    删除替代关系
    DELETE /api/substitutions/<id>
    """
    try:
        success = substitution_service.delete_substitution(substitution_id)
        if not success:
            return jsonify({'error': '替代关系不存在'}), 404

        return jsonify({
            'success': True,
            'message': '删除成功'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
