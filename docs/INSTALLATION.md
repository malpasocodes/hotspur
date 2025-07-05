# Installation Guide

## System Requirements

### Minimum Requirements
- Python 3.9 or higher
- 8GB RAM
- 10GB free disk space
- CPU with AVX support (most modern processors)

### Recommended Requirements
- Python 3.10+
- 16GB RAM
- NVIDIA GPU with 4GB+ VRAM (for faster training)
- 20GB free disk space
- CUDA 11.8 or higher (for GPU support)

## Installation Methods

### Method 1: Using UV (Recommended)

UV is a fast Python package manager that handles dependencies efficiently.

#### Step 1: Install UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

#### Step 2: Clone the Repository

```bash
git clone https://github.com/yourusername/shakespeare-llm.git
cd shakespeare-llm
```

#### Step 3: Install Dependencies

```bash
# This will create a virtual environment and install all dependencies
uv sync

# Activate the environment (if needed)
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

### Method 2: Using Pip

#### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/shakespeare-llm.git
cd shakespeare-llm
```

#### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

#### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install PyTorch (CPU version)
pip install torch

# Or install PyTorch with CUDA support (for NVIDIA GPUs)
# For CUDA 11.8
pip install torch --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch --index-url https://download.pytorch.org/whl/cu121

# Install other dependencies
pip install transformers datasets accelerate tokenizers numpy tqdm sentencepiece
```

### Method 3: Using Conda

#### Step 1: Create Conda Environment

```bash
conda create -n shakespeare-llm python=3.10
conda activate shakespeare-llm
```

#### Step 2: Install PyTorch

```bash
# CPU version
conda install pytorch cpuonly -c pytorch

# GPU version (CUDA 11.8)
conda install pytorch pytorch-cuda=11.8 -c pytorch -c nvidia

# GPU version (CUDA 12.1)
conda install pytorch pytorch-cuda=12.1 -c pytorch -c nvidia
```

#### Step 3: Install Other Dependencies

```bash
pip install transformers datasets accelerate tokenizers numpy tqdm sentencepiece
```

## GPU Setup (Optional but Recommended)

### NVIDIA GPU Setup

1. **Check GPU Compatibility**
   ```bash
   # Check if NVIDIA GPU is detected
   nvidia-smi
   ```

2. **Install CUDA Toolkit** (if not already installed)
   - Download from [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
   - Choose your OS and follow installation instructions

3. **Verify PyTorch GPU Support**
   ```python
   import torch
   print(torch.cuda.is_available())  # Should return True
   print(torch.cuda.get_device_name(0))  # Should show your GPU name
   ```

### AMD GPU Setup (ROCm)

1. **Install ROCm** (Linux only)
   - Follow instructions at [AMD ROCm](https://docs.amd.com/en/latest/deploy/linux/quick_start.html)

2. **Install PyTorch for ROCm**
   ```bash
   pip install torch --index-url https://download.pytorch.org/whl/rocm5.7
   ```

### Apple Silicon (M1/M2/M3) Setup

PyTorch supports Apple Silicon natively:

```bash
# Install PyTorch with MPS (Metal Performance Shaders) support
pip install torch
```

Verify MPS support:
```python
import torch
print(torch.backends.mps.is_available())  # Should return True
```

## Data Setup

The Shakespeare text data is included in the repository, but you can also set it up manually:

### Using Included Data

The processed Shakespeare text is already in `data/processed/shakespeare_only.txt`.

### Processing Your Own Data

If you want to use different text:

```bash
# Extract Shakespeare from Project Gutenberg file
python extract_shakespeare.py

# Or use your own text file
cp your_text_file.txt data/processed/shakespeare_only.txt
```

## Verification

### 1. Run System Check

```bash
python demo.py
```

This will verify:
- Python version
- Package installations
- GPU availability
- Data file presence
- Model accessibility

### 2. Test Installation

```python
# Quick test script
from finetune_shakespeare import ShakespeareFineTuner

# This should initialize without errors
fine_tuner = ShakespeareFineTuner()
print("✅ Installation successful!")
```

### 3. Run a Quick Training Test

```bash
# Run 10 training steps as a test
python quick_start.py train --epochs 0.001
```

## Troubleshooting Installation

### Common Issues

#### 1. **CUDA/GPU Not Detected**

```bash
# Check PyTorch installation
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Reinstall PyTorch with correct CUDA version
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

#### 2. **Module Not Found Errors**

```bash
# Ensure you're in the virtual environment
which python  # Should show .venv/bin/python

# Reinstall all dependencies
pip install -r requirements.txt
```

#### 3. **Memory Errors During Installation**

```bash
# Install packages one by one
pip install torch --no-cache-dir
pip install transformers --no-cache-dir
pip install datasets --no-cache-dir
```

#### 4. **SSL/Certificate Errors**

```bash
# Use trusted host
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <package_name>
```

#### 5. **Disk Space Issues**

The installation requires:
- ~5GB for PyTorch
- ~2GB for model downloads
- ~1GB for other dependencies
- ~2GB for training outputs

Ensure you have at least 10GB free space.

## Environment Variables

You can set these optional environment variables:

```bash
# Set cache directory for Hugging Face models
export HF_HOME=/path/to/cache

# Disable telemetry
export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

# Set CUDA visible devices
export CUDA_VISIBLE_DEVICES=0  # Use first GPU only
```

## Docker Setup (Alternative)

### Using Pre-built Image

```bash
# Pull and run the Docker image
docker pull yourusername/shakespeare-llm
docker run -it --gpus all yourusername/shakespeare-llm
```

### Building from Dockerfile

Create a `Dockerfile`:

```dockerfile
FROM pytorch/pytorch:2.0.0-cuda11.8-cudnn8-runtime

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "quick_start.py", "demo"]
```

Build and run:
```bash
docker build -t shakespeare-llm .
docker run -it --gpus all shakespeare-llm
```

## Next Steps

After successful installation:

1. **Read the [Quick Start Guide](../README.md#quick-start)**
2. **Try the demo**: `python quick_start.py demo`
3. **Start training**: `python quick_start.py train`
4. **Explore the [API Reference](API_REFERENCE.md)**

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Search existing [GitHub Issues](https://github.com/yourusername/shakespeare-llm/issues)
3. Create a new issue with:
   - Your system information (OS, Python version, GPU)
   - Complete error message
   - Steps to reproduce