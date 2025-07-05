#!/usr/bin/env python3
"""
Direct training execution - no fancy stuff
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    from finetune_shakespeare import ShakespeareFineTuner
    
    print("🎭 Starting Shakespeare Training")
    print("Creating trainer...")
    
    trainer = ShakespeareFineTuner(
        model_name="distilgpt2",
        output_dir="shakespeare-distilgpt2",
        max_length=256
    )
    
    print("Starting training...")
    trainer.train(
        num_train_epochs=1,
        per_device_train_batch_size=2,
        learning_rate=3e-5
    )
    
    print("Training complete! Testing generation...")
    result = trainer.generate_text("To be or not to be", max_length=100)
    print(f"Generated: {result[0]}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
