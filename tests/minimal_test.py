#!/usr/bin/env python3
"""
Minimal test to verify everything is working before full training
"""

import torch
import sys
from transformers import AutoTokenizer, AutoModelForCausalLM

def test_setup():
    print("🔍 Testing setup...")
    print(f"Python version: {sys.version}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA device: {torch.cuda.get_device_name()}")
        print(f"CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    
    return True

def test_model_loading():
    print("\n📥 Testing model loading...")
    try:
        tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        model = AutoModelForCausalLM.from_pretrained("distilgpt2")
        print("✅ Model loaded successfully!")
        
        # Quick test
        inputs = tokenizer("Hello world", return_tensors="pt")
        outputs = model(**inputs)
        print("✅ Model inference works!")
        return True
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_data():
    print("\n📚 Testing data loading...")
    try:
        with open("data/processed/shakespeare_only.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        print(f"✅ Loaded {len(lines)} lines of Shakespeare text")
        print(f"Sample: {lines[100][:100]}...")
        return True
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

if __name__ == "__main__":
    print("🎭 Shakespeare LLM - Minimal Test")
    print("=" * 50)
    
    setup_ok = test_setup()
    model_ok = test_model_loading()
    data_ok = test_data()
    
    if setup_ok and model_ok and data_ok:
        print("\n✅ All tests passed! Ready for training.")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
