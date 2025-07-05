#!/usr/bin/env python3
"""
Quick restart of Shakespeare training with safer settings
"""

from finetune_shakespeare import ShakespeareFineTuner
import logging
import sys

# Set up detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('training.log')
    ]
)

def safe_training():
    """Run training with very safe settings to avoid hanging."""
    
    print("🎭 Starting Shakespeare Training - Safe Mode")
    print("=" * 60)
    
    # Initialize with conservative settings
    fine_tuner = ShakespeareFineTuner(
        model_name="distilgpt2",
        output_dir="shakespeare-distilgpt2-safe",
        max_length=256  # Smaller to reduce memory usage
    )
    
    print("✅ Fine-tuner initialized")
    print("🔧 Starting training with minimal settings...")
    
    try:
        # Very conservative training settings
        fine_tuner.train(
            num_train_epochs=1,              # Just 1 epoch for testing
            per_device_train_batch_size=1,   # Smallest possible batch
            learning_rate=3e-5,
            warmup_steps=10,                 # Minimal warmup
            logging_steps=5,                 # Frequent logging
            save_steps=50,
            eval_steps=50,
            save_total_limit=2
        )
        
        print("🎉 Training completed!")
        print(f"📁 Model saved to: shakespeare-distilgpt2-safe/")
        
        # Test generation
        print("🎪 Testing text generation...")
        generated = fine_tuner.generate_text(
            prompt="To be or not to be",
            max_length=100,
            num_return_sequences=1
        )
        
        print("\n" + "="*50)
        print("🎭 GENERATED TEXT:")
        print("="*50)
        print(generated[0])
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = safe_training()
    if success:
        print("\n✅ Safe training completed! You can now try full training.")
    else:
        print("\n❌ Issues encountered. Check the error messages above.")
