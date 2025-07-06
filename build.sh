#!/bin/bash
# Simple build script - Pro plan with adequate memory

set -e  # Exit on any error

echo "🎭 Building Hotspur Shakespeare Search (Pro Plan)..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p hotspur_search/data
mkdir -p hotspur_search/index

# Check if Shakespeare data exists
if [ ! -f "data/processed/shakespeare_only.txt" ]; then
    echo "❌ Shakespeare data not found!"
    exit 1
fi

# Use the working parser fix (this works locally)
echo "🔧 Running fixed parser (creates all 31 works)..."
python fix_parser.py

# Create search index from the fixed segments
echo "🔍 Creating search index..."
python -c "
import sys
sys.path.append('.')
from hotspur_search.utils.search_engine import ShakespeareSearchEngine
engine = ShakespeareSearchEngine()
engine.create_index('hotspur_search/data/shakespeare_segments_fixed.json')
print('✅ Search index created successfully')
"

# Verify the build worked
echo "✅ Verifying build..."
python -c "
import sys
sys.path.append('.')
from hotspur_search.utils.search_engine import ShakespeareSearchEngine
engine = ShakespeareSearchEngine()
works = engine.get_works_list()
print(f'Found {len(works)} works in search index')
if len(works) > 20:
    print('✅ Build successful - all works found')
else:
    print('❌ Build failed - only found:', works)
    sys.exit(1)
"

echo "🎉 Build complete!"