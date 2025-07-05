#!/usr/bin/env python3
"""
Test script to verify the Shakespeare fine-tuning setup works correctly.
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def test_setup():
    """Test that all components are working."""
    print("🎭 Testing Shakespeare LLM Setup")
    print("="*50)
    
    # Check if Shakespeare data exists
    shakespeare_file = "data/processed/shakespeare_only.txt"
    if os.path.exists(shakespeare_file):
        with open(shakespeare_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ Shakespeare data found: {len(content):,} characters")
        print(f"📖 First 100 chars: {content[:100]}...")
    else:
        print(f"❌ Shakespeare data not found at {shakespeare_file}")
        return False
    
    # Test PyTorch
    print(f"🔥 PyTorch version: {torch.__version__}")
    print(f"🖥️  CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
        print(f"💾 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    
    # Test Transformers
    try:
        print("🤗 Testing Hugging Face Transformers...")
        tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        model = AutoModelForCausalLM.from_pretrained("distilgpt2")
        
        # Test tokenization
        test_text = "To be or not to be, that is the question"
        tokens = tokenizer.encode(test_text)
        print(f"✅ Tokenization works: '{test_text}' -> {len(tokens)} tokens")
        
        # Test model forward pass
        with torch.no_grad():
            input_ids = torch.tensor([tokens])
            outputs = model(input_ids)
            logits = outputs.logits
        print(f"✅ Model forward pass works: output shape {logits.shape}")
        
        print("✅ All tests passed! Ready for Shakespeare fine-tuning!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing transformers: {e}")
        return False

def quick_generation_test():
    """Test basic text generation."""
    print("\n🎪 Testing text generation...")
    
    try:
        from transformers import pipeline
        
        generator = pipeline("text-generation", model="distilgpt2", max_length=50)
        result = generator("To be or not to be", do_sample=True, temperature=0.8)
        
        print("✅ Generation test successful!")
        print(f"📝 Generated: {result[0]['generated_text']}")
        return True
        
    except Exception as e:
        print(f"❌ Generation test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_setup()
    if success:
        quick_generation_test()
        print("\n🎉 Setup is working perfectly!")
        print("🚀 You can now run:")
        print("   python quick_start.py train")
        print("   python quick_start.py generate 'your prompt'")
    else:
        print("\n❌ Setup incomplete. Please check the errors above.")
