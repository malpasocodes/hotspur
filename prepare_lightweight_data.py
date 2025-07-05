#!/usr/bin/env python3
"""
Prepare lightweight data for deployment - reduce memory usage
"""

import json
from pathlib import Path

def create_lightweight_data():
    """Create a smaller dataset for memory-constrained deployment"""
    
    print("🪶 CREATING LIGHTWEIGHT DATA FOR DEPLOYMENT")
    print("=" * 60)
    
    shakespeare_file = Path("data/processed/shakespeare_only.txt")
    if not shakespeare_file.exists():
        print("❌ Shakespeare source file not found")
        return False
    
    # Read and analyze the source file
    with open(shakespeare_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Source file: {len(lines):,} lines ({shakespeare_file.stat().st_size / 1024 / 1024:.1f} MB)")
    
    # Create a smaller, representative sample
    # Include major works but reduce content to fit memory constraints
    
    major_works = [
        "THE TRAGEDY OF HAMLET, PRINCE OF DENMARK",
        "THE TRAGEDY OF ROMEO AND JULIET", 
        "THE TRAGEDY OF MACBETH",
        "THE TRAGEDY OF OTHELLO, THE MOOR OF VENICE",
        "THE TRAGEDY OF KING LEAR",
        "A MIDSUMMER NIGHT'S DREAM",
        "AS YOU LIKE IT",
        "THE TEMPEST"
    ]
    
    # Find work boundaries and extract key works
    print("📚 Extracting major works for lightweight deployment...")
    
    lightweight_lines = []
    current_work = None
    work_line_count = 0
    max_lines_per_work = 500  # Limit lines per work for memory
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Check if this is a work title
        for work in major_works:
            if work in line_stripped:
                current_work = work
                work_line_count = 0
                lightweight_lines.append(line)
                print(f"   Found: {work}")
                break
        else:
            # Add content if we're in a major work and under line limit
            if current_work and work_line_count < max_lines_per_work:
                if line_stripped and len(line_stripped) > 3:  # Skip very short lines
                    lightweight_lines.append(line)
                    work_line_count += 1
    
    # Save lightweight version
    lightweight_file = Path("data/processed/shakespeare_lightweight.txt")
    with open(lightweight_file, 'w', encoding='utf-8') as f:
        f.writelines(lightweight_lines)
    
    size_mb = lightweight_file.stat().st_size / 1024 / 1024
    print(f"✅ Created lightweight version: {len(lightweight_lines):,} lines ({size_mb:.1f} MB)")
    print(f"   Reduction: {len(lines) - len(lightweight_lines):,} lines saved")
    
    # Create a lightweight build script that uses this smaller file
    lightweight_build = Path("build_lightweight.sh")
    with open(lightweight_build, 'w') as f:
        f.write(f'''#!/bin/bash
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
print(f"Parsed {{len(segments)}} segments")

# Save compact segments
import json
compact_segments = []
for seg in segments[:10000]:  # Limit total segments
    compact = {{
        'work_title': seg.work_title,
        'text': seg.text,
        'line_number': seg.line_number
    }}
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
''')
    
    lightweight_build.chmod(0o755)
    print(f"✅ Created {lightweight_build}")
    
    print(f"\n💡 DEPLOYMENT OPTIONS:")
    print(f"1. Try memory-optimized build: ./build_memory_optimized.sh")  
    print(f"2. Use ultra-lightweight build: ./build_lightweight.sh")
    print(f"3. Upgrade to Render Starter plan ($7/month) for 1GB RAM")
    
    return True


if __name__ == "__main__":
    create_lightweight_data()