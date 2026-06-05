# Hermes Deep Thinking 增强版

Hermes Agent 增强版深度思考技能，集成 ReAct + ToT + Deep Thinking。

## 🚀 核心特性

### 三大增强引擎

- **ReAct 引擎**：自动信息搜集，推理-行动-观察-反思循环
- **ToT 引擎**：思维树多路径探索，结构化推理
- **Deep Thinking Phase 7**：真正的知识综合，LLM 驱动的结论形成

### 性能提升

| 维度 | 原版 | 增强版 | 提升幅度 |
|------|------|--------|----------|
| 反思次数 | 2-3 次 | 5+ 次 | +67% 至 +150% |
| 多路径探索 | 单路径 | 树状结构 | 结构化 |
| Token 效率 | 基准 | -65%（Phase 7） | 优化 |
| 自动化程度 | 手动 | 自动 | 全自动 |

### L2 工作流优化

| 指标 | 原版 L2 | 增强版 L2 | 提升 |
|------|---------|----------|------|
| 步骤数 | 4 步 | 2 步 | -50% |
| 技能调用 | 2 次 | 1 次 | -50% |
| 交互次数 | 3-4 次 | 1 次 | -75% |
| 信息搜集 | 手动 | 自动（ReAct） | 全自动 |

---

## 📦 安装指南

### 前置条件

- Hermes Agent 已安装
- Python 3.8+
- LLM API 访问权限（OpenAI、Anthropic 等）

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/xx-del/hermes-deep-thinking-enhanced.git
cd hermes-deep-thinking-enhanced
```

2. 复制到 Hermes 技能目录：
```bash
cp -r . ~/.hermes/skills/openclaw-imports/deep-thinking/
```

3. 在 Hermes 配置中启用：
```yaml
# ~/.hermes/config.yaml
skills:
  - openclaw-imports/deep-thinking
```

---

## 🔧 配置说明

编辑 `config/default_config.yaml`：

### 启用 ToT（多路径探索）

```yaml
deep_thinking:
  enhanced:
    tot_enabled: true
    tot_config:
      max_depth: 3        # 最大探索深度
      max_branches: 3     # 每层最大分支数
      beam_width: 2       # 保留的最佳路径数
```

**参数说明**：
- `max_depth`：思维树的最大深度，值越大探索越深
- `max_branches`：每个节点的最大分支数，值越大探索越广
- `beam_width`：保留的最佳路径数，用于剪枝

### 启用 ReAct（自动工具调用）

```yaml
deep_thinking:
  enhanced:
    react_enabled: true
    react_config:
      max_iterations: 5   # 最大迭代次数
      auto_reflect: true   # 自动反思
```

**参数说明**：
- `max_iterations`：ReAct 循环的最大次数
- `auto_reflect`：是否在每次循环后自动反思

### 最强模式（ToT + ReAct）

```yaml
deep_thinking:
  enhanced:
    tot_enabled: true
    react_enabled: true
```

同时启用 ToT 和 ReAct，获得最强推理能力。

---

## 📖 使用方法

### CLI 使用

```bash
cd scripts
python enhanced_thinking.py "你的复杂问题"
```

**示例**：
```bash
python enhanced_thinking.py "分析微服务架构和单体架构的权衡"
```

### 代码使用

```python
from enhanced_thinking import EnhancedDeepThinking

# 创建实例
thinker = EnhancedDeepThinking()

# 启用增强
thinker.config["deep_thinking"]["enhanced"]["tot_enabled"] = True
thinker.config["deep_thinking"]["enhanced"]["react_enabled"] = True

# 执行思考
result = thinker.think("分析微服务架构和单体架构的权衡")

# 查看结果
print(result["conclusion"])
```

### Hermes 集成

技能会自动集成到 Hermes Agent 的 L2 思考任务中。当用户请求分析或规划时，Hermes 会自动调用此增强版深度思考技能。

**L2 任务示例**：
- "分析如何优化系统性能"
- "制定数据库迁移方案"
- "评估技术选型的优劣"

---

## 🧪 测试验证

### 运行测试套件

```bash
cd scripts
python test_enhanced_thinking.py
```

### 测试场景

1. **信息密集型任务**：对比 ReAct 启用前后的效果
2. **复杂决策任务**：对比 ToT 启用前后的效果
3. **最强模式**：ToT + ReAct + Deep Thinking 全部启用

### 验证指标

- ✅ ReAct 步骤数 > 10（信息搜集充足）
- ✅ ToT 探索节点 > 3（多路径探索）
- ✅ Phase 7 增强引擎 = Deep Thinking（知识综合）

---

## 🏗️ 架构说明

### 七阶段流程

```
增强版深度思考
├─ Phase 1: 初始参与（Initial Engagement）
├─ Phase 2: 搜索方案 ← ReAct 引擎（自动）
├─ Phase 3: 问题分解（Problem Decomposition）
├─ Phase 4: 多假设生成 ← ToT 引擎（多路径）
├─ Phase 5: 自然发现（Natural Discovery）
├─ Phase 6: 验证纠错（Verification）
└─ Phase 7: 知识综合 ← Deep Thinking（LLM 驱动）
```

### 三层架构

1. **方法论层**：深度思考七阶段流程（保持不变）
2. **技术增强层**：ToT（Phase 4）+ ReAct（Phase 2）- 可选启用
3. **基础设施层**：Hermes 工具生态

### ReAct 循环

```
Thought（推理）
   ↓
Action（行动）
   ↓
Observation（观察）
   ↓
Reflect（反思）
   ↓
