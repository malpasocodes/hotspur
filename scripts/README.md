# Scripts Directory

This directory contains utility scripts for data processing, system diagnostics, and other development tools.

## Directory Structure

### `data/`
Data processing and preparation scripts:
- `extract_shakespeare.py` - Extract Shakespeare text from Project Gutenberg
- `build_vocabulary.py` - Build vocabulary from text
- `clean_sonnets.py` - Clean and process sonnets
- `create_*.py` - Various vocabulary creation scripts
- `standard_tokenizer.py` - Standard tokenization
- `sentence_piece.py` - SentencePiece tokenization
- `llama_tokenize.py` - LLaMA tokenization
- `split_content.py` - Content splitting utilities

### `utils/`
Utility and diagnostic scripts:
- `diagnose.py` - System diagnostics and resource checking
- `monitor_progress.py` - Real-time training monitoring
- `monitor_training.py` - Training progress monitoring
- `explore_file.py` - File content exploration
- `find_*.py` - Various file search utilities
- `restart_training.py` - Training restart utilities
- `run_training.py` - Training execution utilities

## Usage

These scripts are primarily for development and data preparation. Most users should use the main interface (`quick_start.py`) instead.

### Running Data Processing Scripts

```bash
# Extract Shakespeare data
python scripts/data/extract_shakespeare.py

# Build vocabulary
python scripts/data/build_vocabulary.py

# Tokenize with SentencePiece
python scripts/data/sentence_piece.py
```

### Running Utility Scripts

```bash
# System diagnostics
python scripts/utils/diagnose.py

# Monitor training progress
python scripts/utils/monitor_progress.py

# Explore file content
python scripts/utils/explore_file.py
```

## Note

These scripts were created during development and may require updates to work with the current project structure. Use with caution and check file paths before running.