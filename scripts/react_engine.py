"""
ReAct (Reasoning + Acting) 推理-行动引擎

参考论文: https://arxiv.org/abs/2210.03629
核心：推理-行动-观察-反思循环
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Callable
import json


@dataclass
class ReActStep:
    """ReAct 单步"""
    step_type: str  # "thought" | "action" | "observation" | "reflection"
    content: str
    tool_name: Optional[str] = None
    tool_args: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "step_type": self.step_type,
            "content": self.content,
            "tool_name": self.tool_name,
            "tool_args": self.tool_args,
            "result": str(self.result) if self.result else None
        }


@dataclass
class ReActConfig:
    """ReAct 配置"""
    enabled: bool = False
    max_iterations: int = 5
    tools: List[str] = field(default_factory=lambda: [
        "browser_navigate", "browser_click",
        "terminal", "search_files", "read_file"
    ])
    auto_reflect: bool = True


class ReActEngine:
    """ReAct 推理-行动引擎"""
    
    def __init__(self, config: ReActConfig, tool_executor: Callable = None, llm_client=None):
        self.config = config
        self.tool_executor = tool_executor  # Hermes 工具执行器
        self.llm_client = llm_client  # LLM 调用接口
        
    def run(self, problem: str) -> List[ReActStep]:
        """
        ReAct 推理-行动循环
        
        核心流程：
        1. 推理（思考）
        2. 判断是否需要行动
        3. 行动（执行）
        4. 观察（解析）
        5. 反思（调整）
        6. 循环直到完成
        """
        steps = []
        current_context = problem
        
        for i in range(self.config.max_iterations):
            # Step 1: Thought（推理）
            thought = self._think(current_context, steps)
            steps.append(ReActStep(
                step_type="thought",
                content=thought
            ))
            
            # Step 2: 判断是否需要行动
            if not self._needs_action(thought):
                # 直接返回结论
                break
            
            # Step 3: Action（行动）
            action = self._decide_action(thought)
            steps.append(ReActStep(
                step_type="action",
                content=action["reasoning"],
                tool_name=action["tool"],
                tool_args=action["args"]
            ))
            
            # Step 4: Observation（观察）
            observation = self._execute_tool(action)
            steps.append(ReActStep(
                step_type="observation",
                content=str(observation),
                result=observation
            ))
            
            # Step 5: Reflect（反思）
            if self.config.auto_reflect:
                reflection = self._reflect(observation, steps)
                steps.append(ReActStep(
                    step_type="reflection",
                    content=reflection
                ))
            
            # 更新上下文
            current_context = self._build_context(steps)
            
            # 检查完成条件
            if self._is_complete(steps):
                break
        
        return steps
    
    def _think(self, context: str, steps: List[ReActStep]) -> str:
        """推理阶段"""
        if self.llm_client is None:
            # 降级：返回示例推理
            return f"分析问题：{context[:50]}...，需要进一步搜集信息"
        
        prompt = f"""
当前上下文：{context}

历史步骤：
{self._format_steps(steps)}

请进行推理，思考下一步应该如何做。
"""
        
        try:
            return self.llm_client.generate(prompt)
        except Exception as e:
            print(f"LLM 推理失败: {e}")
            return "推理失败，跳过此步骤"
    
    def _needs_action(self, thought: str) -> bool:
        """判断是否需要行动"""
        # 简单规则：如果推理中包含"需要"、"应该"、"可以"等词，则认为需要行动
        action_keywords = ["需要", "应该", "可以", "搜索", "查询", "读取", "执行"]
        return any(kw in thought for kw in action_keywords)
    
    def _decide_action(self, thought: str) -> Dict[str, Any]:
        """决定行动"""
        if self.llm_client is None:
            # 降级：返回默认行动
            return {
                "reasoning": "需要搜索相关信息",
                "tool": "search_files",
                "args": {"pattern": "test", "path": "."}
            }
        
        prompt = f"""
当前推理：{thought}

可用工具：
{', '.join(self.config.tools)}

