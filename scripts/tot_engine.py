"""
Tree of Thoughts (ToT) 多路径探索引擎

参考论文: https://arxiv.org/abs/2305.10601
GitHub: https://github.com/princeton-nlp/tree-of-thought-llm
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
import json


class ThoughtState(Enum):
    """思维节点状态"""
    EXPLORING = "exploring"
    EVALUATED = "evaluated"
    PRUNED = "pruned"
    TERMINAL = "terminal"


@dataclass
class ThoughtNode:
    """思维节点 - ToT 核心数据结构"""
    id: str
    content: str
    depth: int
    score: float = 0.0
    state: ThoughtState = ThoughtState.EXPLORING
    parent_id: Optional[str] = None
    children: List['ThoughtNode'] = field(default_factory=list)
    reasoning_chain: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "id": self.id,
            "content": self.content,
            "depth": self.depth,
            "score": self.score,
            "state": self.state.value,
            "parent_id": self.parent_id,
            "children_count": len(self.children),
            "reasoning_chain": self.reasoning_chain,
            "metadata": self.metadata
        }


@dataclass
class ToTConfig:
    """ToT 配置"""
    enabled: bool = False
    max_depth: int = 3
    max_branches: int = 3
    beam_width: int = 2
    score_threshold: float = 0.8
    exploration_strategy: str = "beam"


class TreeOfThoughtsEngine:
    """ToT 多路径探索引擎"""
    
    def __init__(self, config: ToTConfig, llm_client=None):
        self.config = config
        self.nodes: Dict[str, ThoughtNode] = {}
        self.llm_client = llm_client  # LLM 调用接口
        self.node_counter = 0
        
    def beam_search(self, root_problem: str) -> ThoughtNode:
        """
        束搜索算法
        
        核心流程：
        1. 创建根节点
        2. 迭代生成子节点（LLM）
        3. 评估节点质量（LLM）
        4. 选择 top-k 继续
        5. 检查终止条件
        6. 返回最佳路径
        """
        # Step 1: 创建根节点
        root = ThoughtNode(
            id="root",
            content=root_problem,
            depth=0
        )
        self.nodes["root"] = root
        
        # Step 2: 迭代生成子节点
        current_beam = [root]
        
        for depth in range(self.config.max_depth):
            next_beam = []
            
            for node in current_beam:
                if node.state == ThoughtState.TERMINAL:
                    continue
                
                # 生成子节点（通过 LLM）
                children = self._generate_children(node)
                
                # 评估节点质量（通过 LLM）
                for child in children:
                    child.score = self._evaluate_node(child)
                    
                    # 检查终止条件
                    if child.score >= self.config.score_threshold:
                        child.state = ThoughtState.TERMINAL
                        return child
                
                next_beam.extend(children)
            
            # Step 4: 选择 top-k 继续（束搜索核心）
            next_beam.sort(key=lambda x: x.score, reverse=True)
            current_beam = next_beam[:self.config.beam_width]
        
        # Step 6: 返回最佳节点
        return max(self.nodes.values(), key=lambda x: x.score)
    
    def _generate_children(self, parent: ThoughtNode) -> List[ThoughtNode]:
        """
        生成子节点（通过 LLM）
        
        返回：ThoughtNode 列表
        """
        if self.llm_client is None:
            # 降级：返回示例节点
            return self._generate_mock_children(parent)
        
        # 调用 LLM 生成多个思考方向
        prompt = f"""
问题：{parent.content}

请生成 {self.config.max_branches} 个不同的思考方向或解决方案。
每个方向应该是一个独立的思路，格式如下：
1. [第一个思考方向]
2. [第二个思考方向]
3. [第三个思考方向]
"""
        
        try:
            response = self.llm_client.generate(prompt)
            thoughts = self._parse_thoughts(response)
            
            children = []
            for i, thought in enumerate(thoughts[:self.config.max_branches]):
                self.node_counter += 1
                child = ThoughtNode(
                    id=f"node_{self.node_counter}",
                    content=thought,
                    depth=parent.depth + 1,
                    parent_id=parent.id
                )
                parent.children.append(child)
                self.nodes[child.id] = child
                children.append(child)
            
            return children
        except Exception as e:
            print(f"LLM 调用失败: {e}")
            return self._generate_mock_children(parent)
    
    def _evaluate_node(self, node: ThoughtNode) -> float:
        """
        评估节点质量（通过 LLM）
        
        返回：分数 (0-1)
        """
        if self.llm_client is None:
            # 降级：返回随机分数
            import random
            return random.uniform(0.5, 0.9)
        
        prompt = f"""
思考方向：{node.content}

请评估这个思考方向的质量，给出一个 0-1 的分数。
标准：
- 0.9-1.0：非常优秀，可以直接采用
- 0.7-0.9：较好，值得继续探索
- 0.5-0.7：一般，可以继续优化
- 0.3-0.5：较差，不太可行
- 0.0-0.3：不可行

请只返回分数数字，不要其他内容。
"""
        
        try:
            response = self.llm_client.generate(prompt)
            score = float(response.strip())
            return max(0.0, min(1.0, score))  # 确保在 0-1 范围
        except Exception as e:
            print(f"LLM 评估失败: {e}")
            return 0.5
    
    def _parse_thoughts(self, response: str) -> List[str]:
        """解析 LLM 响应中的思考方向"""
        thoughts = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            # 匹配 "1. xxx" 或 "1) xxx" 或 "- xxx"
            if line and (line[0].isdigit() or line[0] == '-'):
                # 提取内容
                if '. ' in line:
                    thought = line.split('. ', 1)[1]
                elif ') ' in line:
                    thought = line.split(') ', 1)[1]
                elif line.startswith('- '):
                    thought = line[2:]
                else:
                    thought = line
                
                if thought:
                    thoughts.append(thought)
        
        return thoughts
    
    def _generate_mock_children(self, parent: ThoughtNode) -> List[ThoughtNode]:
        """生成模拟子节点（用于测试）"""
        children = []
        for i in range(self.config.max_branches):
            self.node_counter += 1
            thought = f"思考方向 {self.node_counter}：基于 {parent.content[:30]} 的方案"
            child = ThoughtNode(
                id=f"node_{self.node_counter}",
                content=thought,
                depth=parent.depth + 1,
                parent_id=parent.id
            )
            parent.children.append(child)
            self.nodes[child.id] = child
            children.append(child)
        
        return children
    
    def get_tree_stats(self) -> Dict[str, Any]:
        """获取树统计信息"""
        return {
            "total_nodes": len(self.nodes),
            "max_depth": max(n.depth for n in self.nodes.values()) if self.nodes else 0,
            "terminal_nodes": sum(1 for n in self.nodes.values() if n.state == ThoughtState.TERMINAL),
            "pruned_nodes": sum(1 for n in self.nodes.values() if n.state == ThoughtState.PRUNED),
            "avg_score": sum(n.score for n in self.nodes.values()) / len(self.nodes) if self.nodes else 0
        }


# 测试代码
if __name__ == "__main__":
    config = ToTConfig(
        enabled=True,
        max_depth=3,
        max_branches=3,
        beam_width=2,
        score_threshold=0.8
    )
    
    engine = TreeOfThoughtsEngine(config)
    best_node = engine.beam_search("选择最适合的 AI 推理框架")
    
    print("最佳节点：")
    print(json.dumps(best_node.to_dict(), indent=2, ensure_ascii=False))
    print("\n树统计：")
    print(json.dumps(engine.get_tree_stats(), indent=2, ensure_ascii=False))
