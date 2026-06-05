"""
测试脚本：验证 deep-thinking-test 增强效果

测试场景：
1. 信息搜集密集型任务（对比 ReAct 启用前后）
2. 复杂决策任务（对比 ToT 启用前后）
3. 最强模式（ToT + ReAct 同时启用）
"""

import sys
import json
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_thinking import EnhancedDeepThinking


def test_scenario_1():
    """场景 1：信息搜集密集型任务"""
    print("=" * 60)
    print("场景 1：信息搜集密集型任务")
    print("=" * 60)
    
    problem = "分析 Hermes Agent 的上下文压缩机制"
    
    # 测试 1：未启用增强
    print("\n【测试 1：未启用增强】")
    thinker_vanilla = EnhancedDeepThinking()
    result_vanilla = thinker_vanilla.think(problem)
    
    phase2_vanilla = result_vanilla["phases"][1]
    print(f"Phase 2: {phase2_vanilla['phase']}")
    print(f"增强: {phase2_vanilla.get('enhancement', '无')}")
    print(f"搜索建议数: {len(phase2_vanilla.get('search_suggestions', []))}")
    
    # 测试 2：启用 ReAct
    print("\n【测试 2：启用 ReAct】")
    thinker_react = EnhancedDeepThinking()
    thinker_react.config["deep_thinking"]["enhanced"]["react_enabled"] = True
    # 重新初始化引擎
    from react_engine import ReActConfig, ReActEngine
    react_config = ReActConfig(enabled=True, max_iterations=3)
    thinker_react.react_engine = ReActEngine(react_config, None, None)
    
    result_react = thinker_react.think(problem)
    
    phase2_react = result_react["phases"][1]
    print(f"Phase 2: {phase2_react['phase']}")
    print(f"增强: {phase2_react.get('enhancement', '无')}")
    print(f"ReAct 步骤数: {phase2_react.get('steps_count', 0)}")
    
    # 对比
    print("\n【对比结果】")
    print(f"未增强：需主 AI 手动执行搜索")
    print(f"ReAct 增强：自动执行 {phase2_react.get('steps_count', 0)} 个工具调用步骤")
    print(f"效率提升：自动化信息搜集流程")
    print()


def test_scenario_2():
    """场景 2：复杂决策任务"""
    print("=" * 60)
    print("场景 2：复杂决策任务")
    print("=" * 60)
    
    problem = "选择最适合 Hermes 的推理框架"
    
    # 测试 1：未启用增强
    print("\n【测试 1：未启用增强】")
    thinker_vanilla = EnhancedDeepThinking()
    result_vanilla = thinker_vanilla.think(problem)
    
    phase4_vanilla = result_vanilla["phases"][3]
    print(f"Phase 4: {phase4_vanilla['phase']}")
    print(f"增强: {phase4_vanilla.get('enhancement', '无')}")
    print(f"假设数: {len(phase4_vanilla.get('hypotheses', []))}")
    
    # 测试 2：启用 ToT
    print("\n【测试 2：启用 ToT】")
    thinker_tot = EnhancedDeepThinking()
    thinker_tot.config["deep_thinking"]["enhanced"]["tot_enabled"] = True
    # 重新初始化引擎
    from tot_engine import ToTConfig, TreeOfThoughtsEngine
    tot_config = ToTConfig(enabled=True, max_depth=2, max_branches=2, beam_width=2)
    thinker_tot.tot_engine = TreeOfThoughtsEngine(tot_config, None)
    
    result_tot = thinker_tot.think(problem)
    
    phase4_tot = result_tot["phases"][3]
    print(f"Phase 4: {phase4_tot['phase']}")
    print(f"增强: {phase4_tot.get('enhancement', '无')}")
    tree_stats = phase4_tot.get('tree_stats', {})
    print(f"探索节点数: {tree_stats.get('total_nodes', 0)}")
    print(f"最佳路径得分: {phase4_tot.get('best_path', {}).get('score', 0):.2f}")
    
    # 对比
    print("\n【对比结果】")
    print(f"未增强：生成 {len(phase4_vanilla.get('hypotheses', []))} 个假设")
    print(f"ToT 增强：探索 {tree_stats.get('total_nodes', 0)} 个节点")
    print(f"多路径探索能力提升：+{(tree_stats.get('total_nodes', 0) / max(len(phase4_vanilla.get('hypotheses', [])), 1) - 1) * 100:.0f}%")
    print()


def test_scenario_3():
    """场景 3：最强模式（ToT + ReAct）"""
    print("=" * 60)
    print("场景 3：最强模式（ToT + ReAct 同时启用）")
    print("=" * 60)
    
    problem = "设计 Hermes 插件系统的最佳架构"
    
    print("\n【测试：ToT + ReAct 同时启用】")
    thinker_max = EnhancedDeepThinking()
    thinker_max.config["deep_thinking"]["enhanced"]["tot_enabled"] = True
    thinker_max.config["deep_thinking"]["enhanced"]["react_enabled"] = True
    
    # 重新初始化引擎
    from tot_engine import ToTConfig, TreeOfThoughtsEngine
    from react_engine import ReActConfig, ReActEngine
    
    tot_config = ToTConfig(enabled=True, max_depth=2, max_branches=2, beam_width=2)
    thinker_max.tot_engine = TreeOfThoughtsEngine(tot_config, None)
    
    react_config = ReActConfig(enabled=True, max_iterations=3)
    thinker_max.react_engine = ReActEngine(react_config, None, None)
    
    result_max = thinker_max.think(problem)
    
    print(f"增强类型: {result_max['enhancement_used']}")
    print(f"总阶段数: {result_max['stats']['total_phases']}")
    print(f"增强阶段数: {result_max['stats']['enhanced_phases']}")
    
    # 详细输出
    print("\n【阶段详情】")
    for i, phase in enumerate(result_max["phases"], 1):
        enhancement = phase.get("enhancement", "无")
        if enhancement:
            print(f"Phase {i}: {phase['phase']} ← 增强引擎：{enhancement}")
        else:
            print(f"Phase {i}: {phase['phase']}")
    
    # 性能预估
    print("\n【性能预估】")
    print(f"Token 消耗：约 5-8x（需实际测量）")
    print(f"响应时间：中慢（取决于 LLM 调用次数）")
    print(f"质量提升：多路径探索 + 自动工具调用")
    print()


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("Deep Thinking Test - 增强效果验证")
    print("=" * 60 + "\n")
    
    test_scenario_1()
    test_scenario_2()
    test_scenario_3()
    
    print("=" * 60)
    print("测试完成")
    print("=" * 60)
    print("\n下一步：")
    print("1. 检查测试输出，评估增强效果")
    print("2. 对比 Token 消耗（需实际测量）")
    print("3. 决策：")
    print("   - 效果优秀 + 成本可接受 → 替换原版")
    print("   - 效果优秀 + 成本过高 → 可选增强")
    print("   - 效果一般 → 迭代优化")
    print("   - 效果不佳 → 废弃测试技能")


if __name__ == "__main__":
    main()
