#!/usr/bin/env python3
"""
Force rebuild the search index completely
"""

import shutil
import sys
from pathlib import Path

def force_rebuild():
    """Force rebuild everything from scratch"""
    
    print("🧹 FORCE REBUILDING SEARCH SYSTEM")
    print("=" * 60)
    
    # 1. Delete old index and data
    index_dir = Path("hotspur_search/index")
    data_dir = Path("hotspur_search/data")
    
    if index_dir.exists():
        shutil.rmtree(index_dir)
        print("✅ Deleted old index directory")
    
    if data_dir.exists():
        shutil.rmtree(data_dir)
        print("✅ Deleted old data directory")
    
    # 2. Re-parse with fixed parser
    print("\n📖 Re-parsing Shakespeare with fixed parser...")
    
    # Import and run the fixed parser
    sys.path.append(str(Path(__file__).parent))
    
    # Re-import to make sure we get fresh modules
    if 'fix_parser' in sys.modules:
        del sys.modules['fix_parser']
    
    import fix_parser
    segments_file = fix_parser.reparse_shakespeare()
    
    print(f"✅ Parsing complete: {segments_file}")
    
    # 3. Create fresh search engine and index
    print("\n🔍 Creating fresh search index...")
    
    # Clear any cached modules
    for module in list(sys.modules.keys()):
        if 'hotspur_search' in module:
            del sys.modules[module]
    
    from hotspur_search.utils.search_engine import ShakespeareSearchEngine
    
    # Create completely new engine
    engine = ShakespeareSearchEngine()
    
    # Make sure index directory is created fresh
    if engine.index_dir.exists():
        shutil.rmtree(engine.index_dir)
    engine.index_dir.mkdir(parents=True, exist_ok=True)
    
    # Create index from fixed segments
    engine.create_index(str(segments_file))
    
    # 4. Test the new index
    print("\n🧪 Testing new index...")
    
    stats = engine.get_statistics()
    print(f"   Documents: {stats.get('total_documents', 0):,}")
    print(f"   Works: {stats.get('works', 0)}")
    
    works = engine.get_works_list()
    print(f"   Work list: {works[:5]}...")
    
    # Test searches
    print(f"\n🔍 Testing searches:")
    
    # Test simple word
    results = engine.search("the", limit=3)
    print(f"   'the': {len(results)} results")
    if results:
        print(f"     Sample: {results[0]['text'][:50]}... from {results[0]['work_title']}")
    
    # Test famous quote
    results = engine.search("to be or not to be", limit=3)
    print(f"   'to be or not to be': {len(results)} results")
    if results:
        print(f"     Sample: {results[0]['text'][:80]}...")
    
    # Test another quote
    results = engine.search("romeo", limit=3)
    print(f"   'romeo': {len(results)} results")
    if results:
        print(f"     Sample: {results[0]['text'][:50]}... from {results[0]['work_title']}")
    
    return True


if __name__ == "__main__":
    try:
        if force_rebuild():
            print("\n🎉 FORCE REBUILD COMPLETE!")
            print("\nNow try the search interface:")
            print("   uv run streamlit run hotspur_search/streamlit_app/app.py")
        else:
            print("\n❌ Force rebuild failed")
    except Exception as e:
        print(f"\n❌ Error during force rebuild: {e}")
        import traceback
        traceback.print_exc()