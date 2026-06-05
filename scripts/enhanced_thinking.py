"""
Enhanced Deep Thinking - 增强版深度思考

融合 deep-thinking 方法论 + ToT/ReAct 技术增强
保持原版优势，可选启用增强
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, List
import sys

# 导入引擎
from tot_engine import TreeOfThoughtsEngine, ToTConfig
from react_engine import ReActEngine, ReActConfig


class EnhancedDeepThinking:
    """增强版 deep-thinking"""
    
    def __init__(self, config_path: str = None, llm_client=None, tool_executor=None):
        """
        初始化增强版 deep-thinking
        
        Args:
            config_path: 配置文件路径
            llm_client: LLM 调用接口
            tool_executor: 工具执行器
        """
        # 加载配置
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "default_config.yaml"
        
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        
        # 初始化引擎
        self.tot_engine = None
        self.react_engine = None
        
        enhanced_config = self.config.get("deep_thinking", {}).get("enhanced", {})
        
        # 初始化 ToT 引擎
        if enhanced_config.get("tot_enabled", False):
            tot_config_dict = enhanced_config.get("tot_config", {})
            tot_config = ToTConfig(
                enabled=True,
                max_depth=tot_config_dict.get("max_depth", 3),
                max_branches=tot_config_dict.get("max_branches", 3),
                beam_width=tot_config_dict.get("beam_width", 2),
                score_threshold=tot_config_dict.get("score_threshold", 0.8),
                exploration_strategy=tot_config_dict.get("exploration_strategy", "beam")
            )
            self.tot_engine = TreeOfThoughtsEngine(tot_config, llm_client)
        
        # 初始化 ReAct 引擎
        if enhanced_config.get("react_enabled", False):
            react_config_dict = enhanced_config.get("react_config", {})
            react_config = ReActConfig(
                enabled=True,
                max_iterations=react_config_dict.get("max_iterations", 5),
                tools=react_config_dict.get("tools", []),
                auto_reflect=react_config_dict.get("auto_reflect", True)
            )
            self.react_engine = ReActEngine(react_config, tool_executor, llm_client)
    
    def think(self, problem: str) -> Dict[str, Any]:
        """
        执行增强版思考流程
        
        Args:
            problem: 待解决的问题
        
        Returns:
            思考结果字典
        """
        result = {
            "problem": problem,
            "phases": [],
            "enhancement_used": {
                "tot": self.tot_engine is not None,
                "react": self.react_engine is not None
            },
            "stats": {}
        }
        
        # Phase 1: Initial Engagement
        phase1 = self._initial_engagement(problem)
        result["phases"].append(phase1)
        
        # Phase 2: Search for Existing Solutions
        if self.react_engine:
            # ReAct 增强：自动执行工具调用
            phase2 = self._search_with_react(problem, phase1)
        else:
            # 未增强：输出搜索建议
            phase2 = self._search_manual(problem, phase1)
        result["phases"].append(phase2)
        
        # Phase 3: Problem Decomposition
        phase3 = self._problem_decomposition(problem, result["phases"])
        result["phases"].append(phase3)
        
        # Phase 4: Multiple Hypotheses
        if self.tot_engine:
            # ToT 增强：多路径探索
            phase4 = self._hypotheses_with_tot(problem, phase3)
        else:
            # 未增强：单路径推理
            phase4 = self._hypotheses_manual(problem, phase3)
        result["phases"].append(phase4)
        
        # Phase 5: Natural Discovery Flow
        phase5 = self._natural_discovery(problem, result["phases"])
        result["phases"].append(phase5)
        
        # Phase 6: Verification & Error Correction
        phase6 = self._verification(problem, result["phases"])
        result["phases"].append(phase6)
        
        # Phase 7: Knowledge Synthesis
        phase7 = self._knowledge_synthesis(problem, result["phases"])
        result["phases"].append(phase7)
        
        # 统计信息
        result["stats"] = self._build_stats(result)
        
        return result
    
    def _initial_engagement(self, problem: str) -> Dict[str, Any]:
        """Phase 1: Initial Engagement"""
        return {
            "phase": "Initial Engagement",
            "description": "理解问题、识别已知/未知",
            "problem_rephrased": f"重述问题：{problem}",
            "known": ["问题已明确"],
            "unknown": ["需要进一步搜集信息"],
            "enhancement": None
        }
    
    def _search_with_react(self, problem: str, phase1: Dict) -> Dict:
        """Phase 2 增强：ReAct 自动工具调用"""
        steps = self.react_engine.run(f"搜索现有解决方案：{problem}")
        
        return {
            "phase": "Search for Existing Solutions (Enhanced with ReAct)",
            "description": "自动执行工具调用搜集信息",
            "steps": [step.to_dict() for step in steps],
            "steps_count": len(steps),
            "enhancement": "ReAct"
        }
    
    def _search_manual(self, problem: str, phase1: Dict) -> Dict:
        """Phase 2 未增强：手动搜索建议"""
        return {
            "phase": "Search for Existing Solutions",
            "description": "输出搜索建议，需主 AI 手动执行",
            "search_suggestions": [
                f"搜索关键词：{problem} 实现",
                "搜索 GitHub：{problem}",
                "搜索文档：{problem}"
            ],
            "enhancement": None
        }
    
    def _problem_decomposition(self, problem: str, phases: List[Dict]) -> Dict:
        """Phase 3: Problem Decomposition"""
        return {
            "phase": "Problem Decomposition",
            "description": "分解核心组件、识别约束",
            "components": [
                "核心问题分析",
                "约束条件识别",
                "成功标准定义"
            ],
            "enhancement": None
        }
    
    def _hypotheses_with_tot(self, problem: str, phase3: Dict) -> Dict:
        """Phase 4 增强：ToT 多路径探索"""
        best_path = self.tot_engine.beam_search(problem)
        
        return {
            "phase": "Multiple Hypotheses (Enhanced with ToT)",
            "description": "多路径探索，选择最佳方案",
            "best_path": best_path.to_dict(),
            "tree_stats": self.tot_engine.get_tree_stats(),
            "enhancement": "ToT"
        }
    
    def _hypotheses_manual(self, problem: str, phase3: Dict) -> Dict:
        """Phase 4 未增强：单路径推理"""
        return {
            "phase": "Multiple Hypotheses",
            "description": "生成 2-3 个可能方案",
            "hypotheses": [
                f"方案 1：基于 {problem} 的标准实现",
                f"方案 2：替代方案探索",
                f"方案 3：创新性思路"
            ],
            "enhancement": None
        }
    
    def _natural_discovery(self, problem: str, phases: List[Dict]) -> Dict:
        """Phase 5: Natural Discovery Flow"""
        return {
            "phase": "Natural Discovery Flow",
            "description": "侦探式探索、建立联系",
            "discoveries": [
                "发现关键模式",
                "建立概念联系",
                "深入理解本质"
            ],
            "enhancement": None
        }
    
    def _verification(self, problem: str, phases: List[Dict]) -> Dict:
        """Phase 6: Verification & Error Correction"""
        return {
            "phase": "Verification & Error Correction",
            "description": "验证结论、寻找反例",
            "verification_points": [
                "逻辑一致性检查",
                "边界条件测试",
                "反例搜索"
            ],
            "enhancement": None
        }
    
    def _knowledge_synthesis(self, problem: str, phases: List[Dict]) -> Dict:
        """Phase 7: Knowledge Synthesis - 深度思考并形成结论"""
        
        # 提取前面 Phase 的关键信息
        phase_summary = self._extract_key_insights(phases)
        
        # 构建精简的深度思考提示（三步）
        prompt = f"""
