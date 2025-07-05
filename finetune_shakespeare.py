#!/usr/bin/env python3
"""
Hotspur: Shakespeare Expert AI Assistant
Fine-tunes language models on Shakespeare's complete works to create an expert AI resource
for scholars, students, and enthusiasts of Shakespearean literature.
"""

import os
import json
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    TrainingArguments,
    Trainer,
    pipeline
)
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShakespeareFineTuner:
    def __init__(
        self,
        model_name: str = "distilgpt2",
        shakespeare_file: str = "data/processed/shakespeare_only.txt",
        output_dir: str = "shakespeare-model",
        max_length: int = 512
    ):
        """
        Initialize the Shakespeare fine-tuner.
        
        Args:
            model_name: Pretrained model to use (e.g., 'gpt2', 'distilgpt2', 'microsoft/DialoGPT-medium')
            shakespeare_file: Path to the Shakespeare text file
            output_dir: Directory to save the fine-tuned model
            max_length: Maximum sequence length for training
        """
        self.model_name = model_name
        self.shakespeare_file = shakespeare_file
        self.output_dir = output_dir
        self.max_length = max_length
        
        # Initialize tokenizer and model
        self.tokenizer = None
        self.model = None
        self.dataset = None
        
    def load_and_prepare_data(self) -> List[str]:
        """Load Shakespeare text and prepare it for training."""
        logger.info(f"Loading Shakespeare text from {self.shakespeare_file}")
        
        with open(self.shakespeare_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Basic text cleaning
        text = text.strip()
        
        # Split into smaller chunks for better training
        # We'll create overlapping segments to preserve context
        segments = self.create_text_segments(text)
        
        logger.info(f"Created {len(segments)} text segments for training")
        return segments
    
    def create_text_segments(self, text: str, overlap: int = 50) -> List[str]:
        """
        Create overlapping text segments for training.
        
        Args:
            text: Full Shakespeare text
            overlap: Number of tokens to overlap between segments
            
        Returns:
            List of text segments
        """
        # Split by lines and filter out very short lines
        lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 10]
        
        segments = []
        current_segment = []
        current_length = 0
        
        for line in lines:
            # Estimate token count (rough approximation)
            line_tokens = len(line.split())
            
            if current_length + line_tokens <= self.max_length - 50:  # Leave room for special tokens
                current_segment.append(line)
                current_length += line_tokens
            else:
                if current_segment:
                    segments.append('\n'.join(current_segment))
                
                # Start new segment with some overlap
                if len(current_segment) > overlap:
                    current_segment = current_segment[-overlap:] + [line]
                    current_length = sum(len(l.split()) for l in current_segment)
                else:
                    current_segment = [line]
                    current_length = line_tokens
        
        # Add the last segment
        if current_segment:
            segments.append('\n'.join(current_segment))
        
        return segments
    
    def setup_model_and_tokenizer(self):
        """Initialize the tokenizer and model."""
        logger.info(f"Loading model and tokenizer: {self.model_name}")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # Add pad token if it doesn't exist
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        
        # Resize token embeddings if needed
        self.model.resize_token_embeddings(len(self.tokenizer))
    
    def tokenize_function(self, examples: Dict) -> Dict:
        """Tokenize the text examples."""
        # Tokenize the texts
        tokenized = self.tokenizer(
            examples["text"],
            truncation=True,
            padding=False,
            max_length=self.max_length,
            return_overflowing_tokens=True,
            return_length=True,
        )
        
        # Use input_ids as labels for language modeling
        tokenized["labels"] = tokenized["input_ids"].copy()
        
        return tokenized
    
    def prepare_dataset(self, text_segments: List[str]) -> Dataset:
        """Prepare the dataset for training."""
        logger.info("Preparing dataset...")
        
        # Create dataset
        dataset_dict = {"text": text_segments}
        dataset = Dataset.from_dict(dataset_dict)
        
        # Tokenize dataset
        tokenized_dataset = dataset.map(
            self.tokenize_function,
            batched=True,
            remove_columns=dataset.column_names,
            desc="Tokenizing texts"
        )
        
        return tokenized_dataset
    
    def train(
        self,
        num_train_epochs: int = 3,
        per_device_train_batch_size: int = 4,
        learning_rate: float = 5e-5,
        warmup_steps: int = 100,
        logging_steps: int = 50,
        save_steps: int = 500,
        eval_steps: int = 500,
        save_total_limit: int = 3
    ):
        """Train the model on Shakespeare text."""
        
        # Load and prepare data
        text_segments = self.load_and_prepare_data()
        
        # Setup model and tokenizer
        self.setup_model_and_tokenizer()
        
        # Prepare dataset
        dataset = self.prepare_dataset(text_segments)
        
        # Split into train and validation
        train_size = int(0.9 * len(dataset))
        train_dataset = dataset.select(range(train_size))
        eval_dataset = dataset.select(range(train_size, len(dataset)))
        
        logger.info(f"Training on {len(train_dataset)} examples")
        logger.info(f"Evaluating on {len(eval_dataset)} examples")
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,  # We're doing causal language modeling, not masked LM
        )
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            overwrite_output_dir=True,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=per_device_train_batch_size,
            per_device_eval_batch_size=per_device_train_batch_size,
            learning_rate=learning_rate,
            warmup_steps=warmup_steps,
            logging_steps=logging_steps,
            save_steps=save_steps,
            eval_steps=eval_steps,
            evaluation_strategy="steps",
            save_total_limit=save_total_limit,
            prediction_loss_only=True,
            remove_unused_columns=False,
            dataloader_pin_memory=False,
            report_to=None,  # Disable wandb/tensorboard logging
            gradient_accumulation_steps=2,
            fp16=torch.cuda.is_available(),  # Use mixed precision if GPU available
        )
        
        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=self.tokenizer,
        )
        
        # Train the model
        logger.info("Starting training...")
        trainer.train()
        
        # Save the final model
        logger.info(f"Saving final model to {self.output_dir}")
        trainer.save_model()
        self.tokenizer.save_pretrained(self.output_dir)
        
        # Save training info
        training_info = {
            "base_model": self.model_name,
            "num_epochs": num_train_epochs,
            "learning_rate": learning_rate,
            "train_samples": len(train_dataset),
            "eval_samples": len(eval_dataset),
            "max_length": self.max_length
        }
        
        with open(os.path.join(self.output_dir, "training_info.json"), "w") as f:
            json.dump(training_info, f, indent=2)
        
        logger.info("Training completed!")
    
    def generate_text(
        self,
        prompt: str = "To be or not to be",
        max_length: int = 200,
        num_return_sequences: int = 1,
        temperature: float = 0.8,
        model_path: Optional[str] = None
    ) -> List[str]:
        """
        Generate Shakespeare-style text using the fine-tuned model.
        
        Args:
            prompt: Starting text for generation
            max_length: Maximum length of generated text
            num_return_sequences: Number of sequences to generate
            temperature: Sampling temperature (higher = more creative)
            model_path: Path to fine-tuned model (if None, uses self.output_dir)
            
        Returns:
            List of generated texts
        """
        if model_path is None:
            model_path = self.output_dir
        
        logger.info(f"Loading model from {model_path}")
        
        # Load the fine-tuned model
        generator = pipeline(
            "text-generation",
            model=model_path,
            tokenizer=model_path,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        
        # Generate text
        outputs = generator(
            prompt,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            temperature=temperature,
            do_sample=True,
            pad_token_id=generator.tokenizer.eos_token_id
        )
        
        return [output["generated_text"] for output in outputs]


def main():
    """Main function to run the fine-tuning process."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fine-tune a language model on Shakespeare")
    parser.add_argument("--model", default="distilgpt2", help="Pretrained model to use")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=4, help="Training batch size")
    parser.add_argument("--learning-rate", type=float, default=5e-5, help="Learning rate")
    parser.add_argument("--output-dir", default="shakespeare-model", help="Output directory")
    parser.add_argument("--generate-only", action="store_true", help="Only generate text, don't train")
    parser.add_argument("--prompt", default="To be or not to be", help="Prompt for text generation")
    
    args = parser.parse_args()
    
    # Initialize fine-tuner
    fine_tuner = ShakespeareFineTuner(
        model_name=args.model,
        output_dir=args.output_dir
    )
    
    if args.generate_only:
        # Just generate text
        logger.info(f"Generating text with prompt: '{args.prompt}'")
        generated_texts = fine_tuner.generate_text(
            prompt=args.prompt,
            num_return_sequences=3
        )
        
        print("\n" + "="*50)
        print("GENERATED SHAKESPEARE-STYLE TEXT:")
        print("="*50)
        for i, text in enumerate(generated_texts, 1):
            print(f"\n--- Generation {i} ---")
            print(text)
        print("="*50)
    else:
        # Train the model
        fine_tuner.train(
            num_train_epochs=args.epochs,
            per_device_train_batch_size=args.batch_size,
            learning_rate=args.learning_rate
        )
        
        # Generate some sample text after training
        logger.info("Generating sample text after training...")
        generated_texts = fine_tuner.generate_text(
            prompt=args.prompt,
            num_return_sequences=2
        )
        
        print("\n" + "="*50)
        print("SAMPLE GENERATED TEXT:")
        print("="*50)
        for i, text in enumerate(generated_texts, 1):
            print(f"\n--- Sample {i} ---")
            print(text)
        print("="*50)


if __name__ == "__main__":
    main()
