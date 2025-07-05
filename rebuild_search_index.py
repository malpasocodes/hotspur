#!/usr/bin/env python3
"""
Rebuild the search index with the fixed Shakespeare segments
"""

import sys
from pathlib import Path

def rebuild_search_index():
    """Rebuild the search index with fixed segments"""
    
    print("🔧 REBUILDING SEARCH INDEX")
    print("=" * 60)
    
    # Import search engine
    sys.path.append(str(Path(__file__).parent))
    from hotspur_search.utils.search_engine import ShakespeareSearchEngine
    
    # Clear old index
    engine = ShakespeareSearchEngine()
    engine.clear_index()
    print("✅ Cleared old search index")
    
    # Use the fixed segments file
    segments_file = Path("hotspur_search/data/shakespeare_segments_fixed.json")
    
    if not segments_file.exists():
        print(f"❌ Fixed segments file not found: {segments_file}")
        print("Please run: python fix_parser.py first")
        return False
    
    # Create new index
    print(f"📚 Creating index from {segments_file}...")
    engine.create_index(str(segments_file))
    
    # Test the new index
    print("\n📊 New Index Statistics:")
    stats = engine.get_statistics()
    print(f"   Documents: {stats.get('total_documents', 0):,}")
    print(f"   Works: {stats.get('works', 0)}")
    print(f"   Size: {stats.get('index_size', 0) / 1024 / 1024:.1f} MB")
    
    # List works
    works = engine.get_works_list()
    print(f"\n📚 Works in index ({len(works)} total):")
    for work in sorted(works):
        print(f"   - {work}")
    
    # Test famous quotes
    print(f"\n🎭 Testing famous quotes:")
    test_queries = [
        "to be or not to be",
        "romeo, romeo", 
        "friends, romans, countrymen",
        "shall I compare thee",
        "all the world's a stage"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Searching: '{query}'")
        results = engine.search(query, limit=3)
        print(f"   Found {len(results)} results")
        
        for i, result in enumerate(results[:2]):
            print(f"   Result {i+1}:")
            print(f"     Work: {result.get('work_title', 'Unknown')}")
            print(f"     Text: {result.get('text', '')[:80]}...")
            if result.get('act') and result.get('scene'):
                print(f"     Location: Act {result['act']}, Scene {result['scene']}")
    
    # Test searching within specific works
    print(f"\n🎯 Testing work-specific searches:")
    hamlet_results = engine.search("prince", work_filter="THE TRAGEDY OF HAMLET, PRINCE OF DENMARK", limit=3)
    print(f"   'prince' in Hamlet: {len(hamlet_results)} results")
    
    romeo_results = engine.search("love", work_filter="THE TRAGEDY OF ROMEO AND JULIET", limit=3)
    print(f"   'love' in Romeo & Juliet: {len(romeo_results)} results")
    
    return True


if __name__ == "__main__":
    if rebuild_search_index():
        print("\n🎉 Search index rebuilt successfully!")
        print("\nNow try the search interface:")
        print("   uv run streamlit run hotspur_search/streamlit_app/app.py")
    else:
        print("\n❌ Failed to rebuild search index")