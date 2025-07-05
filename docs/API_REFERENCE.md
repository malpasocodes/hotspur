# API Reference - Hotspur Shakespeare Expert AI

## ShakespeareFineTuner Class

The main class for fine-tuning language models to create Hotspur, an expert AI assistant for Shakespeare scholarship and education.

### Constructor

```python
ShakespeareFineTuner(
    model_name: str = "distilgpt2",
    shakespeare_file: str = "data/processed/shakespeare_only.txt",
    output_dir: str = None,
    max_length: int = 512,
    overlap_tokens: int = 50,
    device: str = None
)
```

#### Parameters

- **model_name** (`str`, optional): The pretrained model to fine-tune. Default: `"distilgpt2"`
  - Supported models: `"distilgpt2"`, `"gpt2"`, `"gpt2-medium"`, `"gpt2-large"`
  - Also supports any Hugging Face causal language model

- **shakespeare_file** (`str`, optional): Path to the Shakespeare text file. Default: `"data/processed/shakespeare_only.txt"`

- **output_dir** (`str`, optional): Directory to save the fine-tuned model. Default: `f"shakespeare-{model_name}"`

- **max_length** (`int`, optional): Maximum sequence length for tokenization. Default: `512`

- **overlap_tokens** (`int`, optional): Number of tokens to overlap between text segments. Default: `50`

- **device** (`str`, optional): Device to use for training/inference. Default: auto-detected (`"cuda"` if available, else `"cpu"`)

### Methods

#### train()

Fine-tune the model on Shakespeare text.

```python
train(
    num_train_epochs: int = 2,
    per_device_train_batch_size: int = 2,
    per_device_eval_batch_size: int = 2,
    gradient_accumulation_steps: int = 2,
    warmup_steps: int = 100,
    weight_decay: float = 0.01,
    logging_steps: int = 25,
    save_steps: int = 500,
    eval_steps: int = 500,
    save_strategy: str = "steps",
    evaluation_strategy: str = "steps",
    learning_rate: float = 3e-5,
    fp16: bool = None,
    load_best_model_at_end: bool = True,
    metric_for_best_model: str = "eval_loss",
    greater_is_better: bool = False,
    push_to_hub: bool = False
)
```

##### Parameters

- **num_train_epochs** (`int`): Number of training epochs. Default: `2`
- **per_device_train_batch_size** (`int`): Training batch size per device. Default: `2`
- **per_device_eval_batch_size** (`int`): Evaluation batch size per device. Default: `2`
- **gradient_accumulation_steps** (`int`): Gradient accumulation steps. Default: `2`
- **warmup_steps** (`int`): Number of warmup steps. Default: `100`
- **weight_decay** (`float`): Weight decay coefficient. Default: `0.01`
- **logging_steps** (`int`): Log every N steps. Default: `25`
- **save_steps** (`int`): Save checkpoint every N steps. Default: `500`
- **eval_steps** (`int`): Evaluate every N steps. Default: `500`
- **save_strategy** (`str`): Checkpoint saving strategy. Default: `"steps"`
- **evaluation_strategy** (`str`): Evaluation strategy. Default: `"steps"`
- **learning_rate** (`float`): Learning rate. Default: `3e-5`
- **fp16** (`bool`): Use mixed precision training. Default: auto-detected based on GPU
- **load_best_model_at_end** (`bool`): Load best model after training. Default: `True`
- **metric_for_best_model** (`str`): Metric to use for best model selection. Default: `"eval_loss"`
- **greater_is_better** (`bool`): Whether higher metric value is better. Default: `False`
- **push_to_hub** (`bool`): Push model to Hugging Face Hub. Default: `False`

##### Returns

- **trainer** (`Trainer`): The Hugging Face Trainer object after training

#### generate_text()

Generate Shakespeare-style text from a prompt.

```python
generate_text(
    prompt: str,
    max_length: int = 200,
    num_return_sequences: int = 1,
    temperature: float = 0.8,
    top_k: int = 50,
    top_p: float = 0.95,
    do_sample: bool = True,
    pad_token_id: int = None,
    eos_token_id: int = None,
    repetition_penalty: float = 1.2,
    no_repeat_ngram_size: int = 3
) -> List[str]
```

##### Parameters

- **prompt** (`str`): The input prompt to continue from
- **max_length** (`int`): Maximum length of generated text. Default: `200`
- **num_return_sequences** (`int`): Number of sequences to generate. Default: `1`
- **temperature** (`float`): Sampling temperature (higher = more creative). Default: `0.8`
- **top_k** (`int`): Top-k sampling parameter. Default: `50`
- **top_p** (`float`): Top-p (nucleus) sampling parameter. Default: `0.95`
- **do_sample** (`bool`): Whether to use sampling. Default: `True`
- **pad_token_id** (`int`): Padding token ID. Default: tokenizer's pad token
- **eos_token_id** (`int`): End-of-sequence token ID. Default: tokenizer's eos token
- **repetition_penalty** (`float`): Penalty for repetition. Default: `1.2`
- **no_repeat_ngram_size** (`int`): Size of n-grams to prevent repetition. Default: `3`

