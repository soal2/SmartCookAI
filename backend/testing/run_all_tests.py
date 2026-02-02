#!/usr/bin/env python3
"""
Master Test Runner
主测试运行器 - 执行所有 P0 AI 功能测试

测试套件:
1. AI 功能完整性测试 (test_ai_generation.py)
2. 性能测试 (test_performance.py)
3. 端到端测试 (test_e2e.py)
"""
import sys
import os
import subprocess
import time

def print_header(title: str):
    """打印标题"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def run_test_script(script_name: str, description: str) -> bool:
    """运行测试脚本"""
    print_header(description)
    print(f"📝 运行脚本: {script_name}\n")

    try:
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=False,
            text=True
        )
        elapsed = time.time() - start_time

        if result.returncode == 0:
            print(f"\n✅ {description} 完成 - 耗时: {elapsed:.2f}秒")
            return True
        else:
            print(f"\n❌ {description} 失败 - 返回码: {result.returncode}")
            return False

    except Exception as e:
        print(f"\n❌ {description} 异常: {e}")
        return False

def main():
    """主函数"""
    print("\n" + "="*70)
    print("  SmartCook AI - P0 AI 功能测试套件")
    print("  Master Test Runner")
    print("="*70)

    print("\n📋 测试计划:")
    print("  1. AI 功能完整性测试")
    print("  2. 性能测试")
    print("  3. 端到端测试")

    print("\n⚠️  注意事项:")
    print("  - 确保已配置 DASHSCOPE_API_KEY")
    print("  - 测试将调用真实的 AI API")
    print("  - 建议在测试环境中运行")
    print("  - 测试可能需要 5-10 分钟")

    input("\n按 Enter 键开始测试...")

    # 记录测试结果
    results = []
    start_time = time.time()

    # 1. AI 功能完整性测试
    results.append((
        "AI 功能完整性测试",
        run_test_script("test_ai_generation.py", "AI 功能完整性测试")
    ))

    # 2. 性能测试
    results.append((
        "性能测试",
        run_test_script("test_performance.py", "性能测试")
    ))

    # 3. 端到端测试
    results.append((
        "端到端测试",
        run_test_script("test_e2e.py", "端到端测试")
    ))

    # 打印总结
    total_time = time.time() - start_time
    print_header("测试总结")

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    print(f"总测试套件数: {total_count}")
    print(f"✅ 通过: {passed_count}")
    print(f"❌ 失败: {total_count - passed_count}")
    print(f"⏱️  总耗时: {total_time:.2f}秒\n")

    print("详细结果:")
    for test_name, passed in results:
        status = "✅" if passed else "❌"
        print(f"  {status} {test_name}")

    if passed_count == total_count:
        print("\n🎉 所有测试套件通过!")
        print("\n✅ P0 AI 功能开发完成，可以进入下一阶段")
    else:
        print("\n⚠️  部分测试套件失败，需要修复")
        print("\n建议:")
        print("  1. 检查失败的测试日志")
        print("  2. 验证 API Key 配置")
        print("  3. 检查网络连接")
        print("  4. 查看详细错误信息")

    print("\n" + "="*70)

if __name__ == '__main__':
    main()