原始问题：{problem}

分析过程：
{phase_summary}

现在，请进行深度思考并形成最终结论：

1. 综合发现
   - 连接 ReAct 搜集的关键信息
   - 连接 ToT 探索的最佳方案
   - 形成整体图景

2. 验证结论
   - 检查逻辑一致性
   - 验证完整性（是否遗漏关键点）
   - 寻找潜在反例

3. 形成建议
   - 核心结论（结论在前）
   - 关键发现（支持结论的依据）
   - 推荐行动（如适用）
   - 注意事项（风险、限制、权衡）

请输出：
1. 核心结论（结论在前）
2. 关键发现（支持结论的依据）
3. 推荐行动（如适用）
4. 注意事项（风险、限制、权衡）
"""
        
        # 调用 LLM 进行深度思考（如果有 LLM 客户端）
        if self.llm_client:
            try:
                conclusion = self.llm_client.generate(prompt)
            except Exception as e:
                conclusion = f"深度思考失败: {e}，请基于前面的分析自行得出结论。"
        else:
            # 降级：返回示例结论
            conclusion = f"""
基于前面的分析，对问题「{problem}」的深度思考结论：

1. 核心结论
   - 已完成 Phase 1-6 的分析
   - 关键洞察已提取
   - 需要进一步综合分析

