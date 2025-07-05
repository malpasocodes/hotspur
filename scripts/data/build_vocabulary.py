# build_vocabulary.py
with open('data/processed/shakespeare_only.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Simple tokenization - split into words, lowercase, remove punctuation
import re
from collections import Counter

# Extract all words (letters only, lowercase)
words = re.findall(r'\b\w+\b', content.lower())

print(f"Total words in all Shakespeare: {len(words)}")

# Count word frequencies
word_counts = Counter(words)
print(f"Unique words: {len(word_counts)}")

print(f"\nTop 20 most common words:")
for word, count in word_counts.most_common(20):
    print(f"'{word}': {count}")

print(f"\nSome rare words (appear only once):")
rare_words = [word for word, count in word_counts.items() if count == 1]
print(f"Words appearing only once: {len(rare_words)}")
print(f"Examples: {rare_words[:10]}")