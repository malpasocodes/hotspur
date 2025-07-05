# 🎭 Hotspur: A Shakespeare Expert AI Assistant

A sophisticated language model fine-tuned on Shakespeare's complete works to serve as an expert resource for scholars, students, and enthusiasts of Shakespearean literature.

## 🎯 Project Vision

Hotspur is designed to be more than a text generator - it's an AI-powered Shakespeare expert that can:
- Analyze and discuss Shakespeare's works with deep understanding
- Assist scholars with research and textual analysis
- Help students understand complex passages and themes
- Provide insights into language, style, and historical context
- Support creative projects and educational initiatives

## 📋 Features

- **📚 Comprehensive Knowledge**: Trained on Shakespeare's complete works (196K+ lines)
- **🎓 Scholarly Applications**: Designed for academic research and education
- **💭 Deep Understanding**: Context-aware analysis of themes, language, and style
- **🔍 Textual Analysis**: Help with interpretation and close reading
- **🎨 Creative Support**: Assist with adaptations and creative projects
- **📖 Educational Resource**: Support for students and educators

## 🚀 Quick Start

### Option 1: Search Interface (Immediate Use)

```bash
# Clone repository
git clone https://github.com/yourusername/hotspur.git
cd hotspur

# Setup search component
python hotspur_search/setup_search.py

# Launch search interface
streamlit run hotspur_search/streamlit_app/app.py
```

### Option 2: Train AI Model (Advanced)

```bash
# Install dependencies (recommended)
uv sync

# Quick training (5-15 minutes on GPU)
python quick_start.py train

# Generate text
python quick_start.py generate "To be or not to be"
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[Search Component Guide](hotspur_search/README.md)** | Complete search functionality guide |
| **[Development Log](DEVELOPMENT_LOG.md)** | Detailed implementation history |
| **[Project Vision](HOTSPUR_VISION.md)** | Goals and future roadmap |
| **[Installation Guide](docs/INSTALLATION.md)** | Complete setup instructions |
| **[API Reference](docs/API_REFERENCE.md)** | Detailed API documentation |
| **[Tutorials](docs/TUTORIALS.md)** | Step-by-step examples |
| **[Troubleshooting](docs/TROUBLESHOOTING.md)** | Common issues and solutions |

## 🎯 Model Selection

| Model | Parameters | GPU Memory | Training Time | Quality |
|-------|------------|------------|---------------|---------|
| **DistilGPT-2** | 82M | 4GB | ~15 min | Good |
| **GPT-2** | 124M | 6GB | ~30 min | Better |
| **GPT-2 Medium** | 355M | 10GB | ~90 min | Best |
| **GPT-2 Large** | 774M | 16GB | ~3 hours | Excellent |

## 🔧 Advanced Usage

### Command Line

```bash
# Custom training
python finetune_shakespeare.py \
    --model gpt2-medium \
    --epochs 3 \
    --batch-size 4 \
    --learning-rate 2e-5 \
    --output-dir my-shakespeare-model

# Advanced generation
python finetune_shakespeare.py \
    --generate-only \
    --prompt "Shall I compare thee" \
    --temperature 0.8 \
    --max-length 300
```

### Python API

```python
from finetune_shakespeare import ShakespeareFineTuner

# Initialize and train
fine_tuner = ShakespeareFineTuner(model_name="gpt2")
fine_tuner.train(num_train_epochs=3)

# Generate text
texts = fine_tuner.generate_text(
    "To be or not to be",
    temperature=0.8,
    num_return_sequences=3
)
```

## 📁 Project Structure

```
shakespeare-llm/
├── 🎭 Core Files
│   ├── finetune_shakespeare.py    # Main ShakespeareFineTuner class
│   ├── quick_start.py             # Simple CLI interface
│   └── config.py                  # Model and training configurations
├── 📊 Data
│   ├── raw/shakespeare_complete.txt     # Original Shakespeare text
│   └── processed/shakespeare_only.txt   # Processed text (196K lines)
├── 📖 Documentation
│   ├── docs/INSTALLATION.md       # Setup guide
│   ├── docs/API_REFERENCE.md      # Complete API docs
│   ├── docs/TUTORIALS.md          # Examples and tutorials
│   └── docs/TROUBLESHOOTING.md    # Common issues
├── 🎨 Examples
│   ├── demo.py                    # System verification demo
│   ├── examples.py                # Usage examples
│   ├── main.py                    # Main example script
│   └── simple_train.py            # Simple training example
├── 🔍 Search Component
│   ├── streamlit_app/             # Web search interface
│   ├── utils/                     # Search engine and parser
│   └── setup_search.py            # Search setup script
├── 🛠️ Scripts
│   ├── data/                      # Data processing scripts
│   │   ├── extract_shakespeare.py
│   │   ├── build_vocabulary.py
│   │   └── ...
│   └── utils/                     # Utility scripts
│       ├── diagnose.py
│       ├── monitor_progress.py
│       └── ...
├── 🧪 Tests
│   ├── test_setup.py              # Setup tests
│   ├── test_training.py           # Training tests
│   └── system_test.py             # System integration tests
├── 🤖 Models (created after training)
│   ├── shakespeare-{model}/       # Fine-tuned model outputs
│   └── tokenizers/                # Custom tokenizer models
├── 📚 Archive
│   └── ...                        # Older versions and alternatives
└── ⚙️ Configuration
    ├── pyproject.toml             # Dependencies
    └── uv.lock                    # Locked dependencies
