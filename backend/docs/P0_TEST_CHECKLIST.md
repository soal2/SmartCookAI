# P0 AI 功能测试 - 执行检查清单

## 测试前准备 ✓

### 1. 环境配置检查
```bash
# 检查项目目录
cd /Users/eversse/Documents/codes/VibeCoding/SmartCookAI/backend

# 检查 Python 环境
python --version  # 应该是 Python 3.8+

# 检查依赖安装
pip list | grep -E "flask|langchain|dashscope|sqlalchemy"
```

**预期结果**:
- ✅ Flask 3.0.0
- ✅ langchain-community
- ✅ SQLAlchemy 2.0.23

### 2. API Key 配置检查
```bash
# 检查 .env 文件
cat .env | grep DASHSCOPE_API_KEY

# 验证配置
python -c "from config import Config; Config.validate(); print('✅ 配置正确')"
```

**预期结果**:
- ✅ DASHSCOPE_API_KEY 已设置
- ✅ 配置验证通过

### 3. 数据库检查
```bash
# 检查数据库文件
ls -lh smartcook.db

# 如果不存在，初始化数据库
python init_db.py
```

**预期结果**:
- ✅ smartcook.db 文件存在
- ✅ 数据库表已创建

### 4. 测试文件检查
```bash
# 检查测试文件
ls -lh test_*.py run_all_tests.py quick_test.sh

# 检查执行权限
ls -l *.py *.sh | grep "x"
```

**预期结果**:
- ✅ test_ai_generation.py (17KB)
- ✅ test_performance.py (7.6KB)
- ✅ test_e2e.py (11KB)
- ✅ run_all_tests.py (3.3KB)
- ✅ quick_test.sh (2.0KB)
- ✅ 所有文件可执行

## 测试执行 ✓

### 方式1: 使用快速启动脚本 (推荐)
```bash
./quick_test.sh
```

**选择选项**:
- 选项1: 运行所有测试 (完整测试)
- 选项2: AI 功能完整性测试
- 选项3: 性能测试
- 选项4: 端到端测试

### 方式2: 运行所有测试
```bash
python run_all_tests.py
```

**预期输出**:
```
======================================================================
  SmartCook AI - P0 AI 功能测试套件
  Master Test Runner
======================================================================

📋 测试计划:
  1. AI 功能完整性测试
  2. 性能测试
  3. 端到端测试

按 Enter 键开始测试...
```

### 方式3: 单独运行测试

#### 测试1: AI 功能完整性
```bash
python test_ai_generation.py
```

**检查点**:
- [ ] 单一食材生成成功
- [ ] 多种食材生成成功
- [ ] 筛选条件正常工作
- [ ] 食材状态标注正确
- [ ] 创意菜名符合要求
- [ ] 数据库保存成功

**预期通过率**: > 80%

#### 测试2: 性能测试
```bash
python test_performance.py
```

**检查点**:
- [ ] 完整生成时间 < 15秒
- [ ] 不同食材数量性能稳定
- [ ] 筛选条件不显著影响性能
- [ ] 并发请求正常

**预期性能**:
- 平均响应时间: 8-12秒
- 最快响应时间: 6-8秒
- 最慢响应时间: 12-15秒

#### 测试3: 端到端测试
```bash
python test_e2e.py
```

**检查点**:
- [ ] 场景1: 新手用户快速做饭 - 通过
- [ ] 场景2: 家庭主妇营养搭配 - 通过
- [ ] 场景3: 剩余食材处理 - 通过

**预期结果**: 3/3 场景通过

## 测试结果验证 ✓

### 1. 功能完整性验证
```bash
# 查看最新生成的食谱
python -c "
from app import create_app
from app.services.recipe_service import recipe_service
app = create_app()
with app.app_context():
    recipes = recipe_service.get_recipe_history(limit=3)
    for r in recipes:
        print(f'✅ {r[\"name\"]} - {r[\"difficulty\"]} - {r[\"cooking_time\"]}')
"
```

**预期输出**:
```
✅ 黄金满屋蛋炒饭 - 新手 - 15分钟
✅ 番茄滑蛋盖饭 - 新手 - 20分钟
✅ 西红柿炒鸡蛋 - 新手 - 10分钟
```

### 2. 数据库验证
```bash
# 查看数据库记录数
sqlite3 smartcook.db "SELECT COUNT(*) FROM recipes;"

# 查看最新3条记录
sqlite3 smartcook.db "SELECT id, name, difficulty FROM recipes ORDER BY created_at DESC LIMIT 3;"
```

**预期结果**:
- ✅ 记录数 > 0
- ✅ 最新记录包含测试生成的食谱

