# create_vocab_from_tokens.py
import json
from collections import Counter

# Load the tokenized data
with open('data/processed/shakespeare_tokens_full.json', 'r') as f:
    tokenized_data = json.load(f)

tokens = tokenized_data['tokens']
print(f"Total token instances: {len(tokens)}")

# Count token frequencies
token_counts = Counter(tokens)
print(f"Unique token types: {len(token_counts)}")

# Show most common tokens (by number)
print("\nMost common token IDs:")
for token_id, count in token_counts.most_common(10):
    print(f"Token ID {token_id}: appears {count} times")

# Create vocabulary mapping: token_id -> index for our model
vocab = {}
for i, (token_id, count) in enumerate(token_counts.most_common()):
    vocab[token_id] = i

print(f"\nVocabulary size: {len(vocab)}")
print("Sample vocab mapping (token_id -> our_index):")
for i, (token_id, our_index) in enumerate(list(vocab.items())[:10]):
    print(f"Token {token_id} -> Index {our_index}")

# Save vocabulary
vocab_data = {
    'vocab': vocab,  # token_id -> our_index
    'vocab_size': len(vocab),
    'total_tokens': len(tokens),
    'tokenizer': tokenized_data['tokenizer']
}

with open('data/processed/shakespeare_vocabulary.json', 'w') as f:
    json.dump(vocab_data, f, indent=2)

print(f"\nSaved vocabulary to shakespeare_vocabulary.json")