#!/usr/bin/env python3
"""
Diagnostic script to check system resources and potential issues
"""

import os
import sys
import psutil
import torch
import subprocess

def check_system_resources():
    """Check system resources and potential bottlenecks."""
    print("🔍 System Diagnostics")
    print("=" * 50)
    
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_percent}%")
    
    # Memory usage
    memory = psutil.virtual_memory()
    print(f"Memory Usage: {memory.percent}% ({memory.used / (1024**3):.1f}GB / {memory.total / (1024**3):.1f}GB)")
    
    # Disk space
    disk = psutil.disk_usage('/')
    print(f"Disk Usage: {disk.percent}% ({disk.free / (1024**3):.1f}GB free)")
    
    # Check if any Python processes are running
    python_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                if proc.info['cmdline'] and any('shakespeare' in arg.lower() for arg in proc.info['cmdline']):
                    python_processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if python_processes:
        print(f"\n🐍 Python processes found: {len(python_processes)}")
        for proc in python_processes:
            print(f"   PID {proc['pid']}: {' '.join(proc['cmdline'])}")
    else:
        print("\n🐍 No Shakespeare-related Python processes found")
    
    return len(python_processes) > 0

def check_pytorch_setup():
    """Check PyTorch configuration and CUDA availability."""
    print("\n🔥 PyTorch Configuration")
    print("=" * 50)
    
    print(f"PyTorch Version: {torch.__version__}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"GPU Count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            gpu_name = torch.cuda.get_device_name(i)
            memory_total = torch.cuda.get_device_properties(i).total_memory / (1024**3)
            print(f"GPU {i}: {gpu_name} ({memory_total:.1f}GB)")
    else:
        print("Running on CPU (this is normal and expected)")

def check_huggingface_cache():
    """Check Hugging Face cache and model downloads."""
    print("\n🤗 Hugging Face Cache")
    print("=" * 50)
    
    cache_dir = os.path.expanduser("~/.cache/huggingface")
    if os.path.exists(cache_dir):
        # Check transformers cache
        transformers_cache = os.path.join(cache_dir, "transformers")
        if os.path.exists(transformers_cache):
            cache_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                           for dirpath, dirnames, filenames in os.walk(transformers_cache)
                           for filename in filenames) / (1024**2)
            print(f"Transformers cache: {cache_size:.1f}MB")
            
            # Check for DistilGPT-2
            distilgpt2_dirs = [d for d in os.listdir(transformers_cache) if 'distilgpt2' in d.lower()]
            if distilgpt2_dirs:
                print(f"DistilGPT-2 found in cache: {distilgpt2_dirs}")
            else:
                print("DistilGPT-2 not found in cache (will need to download)")
        else:
            print("No transformers cache found")
    else:
        print("No Hugging Face cache directory found")

def test_model_loading():
    """Test if we can load the model quickly."""
    print("\n🤖 Model Loading Test")
    print("=" * 50)
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import time
        
        print("Testing tokenizer loading...")
        start_time = time.time()
        tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        tokenizer_time = time.time() - start_time
        print(f"✅ Tokenizer loaded in {tokenizer_time:.2f} seconds")
        
        print("Testing model loading...")
        start_time = time.time()
        model = AutoModelForCausalLM.from_pretrained(
            "distilgpt2",
            torch_dtype=torch.float32  # Force float32 for compatibility
        )
        model_time = time.time() - start_time
        print(f"✅ Model loaded in {model_time:.2f} seconds")
        
        print(f"Model parameters: {model.num_parameters():,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def main():
    """Run all diagnostics."""
    print("🎭 Shakespeare LLM Diagnostics")
    print("=" * 60)
    
    has_running_process = check_system_resources()
    check_pytorch_setup()
    check_huggingface_cache()
    
    if not has_running_process:
        print("\n" + "=" * 60)
        print("🔧 DIAGNOSIS: No training process found running")
        print("This suggests the training may have:")
        print("1. Completed (check for model directory)")
        print("2. Failed/crashed silently")
        print("3. Been interrupted")
        print("\nRecommendation: Restart training with verbose output")
        
        model_works = test_model_loading()
        if model_works:
            print("\n✅ Model loading works fine - safe to restart training")
        else:
            print("\n❌ Model loading has issues - may need troubleshooting")
    else:
        print("\n" + "=" * 60)
        print("🔧 DIAGNOSIS: Training process is still running")
        print("The process may be:")
        print("1. Downloading model files (first time)")
        print("2. Processing large dataset")
        print("3. Stuck in a loop")
        print("\nRecommendation: Wait a bit longer or restart if needed")

if __name__ == "__main__":
    main()