##### Returns

- **generated_texts** (`List[str]`): List of generated text sequences

#### prepare_dataset()

Prepare the dataset for training (called automatically by `train()`).

```python
prepare_dataset(test_size: float = 0.1) -> DatasetDict
```

##### Parameters

- **test_size** (`float`): Proportion of data to use for validation. Default: `0.1`

##### Returns

- **dataset** (`DatasetDict`): Dictionary containing 'train' and 'test' splits

### Example Usage

```python
from finetune_shakespeare import ShakespeareFineTuner

# Initialize with custom parameters
fine_tuner = ShakespeareFineTuner(
    model_name="gpt2",
    output_dir="my-shakespeare-gpt2",
    max_length=512,
    overlap_tokens=50
)

# Train the model
fine_tuner.train(
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-5
)

# Generate text
texts = fine_tuner.generate_text(
    prompt="To be or not to be",
    max_length=300,
    num_return_sequences=3,
    temperature=0.9
)

for i, text in enumerate(texts):
    print(f"Generation {i+1}:\n{text}\n")
```

## Configuration Module

### Model Presets

The `config.py` module provides pre-configured settings for different models:

```python
from config import MODEL_CONFIGS

# Available presets
MODELS = {
    "distilgpt2": {...},      # 82M params, 4GB GPU
    "gpt2": {...},            # 124M params, 6GB GPU
    "gpt2-medium": {...},     # 355M params, 10GB GPU
    "gpt2-large": {...}       # 774M params, 16GB GPU
}
```

### Training Presets

```python
from config import TRAINING_PRESETS

# Available presets
PRESETS = {
    "quick_test": {...},      # 1 epoch, for testing
    "development": {...},     # 2 epochs, balanced
    "production": {...},      # 3 epochs, standard
    "high_quality": {...}     # 5 epochs, best results
}
```

### Generation Style Presets

```python
from config import GENERATION_STYLES

# Available styles
STYLES = {
    "conservative": {...},    # temp=0.7, focused
    "balanced": {...},        # temp=0.8, default
    "creative": {...},        # temp=0.9, varied
    "experimental": {...}     # temp=1.0, diverse
}
```

### Helper Functions

#### get_model_config()

Get configuration for a specific model.

```python
get_model_config(model_name: str) -> Dict[str, Any]
```

#### get_training_preset()

Get training configuration preset.

```python
get_training_preset(preset_name: str) -> Dict[str, Any]
```

#### get_generation_style()

Get generation style configuration.

```python
get_generation_style(style_name: str) -> Dict[str, Any]
```

#### recommend_model()

Get model recommendation based on available resources.

```python
recommend_model(gpu_memory_gb: float = None) -> str
```

## Quick Start Module

The `quick_start.py` module provides a simple CLI interface:

### Commands

#### train

Train a model with default or custom settings.

```bash
python quick_start.py train [--model MODEL] [--epochs EPOCHS] [--batch-size BATCH_SIZE]
```

Options:
- `--model`: Model to use (default: "distilgpt2")
- `--epochs`: Number of training epochs (default: 2)
- `--batch-size`: Batch size per device (default: 2)

#### generate

Generate text from a prompt.

```bash
python quick_start.py generate "Your prompt here" [--model-dir DIR] [--temperature TEMP] [--max-length LENGTH]
```

Options:
- `--model-dir`: Directory containing the fine-tuned model
- `--temperature`: Sampling temperature (default: 0.8)
- `--max-length`: Maximum generation length (default: 200)

#### demo

Run a demo with multiple Shakespeare prompts.

```bash
python quick_start.py demo [--model-dir DIR]
```

## Error Handling

The API includes comprehensive error handling:

- **FileNotFoundError**: Raised when Shakespeare text file is not found
- **ValueError**: Raised for invalid model names or parameters
- **RuntimeError**: Raised for CUDA/GPU-related issues
- **OSError**: Raised for disk space or permission issues

All errors include helpful messages suggesting solutions.

## Performance Considerations

### Memory Usage

- **DistilGPT-2**: ~4GB GPU memory, suitable for most consumer GPUs
- **GPT-2**: ~6GB GPU memory
- **GPT-2 Medium**: ~10GB GPU memory
- **GPT-2 Large**: ~16GB GPU memory

### Training Speed

On a typical setup:
- **GPU (RTX 3060)**: ~5-15 minutes for 2 epochs
- **CPU (8-core)**: ~30-60 minutes for 2 epochs

### Optimization Tips

1. **Batch Size**: Increase if you have more GPU memory
2. **Gradient Accumulation**: Use to simulate larger batch sizes
3. **Mixed Precision**: Automatically enabled on compatible GPUs
4. **Sequence Length**: Reduce `max_length` for faster training
5. **Model Choice**: Start with DistilGPT-2 for experimentation