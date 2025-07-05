#!/usr/bin/env python3
"""
Real-time training monitor for Shakespeare LLM
"""

import os
import time
import json
from datetime import datetime

def check_training_progress():
    """Monitor the training progress and provide status updates."""
    
    print("🎭 Shakespeare LLM Training Monitor")
    print("=" * 50)
    print(f"⏰ Started monitoring at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    model_dir = "shakespeare-distilgpt2"
    
    while True:
        # Check if model directory exists
        if os.path.exists(model_dir):
            print(f"✅ Model directory created: {model_dir}/")
            
            # Check for training files
            files = os.listdir(model_dir)
            
            if "training_info.json" in files:
                print("🎉 Training completed!")
                
                # Read training info
                with open(os.path.join(model_dir, "training_info.json"), 'r') as f:
                    info = json.load(f)
                
                print("\n📊 Training Summary:")
                print(f"   Base Model: {info.get('base_model', 'N/A')}")
                print(f"   Epochs: {info.get('num_epochs', 'N/A')}")
                print(f"   Learning Rate: {info.get('learning_rate', 'N/A')}")
                print(f"   Training Samples: {info.get('train_samples', 'N/A')}")
                print(f"   Validation Samples: {info.get('eval_samples', 'N/A')}")
                
                print("\n✅ Model files created:")
                for file in sorted(files):
                    size = os.path.getsize(os.path.join(model_dir, file))
                    size_mb = size / (1024 * 1024)
                    print(f"   📄 {file} ({size_mb:.1f} MB)")
                
                print("\n🎪 Ready for text generation!")
                print("   Try: uv run python quick_start.py generate 'To be or not to be'")
                break
                
            elif "config.json" in files:
                print("🔄 Training in progress...")
                print(f"   Files created: {len(files)}")
                for file in files:
                    print(f"   📄 {file}")
                    
            else:
                print("🔄 Training starting...")
                
        else:
            print("⏳ Waiting for training to begin...")
            print("   (Loading data and initializing model...)")
        
        print(f"   ⏰ {datetime.now().strftime('%H:%M:%S')} - Checking again in 30 seconds...")
        print()
        
        time.sleep(30)

if __name__ == "__main__":
    try:
        check_training_progress()
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Error during monitoring: {e}")
