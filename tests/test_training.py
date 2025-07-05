#!/usr/bin/env python3
"""
Quick test of the Shakespeare fine-tuner with minimal training.
"""

from finetune_shakespeare import ShakespeareFineTuner
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def quick_test():
    """Test the system with minimal training."""
    print("🎭 Quick Shakespeare LLM Test")
    print("=" * 50)
    
    # Initialize with very conservative settings
    fine_tuner = ShakespeareFineTuner(
        model_name="distilgpt2",
        output_dir="test-shakespeare-model",
        max_length=256  # Smaller for faster testing
    )
    
    print("✅ Fine-tuner initialized")
    
    # Test data loading
    try:
        segments = fine_tuner.load_and_prepare_data()
        print(f"📚 Loaded {len(segments)} text segments")
        print(f"📝 Sample segment preview: {segments[0][:100]}...")
        
        # Test tokenizer setup
        fine_tuner.setup_model_and_tokenizer()
        print("🔤 Tokenizer and model loaded successfully")
        
        # Test quick training (1 epoch, very small batch)
        print("🚀 Starting minimal training (1 epoch for testing)...")
        fine_tuner.train(
            num_train_epochs=1,
            per_device_train_batch_size=1,  # Very small batch
            learning_rate=5e-5,
            logging_steps=5,
            save_steps=50,
            eval_steps=50
        )
        
        print("✅ Training completed!")
        
        # Test text generation
        print("🎪 Testing text generation...")
        generated = fine_tuner.generate_text(
            prompt="To be or not to be",
            max_length=150,
            num_return_sequences=1,
            temperature=0.8
        )
        
        print("\n" + "="*50)
        print("🎭 GENERATED SHAKESPEARE-STYLE TEXT:")
        print("="*50)
        print(generated[0])
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_test()
