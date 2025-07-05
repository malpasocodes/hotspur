#!/usr/bin/env python3
"""
Simple demo script to show how the Shakespeare LLM fine-tuning works.
This runs a minimal example to demonstrate the capabilities.
"""

import os
import sys

def main():
    print("🎭 Shakespeare LLM Fine-tuning Demo")
    print("="*50)
    
    # Check if Shakespeare data exists
    shakespeare_file = "data/processed/shakespeare_only.txt"
    if not os.path.exists(shakespeare_file):
        print(f"❌ Shakespeare data not found at {shakespeare_file}")
        print("Please ensure you have the Shakespeare text file in the correct location.")
        return
    
    # Check file size
    with open(shakespeare_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"✅ Shakespeare data loaded: {len(content):,} characters")
    print(f"📖 Sample text: {content[:200]}...")
    
    print("\n🚀 Ready for fine-tuning!")
    print("\nNext steps:")
    print("1. Train a model:")
    print("   uv run python finetune_shakespeare.py --epochs 2 --batch-size 2")
    print("\n2. Or use the quick interface:")
    print("   uv run python quick_start.py train")
    print("\n3. Generate text after training:")
    print("   uv run python quick_start.py generate 'To be or not to be'")
    
    print(f"\n📊 Available models:")
    models = ["distilgpt2", "gpt2", "gpt2-medium"]
    for model in models:
        print(f"   - {model}")
    
    print(f"\n💡 For quick testing, use: distilgpt2")
    print(f"💡 For better quality, use: gpt2 or gpt2-medium")

if __name__ == "__main__":
    main()
