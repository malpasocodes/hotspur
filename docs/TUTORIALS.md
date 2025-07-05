# Tutorials and Examples

## Table of Contents

1. [Getting Started Tutorial](#getting-started-tutorial)
2. [Basic Usage Examples](#basic-usage-examples)
3. [Advanced Training Techniques](#advanced-training-techniques)
4. [Generation Strategies](#generation-strategies)
5. [Custom Dataset Tutorial](#custom-dataset-tutorial)
6. [Fine-tuning Best Practices](#fine-tuning-best-practices)
7. [Integration Examples](#integration-examples)

## Getting Started Tutorial

### Your First Shakespeare Model

This tutorial will walk you through training your first Shakespeare language model in under 10 minutes.

#### Step 1: Verify Installation

```bash
# Check that everything is installed correctly
python demo.py
```

You should see:
```
✅ Python version: 3.10.x
✅ PyTorch installed: 2.0.x
✅ Transformers installed: 4.x.x
✅ GPU available: Yes/No
✅ Shakespeare data found
```

#### Step 2: Quick Training

```bash
# Train a small model for testing (takes ~5 minutes on GPU)
python quick_start.py train --model distilgpt2 --epochs 1
```

Watch the output:
```
Loading Shakespeare text...
✅ Loaded 196,006 lines of Shakespeare

Initializing model...
✅ Model: distilgpt2 (82M parameters)

Training...
Epoch 1/1: 100%|████████| 1000/1000 [05:23<00:00, 3.09it/s]

✅ Training complete! Model saved to: shakespeare-distilgpt2/
```

#### Step 3: Generate Your First Text

```bash
python quick_start.py generate "To be or not to be"
```

Output:
```
Generated text:
To be or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune...
```

## Basic Usage Examples

### Example 1: Command Line Training

```bash
# Standard training
python finetune_shakespeare.py \
    --model distilgpt2 \
    --epochs 2 \
    --batch-size 2

# High-quality training
python finetune_shakespeare.py \
    --model gpt2-medium \
    --epochs 3 \
    --batch-size 4 \
    --learning-rate 2e-5

# Memory-efficient training
python finetune_shakespeare.py \
    --model gpt2 \
    --batch-size 1 \
    --gradient-accumulation 4
```

### Example 2: Python Script Usage

```python
# basic_example.py
from finetune_shakespeare import ShakespeareFineTuner

# Initialize and train
fine_tuner = ShakespeareFineTuner(model_name="distilgpt2")
fine_tuner.train(num_train_epochs=2)

# Generate text
prompts = [
    "To be or not to be",
    "Shall I compare thee",
    "All the world's a stage"
]

for prompt in prompts:
    print(f"\nPrompt: {prompt}")
    generated = fine_tuner.generate_text(prompt, max_length=100)
    print(f"Generated: {generated[0]}")
```

### Example 3: Batch Generation

```python
# batch_generation.py
from finetune_shakespeare import ShakespeareFineTuner

# Load a trained model
fine_tuner = ShakespeareFineTuner(
    model_name="distilgpt2",
    output_dir="shakespeare-distilgpt2"
)

# Generate multiple variations
variations = fine_tuner.generate_text(
    prompt="Romeo, Romeo, wherefore art thou",
    num_return_sequences=5,
    temperature=0.9,
    max_length=150
)

for i, text in enumerate(variations):
    print(f"\n--- Variation {i+1} ---")
    print(text)
```

## Advanced Training Techniques

### Using Configuration Presets

```python
# advanced_training.py
from finetune_shakespeare import ShakespeareFineTuner
from config import get_training_preset, get_model_config

# Use predefined configurations
model_config = get_model_config("gpt2")
training_config = get_training_preset("high_quality")

fine_tuner = ShakespeareFineTuner(**model_config)
fine_tuner.train(**training_config)
```

### Custom Training Loop

```python
# custom_training.py
from finetune_shakespeare import ShakespeareFineTuner
import torch

class CustomShakespeareTrainer(ShakespeareFineTuner):
    def train(self, **kwargs):
        # Custom preprocessing
        print("Applying custom preprocessing...")
        
        # Add custom callbacks
        kwargs['callbacks'] = [self.custom_callback()]
        
        # Call parent train method
        return super().train(**kwargs)
    
    def custom_callback(self):
        # Implement custom training callback
        from transformers import TrainerCallback
        
        class MyCallback(TrainerCallback):
            def on_epoch_end(self, args, state, control, **kwargs):
                print(f"Epoch {state.epoch} completed!")
                # Add custom logic here
        
        return MyCallback()

# Use custom trainer
trainer = CustomShakespeareTrainer()
trainer.train(num_train_epochs=3)
```

### Distributed Training

```python
# distributed_training.py
import torch
from finetune_shakespeare import ShakespeareFineTuner

# For multi-GPU training
if torch.cuda.device_count() > 1:
    print(f"Using {torch.cuda.device_count()} GPUs")
    
    fine_tuner = ShakespeareFineTuner(
        model_name="gpt2-medium",
        device="cuda"
    )
    
    # Trainer will automatically use DataParallel
    fine_tuner.train(
        num_train_epochs=3,
        per_device_train_batch_size=4,  # Per GPU
        gradient_accumulation_steps=1
    )
```

## Generation Strategies

### Example 1: Conservative Generation

```python
# conservative_generation.py
from finetune_shakespeare import ShakespeareFineTuner

fine_tuner = ShakespeareFineTuner()

# Conservative settings for coherent output
text = fine_tuner.generate_text(
    prompt="Friends, Romans, countrymen",
    temperature=0.7,          # Lower temperature
    top_k=40,                 # Restrict vocabulary
    top_p=0.9,                # Nucleus sampling
    repetition_penalty=1.3,   # Avoid repetition
    max_length=200
)
```

### Example 2: Creative Generation

```python
# creative_generation.py
from finetune_shakespeare import ShakespeareFineTuner

fine_tuner = ShakespeareFineTuner()

# Creative settings for varied output
text = fine_tuner.generate_text(
    prompt="What dreams may come",
    temperature=1.0,          # Higher temperature
    top_k=100,                # Broader vocabulary
    top_p=0.95,               # More diverse sampling
    repetition_penalty=1.1,   # Allow some repetition
    max_length=300
)
```

### Example 3: Interactive Generation

```python
# interactive_generation.py
from finetune_shakespeare import ShakespeareFineTuner

def interactive_shakespeare():
    fine_tuner = ShakespeareFineTuner()
    
    print("Shakespeare Text Generator")
    print("Type 'quit' to exit\n")
    
    while True:
        prompt = input("Enter prompt: ")
        if prompt.lower() == 'quit':
            break
        
        # Get temperature from user
        temp = input("Temperature (0.7-1.2, default 0.8): ")
        temperature = float(temp) if temp else 0.8
        
        # Generate
        texts = fine_tuner.generate_text(
            prompt=prompt,
            temperature=temperature,
            num_return_sequences=1
        )
        
        print(f"\nGenerated:\n{texts[0]}\n")

if __name__ == "__main__":
    interactive_shakespeare()
```

## Custom Dataset Tutorial

### Using Your Own Text

```python
# custom_dataset.py
from finetune_shakespeare import ShakespeareFineTuner

# Example 1: Using a different author
fine_tuner = ShakespeareFineTuner(
    shakespeare_file="data/jane_austen.txt",
    output_dir="austen-gpt2"
)

# Example 2: Using multiple text files
import os

def combine_texts(file_list, output_file):
    """Combine multiple text files into one."""
    with open(output_file, 'w') as outfile:
        for fname in file_list:
            with open(fname) as infile:
                outfile.write(infile.read())
                outfile.write("\n\n")

# Combine multiple works
texts = [
    "data/hamlet.txt",
    "data/macbeth.txt",
    "data/romeo_juliet.txt"
]
combine_texts(texts, "data/combined_plays.txt")

# Train on combined texts
fine_tuner = ShakespeareFineTuner(
    shakespeare_file="data/combined_plays.txt"
)
```

### Preprocessing Custom Data

```python
# preprocess_custom.py
import re

def preprocess_text(input_file, output_file):
    """Clean and prepare text for training."""
    
    with open(input_file, 'r') as f:
        text = f.read()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Split into reasonable chunks
    sentences = text.split('.')
    
    # Write cleaned text
    with open(output_file, 'w') as f:
        for sentence in sentences:
            if len(sentence.strip()) > 10:  # Skip very short sentences
                f.write(sentence.strip() + '.\n')

# Use preprocessed text
preprocess_text("raw_text.txt", "clean_text.txt")
fine_tuner = ShakespeareFineTuner(shakespeare_file="clean_text.txt")
```

## Fine-tuning Best Practices

### 1. Choosing the Right Model

```python
# model_selection.py
from config import recommend_model
import torch

# Get recommendation based on your system
if torch.cuda.is_available():
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
    recommended = recommend_model(gpu_memory)
    print(f"Recommended model: {recommended}")
else:
    print("No GPU detected. Using distilgpt2 for CPU training.")
    recommended = "distilgpt2"

# Train with recommended model
from finetune_shakespeare import ShakespeareFineTuner
fine_tuner = ShakespeareFineTuner(model_name=recommended)
```

### 2. Monitoring Training

```python
# monitor_training.py
from finetune_shakespeare import ShakespeareFineTuner
from transformers import TrainerCallback
import matplotlib.pyplot as plt

class PlottingCallback(TrainerCallback):
    def __init__(self):
        self.train_loss = []
        self.eval_loss = []
    
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs:
            if 'loss' in logs:
                self.train_loss.append(logs['loss'])
            if 'eval_loss' in logs:
                self.eval_loss.append(logs['eval_loss'])
    
    def on_train_end(self, args, state, control, **kwargs):
        # Plot losses
        plt.figure(figsize=(10, 6))
        plt.plot(self.train_loss, label='Training Loss')
        plt.plot(self.eval_loss, label='Validation Loss')
        plt.xlabel('Steps')
        plt.ylabel('Loss')
        plt.legend()
        plt.savefig('training_losses.png')

# Use with training
fine_tuner = ShakespeareFineTuner()
callback = PlottingCallback()
fine_tuner.train(callbacks=[callback])
```

### 3. Preventing Overfitting

```python
# prevent_overfitting.py
from finetune_shakespeare import ShakespeareFineTuner

# Best practices for avoiding overfitting
fine_tuner = ShakespeareFineTuner(
    model_name="gpt2",
    max_length=256  # Shorter sequences
)

fine_tuner.train(
    num_train_epochs=2,           # Don't overtrain
    learning_rate=2e-5,           # Lower learning rate
    weight_decay=0.01,            # L2 regularization
    warmup_steps=500,             # Gradual warmup
    eval_steps=100,               # Frequent evaluation
    load_best_model_at_end=True,  # Use best checkpoint
    early_stopping_patience=3      # Stop if no improvement
)
```

## Integration Examples

### Flask Web API

```python
# shakespeare_api.py
from flask import Flask, request, jsonify
from finetune_shakespeare import ShakespeareFineTuner

app = Flask(__name__)
fine_tuner = ShakespeareFineTuner()

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    temperature = data.get('temperature', 0.8)
    max_length = data.get('max_length', 200)
    
    texts = fine_tuner.generate_text(
        prompt=prompt,
        temperature=temperature,
        max_length=max_length
    )
    
    return jsonify({
        'prompt': prompt,
        'generated': texts[0],
        'parameters': {
            'temperature': temperature,
            'max_length': max_length
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
```

### Gradio Interface

```python
# gradio_interface.py
import gradio as gr
from finetune_shakespeare import ShakespeareFineTuner

# Load model
fine_tuner = ShakespeareFineTuner()

def generate_shakespeare(prompt, temperature, max_length):
    texts = fine_tuner.generate_text(
        prompt=prompt,
        temperature=temperature,
        max_length=int(max_length),
        num_return_sequences=1
    )
    return texts[0]

# Create Gradio interface
iface = gr.Interface(
    fn=generate_shakespeare,
    inputs=[
        gr.Textbox(label="Prompt", placeholder="Enter your prompt..."),
        gr.Slider(0.5, 1.5, 0.8, label="Temperature"),
        gr.Slider(50, 500, 200, label="Max Length")
    ],
    outputs=gr.Textbox(label="Generated Text"),
    title="Shakespeare Text Generator",
    description="Generate Shakespeare-style text from your prompts"
)

iface.launch()
```

### Streamlit App

```python
# streamlit_app.py
import streamlit as st
from finetune_shakespeare import ShakespeareFineTuner

@st.cache_resource
def load_model():
    return ShakespeareFineTuner()

st.title("🎭 Shakespeare Text Generator")

# Load model
fine_tuner = load_model()

# User inputs
prompt = st.text_input("Enter your prompt:", "To be or not to be")
col1, col2 = st.columns(2)

with col1:
    temperature = st.slider("Temperature", 0.5, 1.5, 0.8)
    max_length = st.slider("Max Length", 50, 500, 200)

with col2:
    num_sequences = st.slider("Number of Variations", 1, 5, 1)
    
if st.button("Generate"):
    with st.spinner("Generating..."):
        texts = fine_tuner.generate_text(
            prompt=prompt,
            temperature=temperature,
            max_length=max_length,
            num_return_sequences=num_sequences
        )
    
    for i, text in enumerate(texts):
        st.subheader(f"Generation {i+1}")
        st.write(text)
```

## Next Steps

1. Try different models and compare results
2. Experiment with generation parameters
3. Fine-tune on your own text corpus
4. Build an application using the API
5. Share your creations!

For more details, see the [API Reference](API_REFERENCE.md) and [Troubleshooting Guide](TROUBLESHOOTING.md).