#!/bin/bash
# Ultra-lightweight build for 512MB memory limit

set -e

echo "🪶 Building Hotspur (Ultra Lightweight)..."

# Install minimal dependencies
pip install --no-cache-dir whoosh==2.7.4 streamlit==1.28.1 pandas==2.1.3

# Create directories
mkdir -p hotspur_search/data hotspur_search/index

# Use lightweight Shakespeare data
echo "📚 Using lightweight Shakespeare dataset..."
if [ ! -f "data/processed/shakespeare_lightweight.txt" ]; then
    echo "❌ Lightweight data not found"
    exit 1
fi

# Simple setup with memory management
python << 'EOF'
import sys, gc
sys.path.append('.')

# Use lightweight data
from hotspur_search.utils.shakespeare_parser import ShakespeareParser
parser = ShakespeareParser(context_lines=2)  # Minimal context

# Parse lightweight file
from pathlib import Path
segments = parser.parse_file(Path("data/processed/shakespeare_lightweight.txt"))
print(f"Parsed {len(segments)} segments")

# Save compact segments
import json
compact_segments = []
for seg in segments[:10000]:  # Limit total segments
    compact = {
        'work_title': seg.work_title,
        'text': seg.text,
        'line_number': seg.line_number
    }
    if hasattr(seg, 'speaker') and seg.speaker:
        compact['speaker'] = seg.speaker
    compact_segments.append(compact)

with open("hotspur_search/data/shakespeare_segments.json", 'w') as f:
    json.dump(compact_segments, f, separators=(',', ':'))

del segments, compact_segments
gc.collect()

# Create minimal index
from hotspur_search.utils.search_engine import ShakespeareSearchEngine
engine = ShakespeareSearchEngine()
engine.create_index("hotspur_search/data/shakespeare_segments.json")
print("✅ Lightweight build complete")
EOF

echo "🎉 Ultra-lightweight Hotspur ready!"
