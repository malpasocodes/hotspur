#!/usr/bin/env python3
"""
Monitor the Shakespeare model training progress.
"""

import os
import time
import json
from pathlib import Path

def monitor_training():
    """Monitor training progress by checking for output files."""
    print("🔍 Monitoring Shakespeare LLM Training Progress")
    print("=" * 50)
    
    # Expected output directory
    output_dir = "shakespeare-distilgpt2"
    
    # Check if training has started
    if not os.path.exists(output_dir):
        print("📝 Training directory not yet created")
        print("⏳ Waiting for training to begin...")
        return
    
    print(f"📁 Training directory found: {output_dir}")
    
    # List contents
    files = list(Path(output_dir).rglob("*"))
    if files:
        print("\n📄 Files created during training:")
        for file_path in sorted(files):
            if file_path.is_file():
                size = file_path.stat().st_size
                print(f"   {file_path.name} ({size} bytes)")
    
    # Check for training info
    info_file = os.path.join(output_dir, "training_info.json")
    if os.path.exists(info_file):
        print("\n✅ Training completed!")
        with open(info_file, 'r') as f:
            info = json.load(f)
        print("📊 Training Summary:")
        for key, value in info.items():
            print(f"   {key}: {value}")
    else:
        print("\n⏳ Training still in progress...")
    
    # Check for checkpoint directories
    checkpoints = [d for d in os.listdir(output_dir) if d.startswith("checkpoint-")]
    if checkpoints:
        print(f"\n🔄 Checkpoints saved: {len(checkpoints)}")
        for checkpoint in sorted(checkpoints):
            print(f"   {checkpoint}")

if __name__ == "__main__":
    monitor_training()
