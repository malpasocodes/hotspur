#!/usr/bin/env python3
"""
Step-by-step test of the Shakespeare LLM system.
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__}")
        print(f"   CUDA available: {torch.cuda.is_available()}")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        print("✅ Transformers library")
    except ImportError as e:
        print(f"❌ Transformers import failed: {e}")
        return False
    
    try:
        from datasets import Dataset
        print("✅ Datasets library")
    except ImportError as e:
        print(f"❌ Datasets import failed: {e}")
        return False
    
    try:
        from finetune_shakespeare import ShakespeareFineTuner
        print("✅ ShakespeareFineTuner class")
    except ImportError as e:
        print(f"❌ ShakespeareFineTuner import failed: {e}")
        return False
    
    return True

def test_data():
    """Test if Shakespeare data file exists and is readable."""
    print("\n📚 Testing data file...")
    
    data_file = "data/processed/shakespeare_only.txt"
    
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        return False
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ Data file loaded: {len(content)} characters")
        print(f"   Preview: {content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error reading data file: {e}")
        return False

def test_model_initialization():
    """Test if we can initialize the model."""
    print("\n🤖 Testing model initialization...")
    
    try:
        from finetune_shakespeare import ShakespeareFineTuner
        
        fine_tuner = ShakespeareFineTuner(
            model_name="distilgpt2",
            output_dir="test-output",
            max_length=128
        )
        
        print("✅ ShakespeareFineTuner initialized")
        
        # Test data loading
        segments = fine_tuner.load_and_prepare_data()
        print(f"✅ Data segments created: {len(segments)}")
        
        # Test model setup
        fine_tuner.setup_model_and_tokenizer()
        print("✅ Model and tokenizer loaded")
        
        return True
        
    except Exception as e:
        print(f"❌ Model initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🎭 Shakespeare LLM System Test")
    print("=" * 50)
    
    success = True
    
    success &= test_imports()
    success &= test_data()
    success &= test_model_initialization()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! System is ready for training.")
        print("\nNext steps:")
        print("  1. Run: uv run python quick_start.py train")
        print("  2. Wait for training to complete")
        print("  3. Run: uv run python quick_start.py generate 'your prompt'")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
