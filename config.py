#!/usr/bin/env python3
"""
Configuration file for Shakespeare fine-tuning with different model presets.
"""

# Model configurations with memory requirements and expected performance
MODEL_CONFIGS = {
    "distilgpt2": {
        "model_name": "distilgpt2",
        "description": "Lightweight GPT-2 variant, great for experimentation",
        "gpu_memory_gb": 4,
        "training_time_hrs": 0.5,
        "recommended_batch_size": 4,
        "recommended_epochs": 3,
        "learning_rate": 3e-5,
        "quality": "Good",
        "speed": "Fast"
    },
    
    "gpt2": {
        "model_name": "gpt2",
        "description": "Standard GPT-2 model, balanced performance",
        "gpu_memory_gb": 6,
        "training_time_hrs": 0.8,
        "recommended_batch_size": 3,
        "recommended_epochs": 3,
        "learning_rate": 2e-5,
        "quality": "Very Good",
        "speed": "Medium"
    },
    
    "gpt2-medium": {
        "model_name": "gpt2-medium",
        "description": "Larger GPT-2 model, higher quality output",
        "gpu_memory_gb": 10,
        "training_time_hrs": 2.0,
        "recommended_batch_size": 2,
        "recommended_epochs": 2,
        "learning_rate": 1e-5,
        "quality": "Excellent",
        "speed": "Slow"
    },
    
    "gpt2-large": {
        "model_name": "gpt2-large",
        "description": "Large GPT-2 model, best quality but resource intensive",
        "gpu_memory_gb": 16,
        "training_time_hrs": 4.0,
        "recommended_batch_size": 1,
        "recommended_epochs": 2,
        "learning_rate": 5e-6,
        "quality": "Outstanding",
        "speed": "Very Slow"
    }
}

# Training presets for different scenarios
TRAINING_PRESETS = {
    "quick_test": {
        "description": "Quick test run for validation",
        "epochs": 1,
        "batch_size": 2,
        "learning_rate": 5e-5,
        "max_length": 256,
        "logging_steps": 10
    },
    
    "development": {
        "description": "Development setup for experimentation",
        "epochs": 2,
        "batch_size": 4,
        "learning_rate": 3e-5,
        "max_length": 512,
        "logging_steps": 25
    },
    
    "production": {
        "description": "Production quality training",
        "epochs": 5,
        "batch_size": 4,
        "learning_rate": 2e-5,
        "max_length": 512,
        "logging_steps": 50
    },
    
    "high_quality": {
        "description": "High quality training for best results",
        "epochs": 8,
        "batch_size": 2,
        "learning_rate": 1e-5,
        "max_length": 768,
        "logging_steps": 100
    }
}

# Generation presets for different styles
GENERATION_PRESETS = {
    "conservative": {
        "temperature": 0.7,
        "top_p": 0.9,
        "repetition_penalty": 1.1,
        "description": "Conservative, coherent generation"
    },
    
    "balanced": {
        "temperature": 0.8,
        "top_p": 0.9,
        "repetition_penalty": 1.05,
        "description": "Balanced creativity and coherence"
    },
    
    "creative": {
        "temperature": 1.0,
        "top_p": 0.95,
        "repetition_penalty": 1.0,
        "description": "Creative, more varied generation"
    },
    
    "experimental": {
        "temperature": 1.2,
        "top_p": 0.98,
        "repetition_penalty": 0.95,
        "description": "Highly creative, experimental output"
    }
}

def print_model_comparison():
    """Print a comparison table of different models."""
    print("🎭 Shakespeare LLM Model Comparison")
    print("="*80)
    print(f"{'Model':<15} {'Quality':<12} {'Speed':<10} {'GPU (GB)':<8} {'Batch Size':<10}")
    print("-"*80)
    
    for key, config in MODEL_CONFIGS.items():
        print(f"{key:<15} {config['quality']:<12} {config['speed']:<10} "
              f"{config['gpu_memory_gb']:<8} {config['recommended_batch_size']:<10}")
    print("="*80)

def get_model_config(model_key: str):
    """Get configuration for a specific model."""
    return MODEL_CONFIGS.get(model_key, MODEL_CONFIGS["distilgpt2"])

def get_training_preset(preset_key: str):
    """Get training preset configuration."""
    return TRAINING_PRESETS.get(preset_key, TRAINING_PRESETS["development"])

def get_generation_preset(preset_key: str):
    """Get generation preset configuration."""
    return GENERATION_PRESETS.get(preset_key, GENERATION_PRESETS["balanced"])

def recommend_model(gpu_memory_gb: float = None):
    """Recommend a model based on available GPU memory."""
    if gpu_memory_gb is None:
        print("💡 Without GPU specification, recommending DistilGPT-2 for CPU training")
        return "distilgpt2"
    
    suitable_models = []
    for key, config in MODEL_CONFIGS.items():
        if config['gpu_memory_gb'] <= gpu_memory_gb:
            suitable_models.append((key, config))
    
    if not suitable_models:
        print(f"⚠️  No models fit in {gpu_memory_gb}GB, recommending DistilGPT-2 anyway")
        return "distilgpt2"
    
    # Recommend the largest model that fits
    best_model = max(suitable_models, key=lambda x: x[1]['gpu_memory_gb'])
    print(f"💡 For {gpu_memory_gb}GB GPU, recommending: {best_model[0]}")
    return best_model[0]

if __name__ == "__main__":
    print_model_comparison()
    print("\n🎯 Training Presets:")
    for key, preset in TRAINING_PRESETS.items():
        print(f"  {key}: {preset['description']}")
    
    print("\n🎨 Generation Styles:")
    for key, style in GENERATION_PRESETS.items():
        print(f"  {key}: {style['description']}")
