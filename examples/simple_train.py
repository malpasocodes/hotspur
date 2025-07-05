#!/usr/bin/env python3
"""
Super simple training script to get things working
"""

from finetune_shakespeare import ShakespeareFineTuner
import logging

# Simple logging
logging.basicConfig(level=logging.INFO)

def simple_train():
    print("🎭 Starting Simple Shakespeare Training")
    print("This will use minimal settings to avoid hanging...")
    
    # Create trainer with very safe settings
    trainer = ShakespeareFineTuner(
        model_name="distilgpt2",
        output_dir="shakespeare-simple",
        max_length=128  # Very small context
    )
    
    # Minimal training
    trainer.train(
        num_train_epochs=1,
        per_device_train_batch_size=1,
        learning_rate=5e-5,
        warmup_steps=5,
        logging_steps=1,
        save_steps=25
    )
    
    # Test generation
    text = trainer.generate_text("To be", max_length=50)
    print(f"\nGenerated: {text[0]}")

if __name__ == "__main__":
    simple_train()
