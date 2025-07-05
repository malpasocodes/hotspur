# standard_vocabulary_text.py
import json
from collections import Counter
from transformers import AutoTokenizer

# Use standard GPT-2 tokenizer
print("Loading standard GPT-2 tokenizer...")
tokenizer = AutoTokenizer.from_pretrained('gpt2')

# Read Shakespeare text
with open('data/processed/shakespeare_only.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Tokenize to get the actual text pieces (not numbers)
print("Tokenizing Shakespeare into text pieces...")
token_ids = tokenizer.encode(content)
token_pieces = [tokenizer.decode([token_id]) for token_id in token_ids]

print(f"Total token pieces: {len(token_pieces)}")

# Count frequency of each text piece
token_counts = Counter(token_pieces)
print(f"Unique token pieces used: {len(token_counts)}")

# Show most common token pieces
print(f"\nMost common token pieces in Shakespeare:")
for token_piece, count in token_counts.most_common(20):
    print(f"'{token_piece}': {count}")

# Show some examples of subword pieces
print(f"\nExamples of subword pieces found:")
subword_examples = [piece for piece in token_counts.keys() if piece.startswith('Ġ') or len(piece) < 4][:10]
for piece in subword_examples:
    print(f"'{piece}': {token_counts[piece]} times")

# Create vocabulary of actual text pieces
shakespeare_vocab = {
    'vocabulary_type': 'gpt2_subword_pieces',
    'token_pieces': dict(token_counts),  # actual text pieces -> frequency
    'total_pieces': len(token_pieces),
    'unique_pieces': len(token_counts),
    'most_common_pieces': token_counts.most_common(100)
}

with open('data/processed/shakespeare_text_vocabulary.json', 'w', encoding='utf-8') as f:
    json.dump(shakespeare_vocab, f, indent=2, ensure_ascii=False)

print(f"\nSaved text-based vocabulary to shakespeare_text_vocabulary.json")
print(f"Vocabulary contains actual subword pieces like: {list(token_counts.keys())[:5]}")