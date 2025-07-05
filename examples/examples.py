#!/usr/bin/env python3
"""
Example usage of the Shakespeare LLM fine-tuning system.
This script demonstrates different ways to train and generate text.
"""

from finetune_shakespeare import ShakespeareFineTuner
from config import get_model_config, get_training_preset, get_generation_preset
import logging

logging.basicConfig(level=logging.INFO)

def example_quick_training():
    """Example: Quick training session for testing."""
    print("🎭 Example 1: Quick Training Session")
    print("="*50)
    
    # Get configuration for quick testing
    model_config = get_model_config("distilgpt2")
    training_preset = get_training_preset("quick_test")
    
    print(f"Using model: {model_config['model_name']}")
    print(f"Training preset: quick_test")
    
    # Initialize fine-tuner
    fine_tuner = ShakespeareFineTuner(
        model_name=model_config["model_name"],
        output_dir="shakespeare-quick-test",
        max_length=training_preset["max_length"]
    )
    
    # Train with quick settings
    fine_tuner.train(
        num_train_epochs=training_preset["epochs"],
        per_device_train_batch_size=training_preset["batch_size"],
        learning_rate=training_preset["learning_rate"],
        logging_steps=training_preset["logging_steps"]
    )
    
    print("✅ Quick training completed!")

def example_text_generation():
    """Example: Generate text with different styles."""
    print("\n🎪 Example 2: Text Generation with Different Styles")
    print("="*60)
    
    fine_tuner = ShakespeareFineTuner()
    prompts = [
        "To be or not to be",
        "Shall I compare thee to a summer's day",
        "All the world's a stage"
    ]
    
    styles = ["conservative", "balanced", "creative"]
    
    for prompt in prompts:
        print(f"\n📝 Prompt: '{prompt}'")
        print("-" * 40)
        
        for style in styles:
            print(f"\n🎨 Style: {style}")
            generation_config = get_generation_preset(style)
            
            try:
                generated = fine_tuner.generate_text(
                    prompt=prompt,
                    max_length=100,
                    num_return_sequences=1,
                    temperature=generation_config["temperature"],
                    model_path="shakespeare-quick-test"
                )
                
                print(f"Generated: {generated[0]}")
                
            except Exception as e:
                print(f"❌ Error (model may not exist yet): {e}")

def example_custom_training():
    """Example: Custom training with specific parameters."""
    print("\n🔧 Example 3: Custom Training Configuration")
    print("="*50)
    
    # Custom configuration
    custom_config = {
        "model_name": "distilgpt2",
        "output_dir": "shakespeare-custom",
        "epochs": 2,
        "batch_size": 2,
        "learning_rate": 2e-5,
        "max_length": 400
    }
    
    print("Custom configuration:")
    for key, value in custom_config.items():
        print(f"  {key}: {value}")
    
    fine_tuner = ShakespeareFineTuner(
        model_name=custom_config["model_name"],
        output_dir=custom_config["output_dir"],
        max_length=custom_config["max_length"]
    )
    
    # Note: Commented out to avoid long training in example
    # Uncomment to actually run training
    """
    fine_tuner.train(
        num_train_epochs=custom_config["epochs"],
        per_device_train_batch_size=custom_config["batch_size"],
        learning_rate=custom_config["learning_rate"]
    )
    """
    
    print("💡 Training configuration ready (uncomment to run)")

def example_model_comparison():
    """Example: Show different model options."""
    print("\n📊 Example 4: Model Comparison")
    print("="*50)
    
    from config import print_model_comparison, recommend_model
    
    print_model_comparison()
    
    # Example GPU memory scenarios
    gpu_scenarios = [4, 8, 16, None]
    
    print("\n💡 Model Recommendations:")
    for gpu_gb in gpu_scenarios:
        if gpu_gb:
            recommended = recommend_model(gpu_gb)
            print(f"  {gpu_gb}GB GPU: {recommended}")
        else:
            recommended = recommend_model()
            print(f"  CPU only: {recommended}")

if __name__ == "__main__":
    print("🎭 Shakespeare LLM Examples")
    print("="*60)
    print("This script demonstrates various usage patterns.")
    print("Choose what to run by uncommenting the relevant sections.\n")
    
    # Run model comparison (always safe)
    example_model_comparison()
    
    # Uncomment these to run actual training/generation:
    
    # Example 1: Quick training (takes ~15-30 minutes)
    # example_quick_training()
    
    # Example 2: Text generation (requires trained model)
    # example_text_generation()
    
    # Example 3: Custom training setup
    example_custom_training()
    
    print("\n🎉 Examples completed!")
    print("\n🚀 To actually train a model, run:")
    print("  python quick_start.py train")
    print("  python finetune_shakespeare.py --epochs 2")
