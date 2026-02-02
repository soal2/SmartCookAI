"""
Recipe Routes
食谱相关 API 端点
"""
from flask import Blueprint, request, jsonify
from app.services.recipe_service import recipe_service
from app.models.recipe_progress import RecipeStepProgress
from app.database import db
from datetime import datetime
from config import Config
from app import limiter

bp = Blueprint('recipes', __name__, url_prefix='/api/recipes')


def validate_ingredient(ingredient):
    """验证单个食材数据"""
    if not isinstance(ingredient, dict):
        return False, "食材格式错误"

    if 'name' not in ingredient or not ingredient['name'].strip():
        return False, "食材名称不能为空"

    if 'quantity' not in ingredient:
        return False, "食材数量不能为空"

    # 验证状态
    if 'state' in ingredient and ingredient['state'] not in Config.ALLOWED_STATES:
        return False, f"无效的食材状态: {ingredient['state']}"

    return True, None


def validate_filters(filters):
    """验证筛选条件"""
    if not isinstance(filters, dict):
        return False, "筛选条件格式错误"

    # 验证菜系
    if 'cuisine' in filters and filters['cuisine'] not in Config.ALLOWED_CUISINES:
        return False, f"无效的菜系: {filters['cuisine']}"

    # 验证口味
    if 'taste' in filters and filters['taste'] not in Config.ALLOWED_TASTES:
        return False, f"无效的口味: {filters['taste']}"

    # 验证场景
    if 'scenario' in filters and filters['scenario'] not in Config.ALLOWED_SCENARIOS:
        return False, f"无效的场景: {filters['scenario']}"

    # 验证技能
    if 'skill' in filters and filters['skill'] not in Config.ALLOWED_SKILLS:
        return False, f"无效的技能水平: {filters['skill']}"

    return True, None


@bp.route('/generate', methods=['POST'])
@limiter.limit("10 per hour")
def generate_recipes():
    """
    生成食谱
    POST /api/recipes/generate
    Body: {
        "ingredients": [{"name": "鸡蛋", "quantity": "6个", "state": "新鲜"}],
        "filters": {"cuisine": "中式", "taste": "清淡", "scenario": "快手菜", "skill": "新手"}
    }
    """
    try:
        # 验证请求格式
        if not request.is_json:
            return jsonify({'error': 'Content-Type 必须是 application/json'}), 400

        data = request.get_json()
        ingredients = data.get('ingredients', [])
        filters = data.get('filters', {})

        # 验证食材列表
        if not ingredients:
            return jsonify({'error': '请提供至少一种食材'}), 400

        if not isinstance(ingredients, list):
            return jsonify({'error': '食材必须是列表格式'}), 400

        if len(ingredients) > Config.MAX_INGREDIENTS:
            return jsonify({'error': f'食材数量不能超过 {Config.MAX_INGREDIENTS} 种'}), 400

        # 验证每个食材
        for i, ingredient in enumerate(ingredients):
            valid, error_msg = validate_ingredient(ingredient)
            if not valid:
                return jsonify({'error': f'食材 {i+1}: {error_msg}'}), 400

        # 验证筛选条件
        if filters:
            valid, error_msg = validate_filters(filters)
            if not valid:
                return jsonify({'error': error_msg}), 400

        # 调用 AI 服务生成食谱（会自动保存到历史）
        recipes = recipe_service.generate_recipes(ingredients, filters)

        return jsonify({
            'success': True,
            'recipes': recipes,
            'count': len(recipes)
        })

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': '服务器内部错误，请稍后重试'}), 500


@bp.route('/history', methods=['GET'])
def get_history():
    """
    获取历史生成记录
    GET /api/recipes/history?limit=20
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        history = recipe_service.get_recipe_history(limit)

        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """
    获取单个食谱详情
    GET /api/recipes/<id>
    """
    try:
        recipe = recipe_service.get_recipe_by_id(recipe_id)
        if not recipe:
            return jsonify({'error': '食谱不存在'}), 404

        return jsonify({
            'success': True,
            'recipe': recipe
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """
    删除历史记录
    DELETE /api/recipes/<id>
    """
    try:
        success = recipe_service.delete_recipe(recipe_id)
        if not success:
            return jsonify({'error': '食谱不存在'}), 404

        return jsonify({
            'success': True,
            'message': '删除成功'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:recipe_id>/progress', methods=['GET'])
def get_progress(recipe_id):
    """
    获取步骤完成状态
    GET /api/recipes/<id>/progress
    """
    try:
        progress = RecipeStepProgress.query.filter_by(recipe_id=recipe_id).all()
        return jsonify({
            'success': True,
            'progress': [p.to_dict() for p in progress]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:recipe_id>/progress', methods=['POST'])
def update_progress(recipe_id):
    """
    更新步骤完成状态
    POST /api/recipes/<id>/progress
    Body: {"step_index": 0, "is_completed": true}
    """
    try:
        data = request.get_json()
        step_index = data.get('step_index')
        is_completed = data.get('is_completed', False)

        if step_index is None:
            return jsonify({'error': '请提供 step_index'}), 400

        # 查找或创建进度记录
        progress = RecipeStepProgress.query.filter_by(
            recipe_id=recipe_id,
            step_index=step_index
        ).first()

        if not progress:
            progress = RecipeStepProgress(
                recipe_id=recipe_id,
                step_index=step_index
            )
            db.session.add(progress)

        progress.is_completed = is_completed
        if is_completed:
            progress.completed_at = datetime.utcnow()
        else:
            progress.completed_at = None

        db.session.commit()

        return jsonify({
            'success': True,
            'progress': progress.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
