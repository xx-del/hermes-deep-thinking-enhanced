# Hermes Deep Thinking Enhanced

Enhanced Deep Thinking Skill for Hermes Agent with ReAct + ToT + Deep Thinking integration.

## 🚀 Features

### Core Enhancements

- **ReAct Engine**: Automatic information gathering with reasoning-action-observation-reflection loop
- **ToT Engine**: Tree of Thoughts for multi-path exploration and structured reasoning
- **Deep Thinking Phase 7**: True knowledge synthesis with LLM-powered conclusion formation

### Performance Improvements

| Dimension | Original | Enhanced | Improvement |
|-----------|----------|----------|-------------|
| Reflection Count | 2-3 | 5+ | +67% to +150% |
| Multi-path Exploration | Single | Tree-structured | Structured |
| Token Efficiency | Baseline | -65% (Phase 7) | Optimized |
| Automation | Manual | Automatic | Fully automated |

### L2 Workflow Optimization

| Metric | Original L2 | Enhanced L2 | Improvement |
|--------|-------------|-------------|-------------|
| Steps | 4 | 2 | -50% |
| Skill Calls | 2 | 1 | -50% |
| Interactions | 3-4 | 1 | -75% |
| Information Gathering | Manual | Automatic (ReAct) | Fully automated |

## 📦 Installation

### Prerequisites

- Hermes Agent installed
- Python 3.8+
- LLM API access (OpenAI, Anthropic, etc.)

### Install

1. Clone this repository:
```bash
git clone https://github.com/xx-del/hermes-deep-thinking-enhanced.git
cd hermes-deep-thinking-enhanced
```

2. Copy to Hermes skills directory:
```bash
cp -r . ~/.hermes/skills/openclaw-imports/deep-thinking/
```

3. Configure in Hermes config:
```yaml
# ~/.hermes/config.yaml
skills:
  - openclaw-imports/deep-thinking
```

## 🔧 Configuration

Edit `config/default_config.yaml`:

### Enable ToT (Multi-path Exploration)

```yaml
deep_thinking:
  enhanced:
    tot_enabled: true
    tot_config:
      max_depth: 3
      max_branches: 3
      beam_width: 2
```

### Enable ReAct (Automatic Tool Calling)

```yaml
deep_thinking:
  enhanced:
    react_enabled: true
    react_config:
      max_iterations: 5
      auto_reflect: true
```

### Strongest Mode (ToT + ReAct)

```yaml
deep_thinking:
  enhanced:
    tot_enabled: true
    react_enabled: true
```

## 📖 Usage

### CLI Usage

```bash
cd scripts
python enhanced_thinking.py "Your complex question here"
```

### Code Usage

```python
from enhanced_thinking import EnhancedDeepThinking

# Create instance
thinker = EnhancedDeepThinking()

# Enable enhancements
thinker.config["deep_thinking"]["enhanced"]["tot_enabled"] = True
thinker.config["deep_thinking"]["enhanced"]["react_enabled"] = True

# Execute
result = thinker.think("Analyze the trade-offs between microservices and monolithic architecture")
```

### Integration with Hermes

The skill automatically integrates with Hermes Agent's L2 thinking tasks. When a user asks for analysis or planning, Hermes will automatically call this enhanced deep-thinking skill.

## 🧪 Testing

Run the test suite:

```bash
cd scripts
python test_enhanced_thinking.py
```

### Test Scenarios

1. **Information-intensive tasks**: Compare ReAct enabled vs disabled
2. **Complex decision tasks**: Compare ToT enabled vs disabled
3. **Strongest mode**: ToT + ReAct + Deep Thinking all enabled

## 📚 Documentation

- [SKILL.md](./SKILL.md): Complete skill documentation
- [references/design.md](./references/design.md): Architecture design
- [references/examples.md](./references/examples.md): Usage examples
- [references/reasoning-frameworks.md](./references/reasoning-frameworks.md): ToT/ReAct frameworks comparison
- [references/phase7-deep-thinking-implementation-20260605.md](./references/phase7-deep-thinking-implementation-20260605.md): Phase 7 implementation details

## 🏗️ Architecture

```
Enhanced Deep Thinking
├── Phase 1: Initial Engagement
├── Phase 2: Search for Solutions ← ReAct Engine (Automatic)
├── Phase 3: Problem Decomposition
├── Phase 4: Multiple Hypotheses ← ToT Engine (Multi-path)
├── Phase 5: Natural Discovery
├── Phase 6: Verification
└── Phase 7: Knowledge Synthesis ← Deep Thinking (LLM-powered)
```

### Three-Layer Architecture

1. **Methodology Layer**: Deep-thinking 7-phase flow (unchanged)
2. **Technical Enhancement Layer**: ToT (Phase 4) + ReAct (Phase 2) - Optional
3. **Infrastructure Layer**: Hermes tool ecosystem

## ⚠️ Important Notes

### Token Consumption

- Enhanced mode may consume 5-8x more tokens than original
- Phase 7 prompt optimized to save 65% tokens
- Use for complex tasks that warrant the cost

### Backward Compatibility

- Default: Enhancements disabled, behaves identically to original
- Configuration-driven: Optional enable
- Preserves organic thinking, not mechanical execution

### Limitations

- Requires LLM API access for full functionality
- Works in degraded mode without LLM client
- Token costs higher for complex reasoning tasks

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- Original deep-thinking skill by Hermes Agent
- ReAct framework by Yao et al.
- Tree of Thoughts by Yao et al.
- Hermes Agent community

## 📊 Changelog

### v1.0.0 (2026-06-05)

- Initial release
- ReAct engine integration
- ToT engine integration
- Phase 7 Deep Thinking implementation
- Token optimization (65% reduction)
- Complete test suite
- Documentation

---

**Maintainer**: xx-del  
**Repository**: https://github.com/xx-del/hermes-deep-thinking-enhanced  
**Issues**: https://github.com/xx-del/hermes-deep-thinking-enhanced/issues
