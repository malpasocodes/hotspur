# standard_tokenization.py
import json
from collections import Counter
from transformers import AutoTokenizer

# Use a standard modern tokenizer (GPT-2 style, vocab ~50K)
print("Loading standard GPT-2 tokenizer...")
tokenizer = AutoTokenizer.from_pretrained('gpt2')

print(f"Tokenizer vocabulary size: {tokenizer.vocab_size}")  # Should be ~50K

# Read Shakespeare text
with open('data/processed/shakespeare_only.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Tokenize using the standard tokenizer
print("Tokenizing Shakespeare with standard GPT-2 tokenizer...")
token_ids = tokenizer.encode(content)
tokens_text = [tokenizer.decode([token_id]) for token_id in token_ids]

print(f"Total tokens in Shakespeare: {len(token_ids)}")
print(f"Using standard vocabulary size: {tokenizer.vocab_size}")

# Show how some words get tokenized
test_words = ["Shakespeare", "beautiful", "wherefore", "love", "the"]
print(f"\nHow standard tokenizer handles Shakespeare words:")
for word in test_words:
    token_ids_word = tokenizer.encode(word, add_special_tokens=False)
    tokens_word = [tokenizer.decode([tid]) for tid in token_ids_word]
    print(f"'{word}' -> {tokens_word} (IDs: {token_ids_word})")

# Count which tokens from the standard vocab actually appear in Shakespeare
token_counts = Counter(token_ids)
print(f"\nShakespeare uses {len(token_counts)} unique tokens from the {tokenizer.vocab_size} vocab")

# Save the tokenized Shakespeare
result = {
    'tokenizer': 'gpt2',
    'vocab_size': tokenizer.vocab_size,
    'shakespeare_tokens': token_ids,
    'tokens_used_in_shakespeare': len(token_counts),
    'total_tokens': len(token_ids)
}

with open('data/processed/shakespeare_standard_tokenized.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"\nSaved tokenized Shakespeare using standard vocab to shakespeare_standard_tokenized.json")