```

## 🔍 Search Capabilities

Hotspur includes a powerful search component that provides immediate value:

### Advanced Text Search
- **Word/phrase search**: Find any word or exact phrase across all works
- **Regular expressions**: Advanced pattern matching for complex queries
- **Fuzzy matching**: Find approximate matches for typos and variations
- **Context-aware results**: See surrounding lines for better understanding

### Scholar-Friendly Features
- **Work filtering**: Search within specific plays or the entire corpus
- **Metadata display**: Act/scene numbers, speakers, line references
- **Export functionality**: Download results as CSV, JSON, or text files
- **Citation-ready format**: Easy copy-paste references for academic use

### Example Searches
```
• "to be or not to be" → Find the famous soliloquy and variations
• "love.*death" → Find lines containing both love and death (regex)
• speaker:Hamlet "crown" → Find Hamlet's mentions of crown
• work:"Romeo and Juliet" "star" → Find star references in Romeo & Juliet
```

**🚀 Try it now**: `python hotspur_search/setup_search.py`

### 🎉 Current Status: **SEARCH COMPONENT COMPLETE & TESTED**
- ✅ **93,812 searchable text segments** across 31 Shakespeare works
- ✅ **Sub-second search performance** with multiple query types
- ✅ **Work-specific filtering** - search within individual plays (bug fixed)
- ✅ **Scholar-friendly features**: citations, exports, metadata
- ✅ **Production-ready interface** with Streamlit web app
- ✅ **User-validated** - real-world testing and bug fixes applied

## 🎓 Use Cases for Scholars and Enthusiasts

### Academic Research
- **Textual Analysis**: Explore language patterns, themes, and stylistic elements
- **Comparative Studies**: Analyze similarities across plays and sonnets
- **Historical Context**: Understand Elizabethan language and cultural references
- **Character Analysis**: Deep dive into character motivations and development

### Educational Applications
- **Student Support**: Help understand difficult passages and archaic language
- **Teaching Aid**: Generate explanations and discussion prompts
- **Essay Assistance**: Provide insights for literary analysis papers
- **Language Learning**: Study Early Modern English patterns

### Creative Projects
- **Adaptation Support**: Help modernize or adapt Shakespeare's works
- **Performance Notes**: Insights for actors and directors
- **Creative Writing**: Inspiration for Shakespeare-influenced works

## 💡 Example Interactions

**Scholarly Analysis**:
```
Query: "Analyze the use of madness in Hamlet"
Hotspur: "Madness serves as both a strategic device and thematic element in Hamlet. 
The prince's 'antic disposition' allows him to speak truth through seeming folly..."
```

**Educational Support**:
```
Query: "Explain 'To be or not to be' for a high school student"
Hotspur: "This soliloquy explores Hamlet's contemplation of life versus death. 
He weighs the pain of existence against the uncertainty of what comes after..."
```

**Creative Assistance**:
```
Query: "How might Lady Macbeth's sleepwalking scene be staged?"
Hotspur: "The sleepwalking scene reveals Lady Macbeth's psychological unraveling. 
Consider staging that emphasizes her isolation and the weight of guilt..."
```

## 💡 Tips for Best Results

### 🎯 Model Selection
- **Beginners**: Start with `distilgpt2` (fastest training)
- **Quality**: Use `gpt2-medium` for better results
- **Production**: Use `gpt2-large` for highest quality

### ⚡ Training Settings
- **Quick test**: 1 epoch, batch size 2
- **Development**: 2-3 epochs, batch size 4
- **Production**: 3-5 epochs, batch size 8+

### 🎨 Generation Tips
- **Conservative**: Temperature 0.7, top_k=40
- **Balanced**: Temperature 0.8, top_k=50 (default)
- **Creative**: Temperature 1.0, top_k=100

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| **CUDA out of memory** | Reduce batch size: `--batch-size 1` |
| **Poor text quality** | Train longer: `--epochs 5` |
| **Slow training** | Use GPU or smaller model |
| **Import errors** | Check virtual environment activation |

See [Troubleshooting Guide](docs/TROUBLESHOOTING.md) for detailed solutions.

## 🌟 Project Status

- ✅ **Fully Implemented**: Complete training and generation pipeline
- ✅ **Production Ready**: Error handling, logging, and monitoring
- ✅ **Well Documented**: Comprehensive guides and API documentation
- ✅ **Tested**: Verified on multiple systems and GPU configurations

## 🤝 Contributing

Contributions welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes. Shakespeare's works are in the public domain.

## 🔗 Links

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/shakespeare-llm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/shakespeare-llm/discussions)

---

*"I will speak daggers to her, but use none" - Hamlet*

**Hotspur**: Named after the fierce and eloquent Henry "Hotspur" Percy from Henry IV, Part 1 - a character known for his passionate speech and noble spirit.