# create_vocabulary_dict.py
import re
import json
from collections import Counter

with open('data/processed/shakespeare_only.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Extract all words
words = re.findall(r'\b\w+\b', content.lower())
word_counts = Counter(words)

# Create vocabulary dictionary (word -> index)
# Add special tokens first
vocab = {
    '<PAD>': 0,    # for padding sequences
    '<UNK>': 1,    # for unknown words
    '<START>': 2,  # for start of sequence
    '<END>': 3     # for end of sequence
}

# Add all words, starting from index 4
for i, (word, count) in enumerate(word_counts.most_common()):
    vocab[word] = i + 4

print(f"Vocabulary size: {len(vocab)}")
print(f"Sample vocabulary entries:")
for i, (word, idx) in enumerate(list(vocab.items())[:10]):
    print(f"'{word}': {idx}")

# Save vocabulary to file
with open('data/processed/vocabulary.json', 'w') as f:
    json.dump(vocab, f, indent=2)

print(f"\nSaved vocabulary to data/processed/vocabulary.json")