2. 关键发现
   - 分析过程中发现了多个关键点
   - 部分信息之间存在联系
   - 需要验证完整性

3. 推荐行动
   - 基于前面的分析结果执行
   - 注意验证假设
   - 考虑边缘情况

4. 注意事项
   - 信息搜集可能不完整
   - 部分结论需要验证
   - 建议进一步调研

（注：此为降级输出，无 LLM 客户端）
"""
        
        return {
            "phase": "Knowledge Synthesis",
            "description": "深度思考并形成结论",
            "conclusion": conclusion,
            "enhancement": "Deep Thinking",
            "phases_summary": phase_summary
        }
    
    def _extract_key_insights(self, phases: List[Dict]) -> str:
        """提取前面 Phase 的关键洞察"""
        insights = []
        
        for phase in phases:
            if phase.get("enhancement"):
                # ReAct 或 ToT 的结果
                if "steps" in phase:  # ReAct
                    insights.append(f"\n[{phase['phase']}]")
                    insights.append(f"- 搜集步骤：{phase['steps_count']} 步")
                    # 提取关键观察
                    observations = [s['content'] for s in phase['steps'] if s['step_type'] == 'observation']
                    if observations:
                        insights.append(f"- 关键观察：")
                        for obs in observations[:3]:  # 最多 3 个
                            insights.append(f"  • {obs[:100]}")
                elif "best_path" in phase:  # ToT
                    insights.append(f"\n[{phase['phase']}]")
                    insights.append(f"- 最佳路径得分：{phase['best_path']['score']:.2f}")
                    insights.append(f"- 最佳方案：{phase['best_path']['content'][:100]}")
                    tree_stats = phase.get('tree_stats', {})
                    if tree_stats:
                        insights.append(f"- 探索节点：{tree_stats.get('total_nodes', 0)} 个")
            else:
                # 普通 Phase
                insights.append(f"\n[{phase['phase']}]")
                if "problem_rephrased" in phase:
                    insights.append(f"- 问题重述：{phase['problem_rephrased']}")
                elif "known" in phase and "unknown" in phase:
                    insights.append(f"- 已知：{', '.join(phase['known'][:2])}")
                    insights.append(f"- 未知：{', '.join(phase['unknown'][:2])}")
                elif "components" in phase:
                    insights.append(f"- 核心组件：{', '.join(phase['components'][:3])}")
                elif "hypotheses" in phase:
                    insights.append(f"- 假设数量：{len(phase['hypotheses'])} 个")
                elif "discoveries" in phase:
                    insights.append(f"- 关键发现：{', '.join(phase['discoveries'][:3])}")
                elif "verification_points" in phase:
                    insights.append(f"- 验证点：{', '.join(phase['verification_points'][:3])}")
        
        return '\n'.join(insights)
    
    def _build_stats(self, result: Dict) -> Dict[str, Any]:
        """构建统计信息"""
        stats = {
            "total_phases": len(result["phases"]),
            "enhanced_phases": sum(1 for p in result["phases"] if p.get("enhancement")),
            "tot_used": result["enhancement_used"]["tot"],
            "react_used": result["enhancement_used"]["react"]
        }
        
        # 添加引擎统计
        if self.tot_engine:
            stats["tot_stats"] = self.tot_engine.get_tree_stats()
        
        if self.react_engine:
            stats["react_stats"] = self.react_engine.get_stats()
        
        return stats


# CLI 入口
if __name__ == "__main__":
    # 解析命令行参数
    problem = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "测试问题"
    
    # 创建增强版思考器
    thinker = EnhancedDeepThinking()
    
    # 执行思考
    result = thinker.think(problem)
    
    # 输出结果
    print(json.dumps(result, indent=2, ensure_ascii=False))