请决定使用哪个工具，以及参数是什么。
格式：
工具名：xxx
参数：{{"key": "value"}}
原因：xxx
"""
        
        try:
            response = self.llm_client.generate(prompt)
            return self._parse_action(response)
        except Exception as e:
            print(f"LLM 决策失败: {e}")
            return {
                "reasoning": "决策失败，使用默认工具",
                "tool": "terminal",
                "args": {"command": "echo 'test'"}
            }
    
    def _execute_tool(self, action: Dict[str, Any]) -> Any:
        """执行工具"""
        if self.tool_executor is None:
            # 降级：返回模拟结果
            return f"模拟执行 {action['tool']}"
        
        try:
            return self.tool_executor(
                action["tool"],
                action["args"]
            )
        except Exception as e:
            return f"工具执行失败: {e}"
    
    def _reflect(self, observation: Any, steps: List[ReActStep]) -> str:
        """反思阶段"""
        if self.llm_client is None:
            # 降级：返回示例反思
            return f"观察到结果：{str(observation)[:50]}...，继续分析"
        
        prompt = f"""
观察结果：{observation}

历史步骤：
{self._format_steps(steps)}

请反思这个结果，思考是否需要继续，或者已经得出结论。
"""
        
        try:
            return self.llm_client.generate(prompt)
        except Exception as e:
            print(f"LLM 反思失败: {e}")
            return "反思失败，继续下一步"
    
    def _is_complete(self, steps: List[ReActStep]) -> bool:
        """检查完成条件"""
        # 简单规则：如果最后一个步骤是反思，且包含"结论"、"完成"等词，则认为完成
        if steps and steps[-1].step_type == "reflection":
            completion_keywords = ["结论", "完成", "得出", "解决"]
            return any(kw in steps[-1].content for kw in completion_keywords)
        return False
    
    def _build_context(self, steps: List[ReActStep]) -> str:
        """构建上下文"""
        context_parts = []
        for step in steps[-5:]:  # 只保留最近 5 步
            context_parts.append(f"{step.step_type}: {step.content[:100]}")
        return "\n".join(context_parts)
    
    def _format_steps(self, steps: List[ReActStep]) -> str:
        """格式化历史步骤"""
        if not steps:
            return "无"
        
        formatted = []
        for i, step in enumerate(steps[-5:], 1):  # 只显示最近 5 步
            formatted.append(f"{i}. [{step.step_type}] {step.content[:100]}")
        return "\n".join(formatted)
    
    def _parse_action(self, response: str) -> Dict[str, Any]:
        """解析 LLM 响应中的行动"""
        lines = response.strip().split('\n')
        
        tool = "terminal"
        args = {}
        reasoning = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith("工具名：") or line.startswith("工具:"):
                tool = line.split("：", 1)[-1].split(":", 1)[-1].strip()
            elif line.startswith("参数：") or line.startswith("参数:"):
                try:
                    args_str = line.split("：", 1)[-1].split(":", 1)[-1].strip()
                    args = json.loads(args_str)
                except:
                    args = {}
            elif line.startswith("原因：") or line.startswith("原因:"):
                reasoning = line.split("：", 1)[-1].split(":", 1)[-1].strip()
        
        return {
            "reasoning": reasoning or f"使用 {tool} 工具",
            "tool": tool,
            "args": args
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计信息"""
        return {
            "max_iterations": self.config.max_iterations,
            "tools_available": len(self.config.tools),
            "auto_reflect": self.config.auto_reflect
        }


# 测试代码
if __name__ == "__main__":
    config = ReActConfig(
        enabled=True,
        max_iterations=5,
        auto_reflect=True
    )
    
    engine = ReActEngine(config)
    steps = engine.run("搜索 deep-thinking 相关论文")
    
    print("ReAct 步骤：")
    for i, step in enumerate(steps, 1):
        print(f"\n步骤 {i}:")
        print(json.dumps(step.to_dict(), indent=2, ensure_ascii=False))
    
    print("\n引擎统计：")
    print(json.dumps(engine.get_stats(), indent=2, ensure_ascii=False))
