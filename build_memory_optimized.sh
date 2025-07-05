#!/bin/bash
# Memory-optimized build script for Render free tier (512MB limit)

set -e  # Exit on any error

echo "🎭 Building Hotspur (Memory Optimized)..."

# Install only essential dependencies first
echo "📦 Installing minimal dependencies..."
pip install --no-cache-dir whoosh streamlit pandas

# Create directories
echo "📁 Creating directories..."
mkdir -p hotspur_search/data
mkdir -p hotspur_search/index

# Check available memory
echo "💾 Memory status:"
free -h || echo "Memory info not available"

# Process Shakespeare in smaller chunks to save memory
echo "🔍 Setting up search (memory optimized)..."

# Use Python to do memory-efficient setup
python << 'EOF'
import gc
import json
from pathlib import Path
import sys

print("Starting memory-efficient Shakespeare processing...")

# Add current directory to Python path
sys.path.append('.')

try:
    # Process in smaller chunks
    from hotspur_search.utils.shakespeare_parser import ShakespeareParser
    
    print("Parsing Shakespeare with reduced memory usage...")
    parser = ShakespeareParser(context_lines=3)  # Reduced context
    
    # Read file in chunks
    shakespeare_file = Path("data/processed/shakespeare_only.txt")
    if not shakespeare_file.exists():
        print("ERROR: Shakespeare file not found!")
        sys.exit(1)
    
    # Parse with memory management
    segments = parser.parse_file(shakespeare_file)
    print(f"Parsed {len(segments)} segments")
    
    # Save segments in smaller batches
    output_file = Path("hotspur_search/data/shakespeare_segments.json")
    batch_size = 1000
    all_segments = []
    
    for i in range(0, len(segments), batch_size):
        batch = segments[i:i+batch_size]
        all_segments.extend([seg.to_dict() for seg in batch])
        # Force garbage collection between batches
        gc.collect()
        if i % 5000 == 0:
            print(f"Processed {i}/{len(segments)} segments...")
    
    # Save all segments
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_segments, f, separators=(',', ':'))  # Compact JSON
    
    print(f"Saved {len(all_segments)} segments")
    del all_segments, segments
    gc.collect()
    
    # Create search index with memory optimization
    print("Creating search index...")
    from hotspur_search.utils.search_engine import ShakespeareSearchEngine
    
    engine = ShakespeareSearchEngine()
    engine.create_index(str(output_file))
    
    print("✅ Search setup complete!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

# Verify build worked
echo "✅ Verifying build..."
python -c "
import sys
sys.path.append('.')
from hotspur_search.utils.search_engine import ShakespeareSearchEngine
engine = ShakespeareSearchEngine()
stats = engine.get_statistics()
print(f'Index ready: {stats[\"total_documents\"]} documents')
"

echo "🎉 Memory-optimized build complete!"