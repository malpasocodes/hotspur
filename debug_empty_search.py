#!/usr/bin/env python3
"""
Debug why searches are coming up empty
"""

import sys
import json
from pathlib import Path

def debug_empty_search():
    """Debug the empty search issue"""
    
    print("🔍 DEBUGGING EMPTY SEARCH RESULTS")
    print("=" * 60)
    
    # Check if fixed segments file exists and has content
    segments_file = Path("hotspur_search/data/shakespeare_segments_fixed.json")
    print(f"1. Checking segments file: {segments_file}")
    
    if not segments_file.exists():
        print("❌ Fixed segments file doesn't exist")
        return
    
    # Load and check segments
    with open(segments_file, 'r', encoding='utf-8') as f:
        segments = json.load(f)
    
    print(f"✅ Loaded {len(segments)} segments")
    
    # Show sample segments
    print(f"\n2. Sample segments:")
    for i, seg in enumerate(segments[:3]):
        print(f"   Segment {i+1}:")
        print(f"     Work: {seg.get('work_title', 'NO TITLE')}")
        print(f"     Text: {seg.get('text', 'NO TEXT')[:50]}...")
        print(f"     Line: {seg.get('line_number', 'NO LINE')}")
    
    # Check for specific text
    print(f"\n3. Looking for 'to be or not to be' in segments:")
    found_hamlet = False
    for i, seg in enumerate(segments):
        text = seg.get('text', '').lower()
        if 'to be or not to be' in text:
            print(f"✅ Found at segment {i}:")
            print(f"   Work: {seg.get('work_title')}")
            print(f"   Text: {seg.get('text')}")
            found_hamlet = True
            break
    
    if not found_hamlet:
        print("❌ 'to be or not to be' not found in segments")
        
        # Look for any 'to be' 
        print("   Looking for any 'to be'...")
        for i, seg in enumerate(segments[:1000]):  # Check first 1000
            text = seg.get('text', '').lower()
            if 'to be' in text:
                print(f"   Found 'to be' in: {seg.get('text')[:80]}...")
                break
    
    # Check search engine
    print(f"\n4. Testing search engine directly:")
    try:
        sys.path.append(str(Path(__file__).parent))
        from hotspur_search.utils.search_engine import ShakespeareSearchEngine
        
        engine = ShakespeareSearchEngine()
        
        # Check if index exists
        if not engine._index_exists():
            print("❌ Search index doesn't exist")
            return
        
        # Get stats
        stats = engine.get_statistics()
        print(f"   Index documents: {stats.get('total_documents', 0):,}")
        print(f"   Index works: {stats.get('works', 0)}")
        
        # Test very simple search
        print(f"\n5. Testing simple searches:")
        
        # Test single letter
        results = engine.search("a", limit=5)
        print(f"   Search 'a': {len(results)} results")
        
        # Test common word
        results = engine.search("the", limit=5)
        print(f"   Search 'the': {len(results)} results")
        
        # Test 'be'
        results = engine.search("be", limit=5)
        print(f"   Search 'be': {len(results)} results")
        
        if results:
            print(f"   Sample result:")
            r = results[0]
            print(f"     Work: {r.get('work_title', 'NO TITLE')}")
            print(f"     Text: {r.get('text', 'NO TEXT')[:50]}...")
        
        # Check index content directly
        print(f"\n6. Checking index content:")
        with engine._index.searcher() as searcher:
            # Get first few documents
            docs = list(searcher.documents())[:3]
            print(f"   Index has {len(docs)} sample documents:")
            for i, doc in enumerate(docs):
                print(f"   Doc {i+1}:")
                print(f"     ID: {doc.get('id', 'NO ID')}")
                print(f"     Text: {doc.get('text', 'NO TEXT')[:50]}...")
                print(f"     Work: {doc.get('work_title', 'NO WORK')}")
        
    except Exception as e:
        print(f"❌ Search engine error: {e}")
        import traceback
        traceback.print_exc()
    
    # Final recommendation
    print(f"\n" + "=" * 60)
    print("RECOMMENDATIONS:")
    print("=" * 60)
    print("If search is still empty, try:")
    print("1. Delete and rebuild everything:")
    print("   rm -rf hotspur_search/index hotspur_search/data")
    print("   uv run python fix_parser.py")
    print("   uv run python rebuild_search_index.py")
    print()
    print("2. Check Streamlit is using the right index:")
    print("   Check if the Streamlit app is looking in the right directory")


if __name__ == "__main__":
    debug_empty_search()