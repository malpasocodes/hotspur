# Troubleshooting Guide

This guide covers common issues and their solutions when using the Shakespeare LLM fine-tuning project.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Training Problems](#training-problems)
3. [GPU/CUDA Issues](#gpucuda-issues)
4. [Memory Issues](#memory-issues)
5. [Generation Problems](#generation-problems)
6. [Model Loading Issues](#model-loading-issues)
7. [Data Issues](#data-issues)
8. [Performance Issues](#performance-issues)
9. [Environment Issues](#environment-issues)
10. [Getting Help](#getting-help)

## Installation Issues

### 1. Package Installation Failures

**Problem**: `pip install` fails with error messages
```bash
ERROR: Could not find a version that satisfies the requirement torch>=2.0.0
```

**Solutions**:
```bash
# Update pip first
pip install --upgrade pip

# Use specific PyTorch index
pip install torch --index-url https://download.pytorch.org/whl/cu118

# Install without cache
pip install torch --no-cache-dir

# For older Python versions
pip install torch==1.13.1  # Compatible with Python 3.8+
```

### 2. UV Installation Issues

**Problem**: `uv` command not found
```bash
bash: uv: command not found
```

**Solutions**:
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart terminal or source profile
source ~/.bashrc  # or ~/.zshrc

# Alternative: use pip
pip install uv
```

### 3. Virtual Environment Issues

**Problem**: Wrong Python version or packages not found
```bash
ModuleNotFoundError: No module named 'transformers'
```

**Solutions**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Verify Python version
python --version  # Should be 3.9+

# Reinstall packages in virtual environment
pip install transformers datasets torch accelerate
```

## Training Problems

### 1. Training Crashes

**Problem**: Training stops unexpectedly
```bash
RuntimeError: Expected all tensors to be on the same device
```

**Solutions**:
```python
# Check device consistency
from finetune_shakespeare import ShakespeareFineTuner
import torch

# Explicitly set device
device = "cuda" if torch.cuda.is_available() else "cpu"
fine_tuner = ShakespeareFineTuner(device=device)

# Or use CPU only
fine_tuner = ShakespeareFineTuner(device="cpu")
```

### 2. Training Loss Not Decreasing

**Problem**: Loss stays high or fluctuates wildly

**Solutions**:
```python
# Reduce learning rate
fine_tuner.train(
    learning_rate=1e-5,  # Lower learning rate
    warmup_steps=500,    # More warmup steps
    weight_decay=0.01    # Add regularization
)

# Check data quality
with open("data/processed/shakespeare_only.txt", 'r') as f:
    sample = f.read(1000)
    print(f"Sample data: {sample}")
```

### 3. Training Too Slow

**Problem**: Training takes hours on GPU

**Solutions**:
```python
# Optimize settings
fine_tuner.train(
    per_device_train_batch_size=8,  # Increase batch size
    gradient_accumulation_steps=1,   # Reduce accumulation
    fp16=True,                      # Use mixed precision
    dataloader_num_workers=4,       # Parallel data loading
    max_length=256                  # Shorter sequences
)
```

## GPU/CUDA Issues

### 1. CUDA Out of Memory

**Problem**: 
```bash
RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB
```

**Solutions**:
```python
# Reduce batch size
fine_tuner.train(
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4  # Simulate larger batch
)

# Use gradient checkpointing
fine_tuner.train(
    gradient_checkpointing=True,
    fp16=True  # Use mixed precision
)

# Reduce sequence length
fine_tuner = ShakespeareFineTuner(max_length=256)
```

### 2. CUDA Not Available

**Problem**: GPU not detected
```python
import torch
print(torch.cuda.is_available())  # False
```

**Solutions**:
```bash
# Check GPU
nvidia-smi

# Reinstall PyTorch with CUDA
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cu118

# Verify installation
python -c "import torch; print(torch.cuda.is_available())"
```

### 3. CUDA Version Mismatch

**Problem**: PyTorch CUDA version doesn't match system CUDA
```bash
RuntimeError: The NVIDIA driver on your system is too old
```

**Solutions**:
```bash
# Check CUDA version
nvidia-smi  # Look for CUDA Version

# Install matching PyTorch version
# For CUDA 11.8
pip install torch --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch --index-url https://download.pytorch.org/whl/cu121

# For CPU only
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## Memory Issues

### 1. System RAM Exhausted

**Problem**: System freezes or kills process
```bash
Killed (signal 9)
```

**Solutions**:
```python
# Reduce dataset size
fine_tuner.prepare_dataset(test_size=0.2)  # Use less data

# Use smaller model
fine_tuner = ShakespeareFineTuner(model_name="distilgpt2")

# Reduce sequence length
fine_tuner = ShakespeareFineTuner(max_length=256)

# Enable gradient checkpointing
fine_tuner.train(gradient_checkpointing=True)
```

### 2. Data Loading Memory Issues

**Problem**: High memory usage during data loading
```bash
MemoryError: Unable to allocate array
```

**Solutions**:
```python
# Use streaming dataset
from datasets import load_dataset

# Process data in chunks
fine_tuner.train(
    dataloader_num_workers=1,      # Reduce workers
    per_device_train_batch_size=1, # Smaller batches
    preprocessing_num_workers=1    # Reduce preprocessing workers
)
```

## Generation Problems

### 1. Poor Quality Generation

**Problem**: Generated text is repetitive or nonsensical

**Solutions**:
```python
# Adjust generation parameters
texts = fine_tuner.generate_text(
    prompt="To be or not to be",
    temperature=0.8,              # Try different values (0.7-1.0)
    top_k=50,                     # Limit vocabulary
    top_p=0.95,                   # Nucleus sampling
    repetition_penalty=1.2,       # Penalize repetition
    no_repeat_ngram_size=3        # Prevent n-gram repetition
)

# Train for more epochs
fine_tuner.train(num_train_epochs=5)
```

### 2. Generation Stops Too Early

**Problem**: Generated text is too short

**Solutions**:
```python
# Increase max length
texts = fine_tuner.generate_text(
    prompt="To be or not to be",
    max_length=300,  # Increase length
    min_length=50,   # Set minimum length
    pad_token_id=fine_tuner.tokenizer.eos_token_id
)

# Check tokenizer settings
print(f"EOS token: {fine_tuner.tokenizer.eos_token}")
print(f"EOS token ID: {fine_tuner.tokenizer.eos_token_id}")
```

### 3. Generation Takes Too Long

**Problem**: Text generation is very slow

**Solutions**:
```python
# Optimize generation
texts = fine_tuner.generate_text(
    prompt="To be or not to be",
    max_length=200,     # Shorter length
    num_beams=1,        # Disable beam search
    do_sample=True,     # Use sampling
    early_stopping=True # Stop early if possible
)

# Use smaller model
fine_tuner = ShakespeareFineTuner(model_name="distilgpt2")
```

## Model Loading Issues

### 1. Model Not Found

**Problem**: 
```bash
OSError: shakespeare-distilgpt2 does not appear to be a valid model
```

**Solutions**:
```bash
# Check if model directory exists
ls -la shakespeare-distilgpt2/

# Retrain if missing
python quick_start.py train

# Use specific model path
python quick_start.py generate "prompt" --model-dir /full/path/to/model
```

### 2. Corrupted Model Files

**Problem**: Model loads but produces errors
```bash
RuntimeError: Error(s) in loading state_dict
```

**Solutions**:
```bash
# Remove corrupted model and retrain
rm -rf shakespeare-distilgpt2/
python quick_start.py train

# Check model files
ls -la shakespeare-distilgpt2/
# Should contain: config.json, pytorch_model.bin, tokenizer files
```

### 3. Version Compatibility Issues

**Problem**: Model was trained with different transformers version
```bash
ValueError: Unrecognized configuration class
```

**Solutions**:
```bash
# Update transformers
pip install --upgrade transformers

# Or use specific version
pip install transformers==4.21.0

# Retrain with current version
python quick_start.py train
```

## Data Issues

### 1. Shakespeare Data File Missing

**Problem**: 
```bash
FileNotFoundError: data/processed/shakespeare_only.txt not found
```

**Solutions**:
```bash
# Extract Shakespeare data
python extract_shakespeare.py

# Or manually create directory
mkdir -p data/processed/
# Then copy your text file to data/processed/shakespeare_only.txt
```

### 2. Data Encoding Issues

**Problem**: Text contains unusual characters
```bash
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Solutions**:
```python
# Fix encoding
with open("data/processed/shakespeare_only.txt", 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

# Clean text
import re
text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII

# Save cleaned text
with open("data/processed/shakespeare_only.txt", 'w', encoding='utf-8') as f:
    f.write(text)
```

### 3. Empty or Corrupted Data

**Problem**: Training fails due to empty dataset

**Solutions**:
```bash
# Check file size
wc -l data/processed/shakespeare_only.txt
# Should show ~196,000 lines

# Check file content
head -n 10 data/processed/shakespeare_only.txt

# Re-extract if needed
python extract_shakespeare.py
```

## Performance Issues

### 1. Slow Training on CPU

**Problem**: Training takes hours on CPU

**Solutions**:
```python
# Use smaller model
fine_tuner = ShakespeareFineTuner(model_name="distilgpt2")

# Optimize settings for CPU
fine_tuner.train(
    per_device_train_batch_size=1,
    gradient_accumulation_steps=2,
    dataloader_num_workers=2,
    num_train_epochs=1  # Reduce epochs for testing
)
```

### 2. High Memory Usage

**Problem**: Process uses too much RAM

**Solutions**:
```python
# Monitor memory usage
import psutil
process = psutil.Process()
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB")

# Reduce memory usage
fine_tuner = ShakespeareFineTuner(
    max_length=256,  # Shorter sequences
    overlap_tokens=25  # Less overlap
)
```

## Environment Issues

### 1. Python Version Incompatibility

**Problem**: Features not available in older Python versions

**Solutions**:
```bash
# Check Python version
python --version

# Install compatible Python version
# Use pyenv or conda to manage multiple Python versions
pyenv install 3.10.12
pyenv global 3.10.12

# Or use conda
conda create -n shakespeare python=3.10
conda activate shakespeare
```

### 2. Package Conflicts

**Problem**: Different packages have conflicting dependencies

**Solutions**:
```bash
# Create fresh environment
python -m venv fresh_env
source fresh_env/bin/activate

# Install minimal required packages
pip install torch transformers datasets accelerate

# Or use UV for better dependency resolution
uv sync
```

## Getting Help

### 1. Debugging Steps

Before asking for help, try these debugging steps:

```python
# debug_info.py
import torch
import transformers
import sys
import os

print("=== Debug Information ===")
print(f"Python version: {sys.version}")
print(f"PyTorch version: {torch.__version__}")
print(f"Transformers version: {transformers.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

print(f"Working directory: {os.getcwd()}")
print(f"Shakespeare data exists: {os.path.exists('data/processed/shakespeare_only.txt')}")

# Test basic functionality
try:
    from finetune_shakespeare import ShakespeareFineTuner
    fine_tuner = ShakespeareFineTuner()
    print("✅ ShakespeareFineTuner imports successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
```

### 2. Common Error Messages

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `CUDA out of memory` | GPU memory exhausted | Reduce batch size |
| `Module not found` | Missing dependencies | Check virtual environment |
| `File not found` | Missing data files | Run data extraction |
| `RuntimeError: Expected all tensors to be on the same device` | Device mismatch | Set device explicitly |
| `UnicodeDecodeError` | Text encoding issues | Fix file encoding |
| `ValueError: Unrecognized configuration` | Version mismatch | Update packages |

### 3. Where to Get Help

1. **Check the logs**: Look for detailed error messages
2. **Search existing issues**: Check the GitHub issues page
3. **Create a new issue**: Include:
   - Complete error message
   - Debug information (from script above)
   - Steps to reproduce
   - Your system information

### 4. Minimal Reproducible Example

When reporting issues, provide a minimal example:

```python
# minimal_example.py
from finetune_shakespeare import ShakespeareFineTuner

# This should work
fine_tuner = ShakespeareFineTuner()

# This causes the error
# [Include the specific code that fails]
```

### 5. Community Resources

- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: Check all documentation files
- **Stack Overflow**: Use tags `huggingface`, `transformers`, `pytorch`
- **Discord/Reddit**: ML communities for general help

Remember: The more information you provide, the better help you'll receive!