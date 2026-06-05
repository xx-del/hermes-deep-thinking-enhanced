# 推理框架对比引用

完整对比文档：`~/.hermes/skills/openclaw-imports/deep-thinking/references/reasoning-frameworks-comparison.md`

## 核心洞察

**不同层次框架对比**：

| 框架类型 | 代表 | 作用层 | 本质 |
|---------|------|--------|------|
| 方法论框架 | deep-thinking | Prompt 层 | 教 AI 如何思考 |
| 算法实现框架 | Tree of Thoughts | 算法层 | 实现具体推理机制 |
| 工程集成框架 | ReAct | 应用层 | 集成工具和推理 |

## 集成方案

**方案 A（推荐）：增强 deep-thinking**

保持方法论优势，在技术实现层引入 ToT/ReAct 机制

**实施路径**：
```
deep-thinking (方法论层)
├── Phase 2 (Search for Solutions)
│   └── 引入 ReAct 实现工具调用
└── Phase 4 (Multiple Hypotheses)
    └── 引入 ToT 实现多路径探索
```

**增强效果**：
- 步骤减少 67%（3 步手动 → 1 步自动）
- 迭代能力提升 3-5 倍
