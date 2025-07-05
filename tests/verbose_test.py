#!/usr/bin/env python3
"""
Simplified Shakespeare training with verbose output and error handling
"""

import os
import sys
import time
import traceback
from datetime import datetime

def log_with_timestamp(message):
    """Print message with timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")
    sys.stdout.flush()

def test_basic_imports():
    """Test that all imports work."""
    log_with_timestamp("🔍 Testing imports...")
    
    try:
        import torch
        log_with_timestamp(f"✅ PyTorch {torch.__version__} - CUDA: {torch.cuda.is_available()}")
    except Exception as e:
        log_with_timestamp(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        log_with_timestamp("✅ Transformers imported")
    except Exception as e:
        log_with_timestamp(f"❌ Transformers import failed: {e}")
        return False
    
    try:
        from finetune_shakespeare import ShakespeareFineTuner
        log_with_timestamp("✅ ShakespeareFineTuner imported")
    except Exception as e:
        log_with_timestamp(f"❌ ShakespeareFineTuner import failed: {e}")
        return False
    
    return True

def test_data_loading():
    """Test data file loading."""
    log_with_timestamp("📚 Testing data loading...")
    
    data_file = "data/processed/shakespeare_only.txt"
    if not os.path.exists(data_file):
        log_with_timestamp(f"❌ Data file not found: {data_file}")
        return False
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            content = f.read()
        log_with_timestamp(f"✅ Data loaded: {len(content)} characters")
        return True
    except Exception as e:
        log_with_timestamp(f"❌ Data loading failed: {e}")
        return False

def test_model_download():
    """Test model downloading/loading with timeout."""
    log_with_timestamp("🤖 Testing model download/loading...")
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        # Test tokenizer first
        log_with_timestamp("Loading tokenizer...")
        start_time = time.time()
        tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        tokenizer_time = time.time() - start_time
        log_with_timestamp(f"✅ Tokenizer loaded in {tokenizer_time:.1f}s")
        
        # Test model loading
        log_with_timestamp("Loading model (this may take a few minutes on first run)...")
        start_time = time.time()
        model = AutoModelForCausalLM.from_pretrained(
            "distilgpt2",
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        model_time = time.time() - start_time
        log_with_timestamp(f"✅ Model loaded in {model_time:.1f}s")
        log_with_timestamp(f"Model has {model.num_parameters():,} parameters")
        
        return True
        
    except Exception as e:
        log_with_timestamp(f"❌ Model loading failed: {e}")
        traceback.print_exc()
        return False

def run_minimal_training():
    """Run minimal training with maximum verbosity."""
    log_with_timestamp("🚀 Starting minimal training...")
    
    try:
        from finetune_shakespeare import ShakespeareFineTuner
        
        # Initialize with minimal settings
        fine_tuner = ShakespeareFineTuner(
            model_name="distilgpt2",
            output_dir="test-shakespeare-minimal",
            max_length=256  # Smaller for faster processing
        )
        log_with_timestamp("✅ Fine-tuner initialized")
        
        # Test data preparation
        log_with_timestamp("📝 Preparing data...")
        segments = fine_tuner.load_and_prepare_data()
        log_with_timestamp(f"✅ Created {len(segments)} segments")
        
        # Test model setup
        log_with_timestamp("🔧 Setting up model and tokenizer...")
        fine_tuner.setup_model_and_tokenizer()
        log_with_timestamp("✅ Model and tokenizer ready")
        
        # Run ultra-minimal training
        log_with_timestamp("🎯 Starting training (1 epoch, tiny batch)...")
        fine_tuner.train(
            num_train_epochs=1,
            per_device_train_batch_size=1,
            learning_rate=5e-5,
            logging_steps=1,  # Log every step
            save_steps=10,
            eval_steps=10,
            warmup_steps=0
        )
        
        log_with_timestamp("🎉 Training completed successfully!")
        return True
        
    except Exception as e:
        log_with_timestamp(f"❌ Training failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run step-by-step diagnostics and training."""
    log_with_timestamp("🎭 Shakespeare LLM - Verbose Training")
    log_with_timestamp("=" * 60)
    
    # Step 1: Test imports
    if not test_basic_imports():
        log_with_timestamp("❌ Import test failed - stopping")
        return False
    
    # Step 2: Test data
    if not test_data_loading():
        log_with_timestamp("❌ Data test failed - stopping")
        return False
    
    # Step 3: Test model loading (this is often where it hangs)
    if not test_model_download():
        log_with_timestamp("❌ Model loading test failed - stopping")
        return False
    
    # Step 4: Run minimal training
    if not run_minimal_training():
        log_with_timestamp("❌ Training failed")
        return False
    
    log_with_timestamp("🎉 All tests passed! System is working correctly.")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        log_with_timestamp("✅ Ready for full training with: uv run python quick_start.py train")
    else:
        log_with_timestamp("❌ Issues found - check errors above")
