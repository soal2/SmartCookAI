#!/usr/bin/env python3
"""
Chain Service Test
链式食谱服务基础测试
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.services.recipe_service import recipe_service


def main():
    app = create_app()
    with app.app_context():
        result = recipe_service.process_chain('我想做一道清淡的鸡肉料理，家里只有鸡胸肉和西兰花')

        assert 'analysis' in result
        assert 'recipes' in result
        assert 'substitutions' in result

        print('✅ 链式服务测试通过')


if __name__ == '__main__':
    main()
