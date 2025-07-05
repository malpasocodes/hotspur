# save_full_tokenized.py
from transformers import AutoTokenizer
import json

# Load the same tokenizer (it will use cached version now)
try:
    tokenizer = AutoTokenizer.from_pretrained('meta-llama/Llama-2-7b-hf')
    tokenizer_name = "Llama-2"
except:
    try:
        tokenizer = AutoTokenizer.from_pretrained('codellama/CodeLlama-7b-hf')
        tokenizer_name = "CodeLlama"
    except:
        tokenizer = AutoTokenizer.from_pretrained('mistralai/Mistral-7B-v0.1')
        tokenizer_name = "Mistral"

with open('data/processed/shakespeare_only.txt', 'r', encoding='utf-8') as file:
    content = file.read()

print(f"Tokenizing full corpus with {tokenizer_name}...")
tokens = tokenizer.encode(content)

# Save the FULL tokenized corpus
print(f"Saving all {len(tokens)} tokens...")
with open('data/processed/shakespeare_tokens_full.json', 'w') as f:
    json.dump({
        'tokenizer': tokenizer_name,
        'tokens': tokens,  # All tokens, not just sample
        'total_tokens': len(tokens),
        'vocab_size': tokenizer.vocab_size
    }, f)

print(f"Saved complete tokenized corpus to shakespeare_tokens_full.json")
print(f"File contains {len(tokens)} tokens ready for LLM training")