#!/usr/bin/env python3
"""
Verify Hotspur setup is complete and working
"""

import json
from pathlib import Path

def verify_setup():
    """Verify that Hotspur is properly set up"""
    
    print("🔍 HOTSPUR SETUP VERIFICATION")
    print("=" * 50)
    
    checks = []
    
    # 1. Check Shakespeare source data
    shakespeare_file = Path("data/processed/shakespeare_only.txt")
    if shakespeare_file.exists():
        size = shakespeare_file.stat().st_size / 1024 / 1024
        checks.append(("✅", f"Shakespeare source data: {size:.1f} MB"))
    else:
        checks.append(("❌", "Shakespeare source data missing"))
    
    # 2. Check parsed segments
    segments_file = Path("hotspur_search/data/shakespeare_segments_fixed.json")
    if segments_file.exists():
        with open(segments_file, 'r') as f:
            segments = json.load(f)
        works = set(seg['work_title'] for seg in segments)
        checks.append(("✅", f"Parsed segments: {len(segments):,} segments, {len(works)} works"))
    else:
        checks.append(("❌", "Parsed segments missing"))
    
    # 3. Check search index
    index_dir = Path("hotspur_search/index")
    if index_dir.exists() and list(index_dir.glob("*")):
        index_size = sum(f.stat().st_size for f in index_dir.glob("*")) / 1024 / 1024
        checks.append(("✅", f"Search index: {index_size:.1f} MB"))
    else:
        checks.append(("❌", "Search index missing"))
    
    # 4. Test search functionality
    try:
        import sys
        sys.path.append(str(Path(__file__).parent))
        from hotspur_search.utils.search_engine import ShakespeareSearchEngine
        
        engine = ShakespeareSearchEngine()
        stats = engine.get_statistics()
        
        # Test a simple search
        results = engine.search("love", limit=5)
        
        checks.append(("✅", f"Search engine: {stats['total_documents']:,} docs, {len(results)} results for 'love'"))
        
    except Exception as e:
        checks.append(("❌", f"Search engine error: {str(e)[:50]}..."))
    
    # 5. Check dependencies
    deps_ok = True
    required = ['whoosh', 'streamlit', 'pandas']
    for dep in required:
        try:
            __import__(dep)
        except ImportError:
            deps_ok = False
            break
    
    if deps_ok:
        checks.append(("✅", "Dependencies: whoosh, streamlit, pandas"))
    else:
        checks.append(("❌", "Missing dependencies"))
    
    # Print results
    for status, message in checks:
        print(f"{status} {message}")
    
    # Summary
    success_count = sum(1 for status, _ in checks if status == "✅")
    total_checks = len(checks)
    
    print(f"\n📊 SUMMARY: {success_count}/{total_checks} checks passed")
    
    if success_count == total_checks:
        print("\n🎉 HOTSPUR IS READY!")
        print("\nQuick start:")
        print("  uv run streamlit run hotspur_search/streamlit_app/app.py")
        print("\nTry searching for:")
        print('  • "To be, or not to be"')
        print('  • "Romeo, Romeo"') 
        print('  • love')
        print('  • crown (filtered to Hamlet)')
    else:
        print("\n⚠️  SETUP INCOMPLETE")
        print("Run: python hotspur_search/setup_search.py")
        
        if success_count < 3:
            print("Or force rebuild: python force_rebuild.py")


if __name__ == "__main__":
    verify_setup()