重复或结束
```

### ToT 探索

```
根节点
├─ 分支 1（得分 0.85）
│  ├─ 子分支 1.1
│  └─ 子分支 1.2
├─ 分支 2（得分 0.72）
│  └─ 子分支 2.1
└─ 分支 3（得分 0.68）
```

---

## ⚠️ 注意事项

### Token 消耗

- 增强模式可能消耗 5-8 倍于原版的 Token
- Phase 7 提示已优化，节省 65% Token
- 仅在复杂任务时启用，简单任务使用原版

**Token 消耗估算**：

| 模式 | Token 倍数 | 适用场景 |
|------|-----------|----------|
| 未增强 | 1x | 简单任务 |
| 仅 ReAct | 2-3x | 信息搜集密集型 |
| 仅 ToT | 3-5x | 复杂决策型 |
| 最强模式 | 5-8x | 超复杂任务 |

### 向下兼容

- **默认**：增强功能关闭，行为与原版完全一致
- **配置驱动**：可选启用，灵活控制
- **有机思考**：保持自然推理流程，非机械化执行

### 限制

- 需要 LLM API 访问权限才能发挥完整功能
- 无 LLM 客户端时工作在降级模式
- 复杂推理任务 Token 成本较高

---

## ❓ 常见问题

### Q1: 如何判断是否需要启用增强？

**A**: 根据任务复杂度判断：
- **简单任务**（单步推理）：不需要启用
- **中等任务**（需要搜集信息）：启用 ReAct
- **复杂任务**（需要多路径探索）：启用 ToT
- **超复杂任务**（需要深度分析）：启用最强模式

### Q2: Token 消耗太高怎么办？

**A**: 
1. 降低 `max_iterations`（ReAct）或 `max_depth`（ToT）
2. 仅在关键步骤启用增强
3. 使用更便宜的 LLM 模型

### Q3: 如何验证增强功能是否生效？

**A**: 
1. 查看输出中的"Phase 2 ← ReAct"和"Phase 4 ← ToT"
2. 检查 ReAct 步骤数和 ToT 探索节点数
3. 确认 Phase 7 增强引擎为"Deep Thinking"

### Q4: 降级模式是什么？

**A**: 
当没有配置 LLM 客户端时，技能会工作在降级模式：
- ReAct 和 ToT 仍可正常工作
- Phase 7 使用固定模板输出
- 功能完整但结论质量可能较低

### Q5: 如何回退到原版？

**A**: 
```bash
# 禁用增强
thinker.config["deep_thinking"]["enhanced"]["tot_enabled"] = False
thinker.config["deep_thinking"]["enhanced"]["react_enabled"] = False
```

或恢复原版 deep-thinking 技能（参考备份目录）。

---

## 📊 性能对比

### 反思次数对比

| 任务类型 | 原版 | 增强版 | 提升 |
|---------|------|--------|------|
| 信息搜集 | 2 次 | 5 次 | +150% |
| 方案设计 | 3 次 | 5 次 | +67% |
| 问题诊断 | 2 次 | 6 次 | +200% |

### L2 工作流对比

**原版 L2 流程**：
```
1. 初次思考（调用 deep-thinking）
   ↓
2. 信息搜集（手动执行）
   ↓
3. 二次思考（调用 deep-thinking）
   ↓
4. 输出结果
```
**交互次数**：3-4 次  
**技能调用**：2 次

**增强版 L2 流程**：
```
1. 思考（调用 deep-thinking）
   ├─ Phase 2: ReAct 自动搜集
   ├─ Phase 4: ToT 多路径探索
   └─ Phase 7: Deep Thinking 深度思考
   ↓
2. 输出结果
```
**交互次数**：1 次  
**技能调用**：1 次

**效率提升**：
- 步骤减少：50%
- 交互减少：75%
- 自动化：100%

---

## 📚 文档资源

- [SKILL.md](./SKILL.md)：完整技能文档
- [README.md](./README.md)：英文使用说明
- [references/design.md](./references/design.md)：架构设计文档
- [references/examples.md](./references/examples.md)：使用示例
- [references/reasoning-frameworks.md](./references/reasoning-frameworks.md)：推理框架对比
- [references/phase7-deep-thinking-implementation-20260605.md](./references/phase7-deep-thinking-implementation-20260605.md)：Phase 7 实现细节

---

## 🤝 贡献指南

欢迎贡献！请：

1. Fork 本仓库
2. 创建特性分支（`git checkout -b feature/AmazingFeature`）
3. 提交更改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 提交 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

---

## 🙏 致谢

- Hermes Agent 原版 deep-thinking 技能
- Yao et al. 的 ReAct 框架
- Yao et al. 的 Tree of Thoughts 框架
- Hermes Agent 社区

---

## 📊 更新日志

### v1.0.0 (2026-06-05)

**首次发布**：
- ✅ ReAct 引擎集成
- ✅ ToT 引擎集成
- ✅ Phase 7 Deep Thinking 实现
- ✅ Token 优化（节省 65%）
- ✅ 完整测试套件
- ✅ 详细文档

**性能验证**：
- ReAct 步骤数：20 步（5 次反思）
- ToT 探索节点：13 个
- Phase 7 增强：Deep Thinking
- 功能满足度：3/3（完全满足）

---

**维护者**：xx-del  
**仓库地址**：https://github.com/xx-del/hermes-deep-thinking-enhanced  
**问题反馈**：https://github.com/xx-del/hermes-deep-thinking-enhanced/issues  
**英文文档**：[README.md](./README.md)
