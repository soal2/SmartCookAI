"""
Recipe Chain Routes
链式食谱生成 API 端点
"""
from flask import Blueprint, request, jsonify
from app.services.recipe_service import recipe_service
from app import limiter

bp = Blueprint('recipe_chain', __name__, url_prefix='/api/chain')


def _validate_request(data):
    if not isinstance(data, dict):
        return False, '请求体格式错误'

    user_input = data.get('user_input', '')
    if not isinstance(user_input, str) or not user_input.strip():
        return False, 'user_input 不能为空'

    return True, None


@bp.route('/process', methods=['POST'])
@limiter.limit("10 per hour")
def process_chain():
    """
    处理链式流程
    POST /api/chain/process
    Body: {"user_input": "..."}
    """
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type 必须是 application/json'}), 400

        data = request.get_json()
        valid, error_msg = _validate_request(data)
        if not valid:
            return jsonify({'error': error_msg}), 400

        result = recipe_service.process_chain(data['user_input'].strip())

        return jsonify({
            'success': True,
            'analysis': result.get('analysis', {}),
            'recipes': result.get('recipes', []),
            'substitutions': result.get('substitutions', {}),
            'missing_ingredients': result.get('missing_ingredients', []),
            'substitution_candidates': result.get('substitution_candidates', {})
        })
    except Exception as e:
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500
