#!/usr/bin/env python3
"""
Fix work filtering by updating the search engine schema
"""

import sys
import shutil
from pathlib import Path

def fix_work_filtering():
    """Fix the work filtering issue by updating search schema"""
    
    print("🔧 FIXING WORK FILTERING ISSUE")
    print("=" * 60)
    
    print("Problem identified: work_title field is TEXT type (tokenized)")
    print("Solution: Change to ID type (exact matching) and rebuild index")
    
    # 1. First, let's check the current schema
    sys.path.append(str(Path(__file__).parent))
    from hotspur_search.utils.search_engine import ShakespeareSearchEngine
    
    # 2. Create a fixed search engine class
    print("\n📝 Creating fixed search engine...")
    
    # Read the current search engine file
    search_engine_file = Path("hotspur_search/utils/search_engine.py")
    with open(search_engine_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the schema definition
    old_schema = """        # Define schema for Shakespeare texts
        self.schema = Schema(
            # Unique identifier
            id=ID(stored=True, unique=True),
            
            # Text content (searchable)
            text=TEXT(stored=True, analyzer=None),  # Main text
            text_lower=TEXT(stored=False),  # Lowercase for case-insensitive search
            
            # Metadata (stored and some searchable)
            work_title=TEXT(stored=True, field_boost=2.0),"""
    
    new_schema = """        # Define schema for Shakespeare texts
        self.schema = Schema(
            # Unique identifier
            id=ID(stored=True, unique=True),
            
            # Text content (searchable)
            text=TEXT(stored=True, analyzer=None),  # Main text
            text_lower=TEXT(stored=False),  # Lowercase for case-insensitive search
            
            # Metadata (stored and some searchable)
            work_title=ID(stored=True),  # Changed from TEXT to ID for exact matching"""
    
    if old_schema in content:
        new_content = content.replace(old_schema, new_schema)
        
        # Create backup
        backup_file = search_engine_file.with_suffix('.py.backup')
        shutil.copy(search_engine_file, backup_file)
        print(f"✅ Created backup: {backup_file}")
        
        # Write fixed content
        with open(search_engine_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Updated search engine schema")
    else:
        print("⚠️  Schema pattern not found - may already be fixed")
    
    # 3. Clear and rebuild the index
    print("\n🧹 Clearing old index...")
    index_dir = Path("hotspur_search/index")
    if index_dir.exists():
        shutil.rmtree(index_dir)
        print("✅ Cleared old index")
    
    # 4. Rebuild with fixed schema
    print("\n🔍 Rebuilding search index with fixed schema...")
    
    # Clear cached modules to get fresh import
    for module in list(sys.modules.keys()):
        if 'hotspur_search' in module:
            del sys.modules[module]
    
    # Import fresh search engine
    from hotspur_search.utils.search_engine import ShakespeareSearchEngine
    
    # Create new index
    engine = ShakespeareSearchEngine()
    segments_file = Path("hotspur_search/data/shakespeare_segments_fixed.json")
    
    if segments_file.exists():
        engine.create_index(str(segments_file))
        print("✅ Index rebuilt with fixed schema")
    else:
        print("❌ Segments file not found - run force_rebuild.py first")
        return False
    
    # 5. Test the fix
    print("\n🧪 Testing fixed work filtering...")
    
    # Test basic search
    results = engine.search("love", limit=3)
    print(f"Basic search 'love': {len(results)} results")
    
    # Test work filtering
    works = engine.get_works_list()
    if works:
        test_work = works[0]
        print(f"Testing filter for: '{test_work}'")
        
        filtered_results = engine.search("love", work_filter=test_work, limit=3)
        print(f"Filtered search: {len(filtered_results)} results")
        
        if filtered_results:
            print("✅ Work filtering is now working!")
            for i, result in enumerate(filtered_results[:2]):
                print(f"  Result {i+1}: {result['text'][:50]}...")
        else:
            print("❌ Work filtering still not working")
            
            # Debug further
            print(f"\nDebugging with work: '{test_work}'")
            with engine._index.searcher() as searcher:
                from whoosh.query import Term
                work_query = Term("work_title", test_work)
                work_results = searcher.search(work_query, limit=3)
                print(f"Direct work query: {len(work_results)} results")
    
    return True


if __name__ == "__main__":
    if fix_work_filtering():
        print("\n🎉 WORK FILTERING FIX COMPLETE!")
        print("\nNow test the search interface:")
        print("  uv run streamlit run hotspur_search/streamlit_app/app.py")
        print("\nTry:")
        print("  1. Search for 'love' with 'All Works' - should work")
        print("  2. Search for 'love' filtered to 'THE TRAGEDY OF ROMEO AND JULIET' - should now work!")
    else:
        print("\n❌ Fix failed - check error messages above")