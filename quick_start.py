#!/usr/bin/env python3
"""
Quick start script for Hotspur - Shakespeare Expert AI Assistant.
This script provides easy-to-use functions for training and interacting with Hotspur.
"""

from finetune_shakespeare import ShakespeareFineTuner
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def quick_train(model_name="distilgpt2", epochs=2):
    """
    Quick training function with sensible defaults.
    
    Args:
        model_name: Model to use ('distilgpt2', 'gpt2', etc.)
        epochs: Number of training epochs
    """
    print(f"🎭 Training Hotspur Shakespeare Expert AI with {model_name}")
    print(f"📚 Training for {epochs} epochs to build expertise...")
    
    fine_tuner = ShakespeareFineTuner(
        model_name=model_name,
        output_dir=f"shakespeare-{model_name.replace('/', '-')}"
    )
    
    fine_tuner.train(
        num_train_epochs=epochs,
        per_device_train_batch_size=2,  # Smaller batch size for safety
        learning_rate=3e-5,
        logging_steps=25
    )
    
    print("✅ Training completed!")
    return fine_tuner

def quick_generate(prompt="Shall I compare thee", model_path="shakespeare-distilgpt2"):
    """
    Quick text generation function.
    
    Args:
        prompt: Starting text
        model_path: Path to fine-tuned model
    """
    print(f"🎪 Generating Shakespeare-style text...")
    print(f"📝 Prompt: '{prompt}'")
    
    fine_tuner = ShakespeareFineTuner()
    
    try:
        generated_texts = fine_tuner.generate_text(
            prompt=prompt,
            max_length=150,
            num_return_sequences=3,
            temperature=0.8,
            model_path=model_path
        )
        
        print("\n" + "="*60)
        print("🎭 GENERATED SHAKESPEAREAN TEXT:")
        print("="*60)
        
        for i, text in enumerate(generated_texts, 1):
            print(f"\n--- Verse {i} ---")
            print(text)
            print("-" * 40)
        
        print("="*60)
        return generated_texts
        
    except Exception as e:
        print(f"❌ Error generating text: {e}")
        print("💡 Make sure you've trained a model first!")
        return None

def demo_prompts():
    """Demo with various Shakespearean prompts."""
    prompts = [
        "To be or not to be",
        "Shall I compare thee to a summer's day",
        "All the world's a stage",
        "What light through yonder window breaks",
        "Friends, Romans, countrymen"
    ]
    
    print("🎭 Running Shakespeare generation demo...")
    
    for prompt in prompts:
        print(f"\n🎪 Generating for: '{prompt}'")
        quick_generate(prompt, model_path="shakespeare-distilgpt2")
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        print("🎭 Shakespeare LLM Quick Start")
        print("="*40)
        print("Usage:")
        print("  python quick_start.py train              # Train model")
        print("  python quick_start.py generate 'prompt'  # Generate text")
        print("  python quick_start.py demo               # Run demo")
        print("="*40)
    
    elif sys.argv[1] == "train":
        quick_train()
    
    elif sys.argv[1] == "generate":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "To be or not to be"
        quick_generate(prompt)
    
    elif sys.argv[1] == "demo":
        demo_prompts()
    
    else:
        print("❌ Unknown command. Use 'train', 'generate', or 'demo'")
