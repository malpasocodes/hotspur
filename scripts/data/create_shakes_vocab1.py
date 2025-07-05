# create_shakespeare_vocab_no_stopwords.py
import re
import json
from collections import Counter

# Common English stop words
STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 
    'to', 'was', 'will', 'with', 'i', 'you', 'we', 'they', 'them', 
    'his', 'her', 'him', 'she', 'my', 'me', 'us', 'our', 'their',
    'but', 'not', 'or', 'so', 'if', 'then', 'than', 'when', 'where',
    'who', 'what', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'only', 'own'
}

# Read the clean Shakespeare text
with open('data/processed/shakespeare_only.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Extract all words
words = re.findall(r'\b[a-zA-Z]+\b', content)
words_lower = [word.lower() for word in words]

# Count all words
all_word_counts = Counter(words_lower)

# Filter out stop words
content_words = {word: count for word, count in all_word_counts.items() 
                 if word not in STOP_WORDS}

print(f"Total words: {len(words)}")
print(f"All unique words: {len(all_word_counts)}")
print(f"Content words (no stop words): {len(content_words)}")

# Show most common content words
content_word_counts = Counter(content_words)
print(f"\nTop 20 most common content words:")
for word, count in content_word_counts.most_common(20):
    print(f"'{word}': {count}")

# Save both versions
vocab_data = {
    'all_words': dict(all_word_counts),
    'content_words': content_words,
    'stop_words_removed': list(STOP_WORDS),
    'stats': {
        'total_words': len(words),
        'unique_all': len(all_word_counts),
        'unique_content': len(content_words)
    }
}

with open('data/processed/shakespeare_vocabulary.json', 'w', encoding='utf-8') as f:
    json.dump(vocab_data, f, indent=2, ensure_ascii=False)

print(f"\nSaved both full and filtered vocabularies to shakespeare_vocabulary.json")