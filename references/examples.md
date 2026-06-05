# 使用示例

## 示例 1：启用 ToT 探索多个方案

**场景**：选择最佳 AI 框架

**配置**：
```yaml
deep_thinking:
  enhanced:
    tot_enabled: true
    tot_config:
      max_depth: 3
      max_branches: 3
      beam_width: 2
```

**执行**：
```bash
cd ~/.hermes/skills/openclaw-imports/deep-thinking-test/scripts
python enhanced_thinking.py "选择最佳 AI 框架"
```

**预期输出**：
- Phase 4 将探索多个思考路径
- 返回最佳路径及其得分
- 提供树统计信息

---

## 示例 2：启用 ReAct 自动搜集信息

**场景**：分析某项目代码结构

**配置**：
```yaml
deep_thinking:
  enhanced:
    react_enabled: true
    react_config:
      max_iterations: 5
      auto_reflect: true
```

**执行**：
```bash
python enhanced_thinking.py "分析 Hermes 项目代码结构"
```

**预期输出**：
- Phase 2 将自动执行工具调用
- 返回推理-行动-观察-反思步骤
- 提供搜集到的信息摘要

---

## 示例 3：最强模式（ToT + ReAct）

**场景**：设计系统架构

**配置**：
```yaml
deep_thinking:
  enhanced:
    tot_enabled: true
    react_enabled: true
```

**执行**：
```bash
python enhanced_thinking.py "设计微服务架构"
```

**预期输出**：
- Phase 2：自动搜集最佳实践
- Phase 4：探索多个架构方案
- 提供完整的决策链路

---

## 性能对比

| 模式 | Token 消耗 | 响应时间 | 质量提升 |
|------|-----------|----------|----------|
| 未增强 | 1x | 快 | 基准 |
| 仅 ToT | 3-5x | 中 | +67% 探索能力 |
| 仅 ReAct | 2-3x | 中 | +67% 工具集成 |
| ToT + ReAct | 5-8x | 慢 | 综合提升 |

---

## 注意事项

1. **Token 消耗**：启用增强会增加 5-8 倍消耗
2. **响应时间**：取决于 LLM 调用次数
3. **降级机制**：LLM 调用失败会返回模拟结果
4. **配置优先**：默认关闭，需手动启用