### 3. 日志验证
```bash
# 查看日志输出 (如果有日志文件)
tail -50 logs/smartcook.log 2>/dev/null || echo "日志输出到控制台"
```

**预期内容**:
- ✅ AI 模型初始化成功
- ✅ 食谱生成请求日志
- ✅ AI 响应成功日志
- ✅ 食谱保存成功日志

## 常见问题排查 ✓

### 问题1: API Key 错误
**症状**: `DASHSCOPE_API_KEY 未设置`

**解决步骤**:
```bash
# 1. 检查 .env 文件
cat .env

# 2. 如果不存在，创建
cp .env.example .env

# 3. 编辑并添加 API Key
nano .env
# 添加: DASHSCOPE_API_KEY=sk-your-key-here

# 4. 验证
python -c "from config import Config; print(Config.DASHSCOPE_API_KEY[:10])"
```

### 问题2: 模块导入错误
**症状**: `ModuleNotFoundError: No module named 'xxx'`

**解决步骤**:
```bash
# 重新安装依赖
pip install -r requirements.txt

# 验证安装
pip list | grep -E "flask|langchain|dashscope"
```

### 问题3: 数据库错误
**症状**: `no such table: recipes`

**解决步骤**:
```bash
# 重新初始化数据库
rm smartcook.db
python init_db.py

# 验证
sqlite3 smartcook.db ".tables"
```

### 问题4: 测试超时
**症状**: 测试运行时间过长

**解决步骤**:
1. 检查网络连接
2. 验证 API 服务状态
3. 考虑使用更快的模型 (qwen-turbo)
4. 减少测试用例数量

### 问题5: JSON 解析失败
**症状**: `JSON 解析失败`

**解决步骤**:
```bash
# 查看详细日志
python test_ai_generation.py 2>&1 | grep -A 5 "JSON 解析失败"

# 检查 AI 响应格式
# 可能需要优化 Prompt
```

## 成功标准检查 ✓

### P0 完成标准
- [ ] AI 功能完整性测试通过 (通过率 > 80%)
- [ ] 性能测试达标 (< 15秒)
- [ ] 端到端测试通过 (3/3 场景)
- [ ] 日志系统正常工作
- [ ] 错误处理正常
- [ ] 数据持久化正常

### 质量指标
- [ ] 测试覆盖率 > 80%
- [ ] 响应时间 < 15秒
- [ ] 生成成功率 > 95%
- [ ] 无严重错误

### 用户体验
- [ ] 生成的食谱可执行
- [ ] 步骤清晰易懂
- [ ] 食材用量合理
- [ ] 菜名有吸引力

## 测试报告 ✓

### 测试执行记录
```
测试日期: ___________
测试人员: ___________
测试环境: ___________

测试结果:
□ AI 功能完整性测试: 通过 / 失败
  - 通过率: _____%
  - 失败用例: ___________

□ 性能测试: 通过 / 失败
  - 平均响应时间: _____秒
  - 最慢响应时间: _____秒

□ 端到端测试: 通过 / 失败
  - 场景1: 通过 / 失败
  - 场景2: 通过 / 失败
  - 场景3: 通过 / 失败

总体评价: 优秀 / 良好 / 需改进

备注:
___________________________________________
___________________________________________
```

## 下一步行动 ✓

### 如果所有测试通过
- ✅ P0 AI 功能开发完成
- ✅ 可以进入 P1 优化阶段
- ✅ 准备前端集成

### 如果部分测试失败
1. 记录失败的测试用例
2. 分析失败原因
3. 修复问题
4. 重新运行测试
5. 更新测试报告

### P1 优化计划
- [ ] 实现缓存机制
- [ ] 添加智能食材替代
- [ ] 实现营养分析
- [ ] 优化 Prompt 质量
- [ ] 添加用户反馈机制

## 附录

### 快速命令参考
```bash
# 进入项目目录
cd /Users/eversse/Documents/codes/VibeCoding/SmartCookAI/backend

# 运行所有测试
./quick_test.sh

# 或
python run_all_tests.py

# 单独测试
python test_ai_generation.py
python test_performance.py
python test_e2e.py

# 查看数据库
sqlite3 smartcook.db "SELECT * FROM recipes ORDER BY created_at DESC LIMIT 5;"

# 验证配置
python -c "from config import Config; Config.validate(); print('✅ OK')"
```

### 相关文档
- `P0_IMPLEMENTATION_SUMMARY.md` - 实施总结
- `TESTING_README.md` - 详细测试文档
- `CLAUDE.md` - 项目说明
- `DATABASE_QUICK_REFERENCE.md` - 数据库参考

---

**检查清单完成日期**: ___________
**检查人**: ___________
**签名**: ___________
