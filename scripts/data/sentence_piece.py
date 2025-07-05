# sophisticated_tokenization.py
import sentencepiece as spm
import json
from collections import Counter

# Step 1: Train a SentencePiece model on Shakespeare text
def train_sentencepiece_model():
    print("Training SentencePiece model on Shakespeare...")
    
    # Train the tokenizer
    spm.SentencePieceTrainer.train(
        input='data/processed/shakespeare_only.txt',
        model_prefix='shakespeare_sp',
        vocab_size=8000,  # Number of subword tokens to create
        character_coverage=1.0,
        model_type='bpe',  # Byte Pair Encoding
        pad_id=0,
        unk_id=1,
        bos_id=2,  # Beginning of sentence
        eos_id=3   # End of sentence
    )
    print("SentencePiece model trained!")

# Step 2: Load the trained model and tokenize
def tokenize_shakespeare():
    # Load the trained tokenizer
    sp = spm.SentencePieceProcessor()
    sp.load('shakespeare_sp.model')
    
    # Read Shakespeare text
    with open('data/processed/shakespeare_only.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Tokenize the entire text
    tokens = sp.encode_as_pieces(content)
    token_ids = sp.encode_as_ids(content)
    
    print(f"Total subword tokens: {len(tokens)}")
    print(f"Vocabulary size: {sp.get_piece_size()}")
    
    # Show examples of how words get broken down
    test_words = ["Shakespeare", "beautiful", "wherefore", "magnificent", "love", "the"]
    print(f"\nHow words get tokenized:")
    for word in test_words:
        pieces = sp.encode_as_pieces(word)
        print(f"'{word}' -> {pieces}")
    
    # Count token frequencies
    token_counts = Counter(tokens)
    print(f"\nMost common subword tokens:")
    for token, count in token_counts.most_common(20):
        print(f"'{token}': {count}")
    
    # Save results
    vocab_data = {
        'tokenizer_type': 'sentencepiece_bpe',
        'vocab_size': sp.get_piece_size(),
        'total_tokens': len(tokens),
        'sample_tokens': tokens[:100],
        'token_frequencies': dict(token_counts.most_common(100)),
        'vocabulary': [sp.id_to_piece(i) for i in range(sp.get_piece_size())]
    }
    
    with open('data/processed/shakespeare_subword_vocab.json', 'w', encoding='utf-8') as f:
        json.dump(vocab_data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved subword vocabulary to shakespeare_subword_vocab.json")

# Run both steps
if __name__ == "__main__":
    train_sentencepiece_model()
    tokenize_shakespeare()