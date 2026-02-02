#!/bin/bash
# SmartCook AI - P0 AI 功能测试快速启动脚本

echo "======================================================================"
echo "  SmartCook AI - P0 AI 功能测试"
echo "======================================================================"
echo ""

# 检查是否在 backend 目录
if [ ! -f "config.py" ]; then
    echo "❌ 错误: 请在 backend 目录下运行此脚本"
    echo "   cd backend && ./quick_test.sh"
    exit 1
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "❌ 错误: .env 文件不存在"
    echo ""
    echo "请执行以下步骤:"
    echo "  1. cp .env.example .env"
    echo "  2. 编辑 .env 文件，添加 DASHSCOPE_API_KEY"
    exit 1
fi

# 检查 API Key
if ! grep -q "DASHSCOPE_API_KEY=sk-" .env; then
    echo "⚠️  警告: DASHSCOPE_API_KEY 可能未正确配置"
    echo ""
    read -p "是否继续? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ 环境检查通过"
echo ""

# 显示测试选项
echo "请选择测试类型:"
echo "  1. 运行所有测试 (推荐)"
echo "  2. AI 功能完整性测试"
echo "  3. 性能测试"
echo "  4. 端到端测试"
echo "  5. 退出"
echo ""

read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🚀 运行所有测试..."
        python run_all_tests.py
        ;;
    2)
        echo ""
        echo "🚀 运行 AI 功能完整性测试..."
        python test_ai_generation.py
        ;;
    3)
        echo ""
        echo "🚀 运行性能测试..."
        python test_performance.py
        ;;
    4)
        echo ""
        echo "🚀 运行端到端测试..."
        python test_e2e.py
        ;;
    5)
        echo "退出"
        exit 0
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "======================================================================"
echo "  测试完成"
echo "======================================================================"
