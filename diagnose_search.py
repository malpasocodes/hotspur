#!/usr/bin/env python3
"""
Diagnosis script for Hotspur Search issues
"""

import json
import sys
from pathlib import Path

def check_data_files():
    """Check if source data files exist"""
    print("=" * 60)
    print("1. CHECKING DATA FILES")
    print("=" * 60)
    
    # Check original Shakespeare file
    shakespeare_file = Path("data/processed/shakespeare_only.txt")
    if shakespeare_file.exists():
        size = shakespeare_file.stat().st_size / 1024 / 1024
        print(f"✅ Source file exists: {shakespeare_file} ({size:.1f} MB)")
        
        # Check first few lines
        with open(shakespeare_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
        print(f"   File has {len(lines)} lines (showing first few):")
        for i, line in enumerate(lines[:5]):
            print(f"   Line {i+1}: {line.strip()[:80]}...")
    else:
        print(f"❌ Source file missing: {shakespeare_file}")
        return False
    
    return True


def check_parsed_segments():
    """Check if Shakespeare text was parsed correctly"""
    print("\n" + "=" * 60)
    print("2. CHECKING PARSED SEGMENTS")
    print("=" * 60)
    
    segments_file = Path("hotspur_search/data/shakespeare_segments.json")
    
    if not segments_file.exists():
        print(f"❌ Segments file missing: {segments_file}")
        return False
    
    try:
        with open(segments_file, 'r', encoding='utf-8') as f:
            segments = json.load(f)
        
        print(f"✅ Segments file exists with {len(segments)} segments")
        
        if len(segments) == 0:
            print("❌ No segments found in file")
            return False
        
        # Show sample segments
        print("\n📄 Sample segments:")
        for i, segment in enumerate(segments[:3]):
            print(f"\nSegment {i+1}:")
            print(f"  Work: {segment.get('work_title', 'Unknown')}")
            print(f"  Type: {segment.get('work_type', 'Unknown')}")
            print(f"  Text: {segment.get('text', '')[:100]}...")
            print(f"  Line: {segment.get('line_number', 'Unknown')}")
            if segment.get('speaker'):
                print(f"  Speaker: {segment.get('speaker')}")
        
        # Check for famous quotes
        famous_quotes = [
            "to be or not to be",
            "shall I compare thee",
            "romeo romeo"
        ]
        
        print(f"\n🔍 Looking for famous quotes in {len(segments)} segments...")
        for quote in famous_quotes:
            found = False
            for segment in segments:
                if quote.lower() in segment.get('text', '').lower():
                    print(f"✅ Found '{quote}' in: {segment['text'][:60]}...")
                    found = True
                    break
            if not found:
                print(f"❌ Could not find '{quote}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading segments file: {e}")
        return False


def check_search_index():
    """Check if search index was created correctly"""
    print("\n" + "=" * 60)
    print("3. CHECKING SEARCH INDEX")
    print("=" * 60)
    
    index_dir = Path("hotspur_search/index")
    
    if not index_dir.exists():
        print(f"❌ Index directory missing: {index_dir}")
        return False
    
    index_files = list(index_dir.glob("*"))
    if not index_files:
        print(f"❌ No index files found in {index_dir}")
        return False
    
    print(f"✅ Index directory exists with {len(index_files)} files")
    for f in index_files:
        size = f.stat().st_size / 1024
        print(f"   {f.name}: {size:.1f} KB")
    
    # Test search engine
    try:
        sys.path.append(str(Path(__file__).parent))
        from hotspur_search.utils.search_engine import ShakespeareSearchEngine
        
        engine = ShakespeareSearchEngine()
        stats = engine.get_statistics()
        
        print(f"\n📊 Index Statistics:")
        print(f"   Documents: {stats.get('total_documents', 0):,}")
        print(f"   Works: {stats.get('works', 0)}")
        print(f"   Size: {stats.get('index_size', 0) / 1024 / 1024:.1f} MB")
        
        # Get works list
        works = engine.get_works_list()
        print(f"\n📚 Works in index ({len(works)} total):")
        for work in works[:10]:
            print(f"   - {work}")
        if len(works) > 10:
            print(f"   ... and {len(works) - 10} more")
        
        return True, engine
        
    except Exception as e:
        print(f"❌ Error initializing search engine: {e}")
        return False, None


def test_searches(engine):
    """Test actual search functionality"""
    print("\n" + "=" * 60)
    print("4. TESTING SEARCH FUNCTIONALITY")
    print("=" * 60)
    
    test_queries = [
        ("be", "word search"),
        ("to be or not to be", "phrase search"),
        ("love", "theme search"),
        ("Hamlet", "character search")
    ]
    
    for query, description in test_queries:
        print(f"\n🔍 Testing {description}: '{query}'")
        try:
            results = engine.search(query, limit=3)
            print(f"   Found {len(results)} results")
            
            for i, result in enumerate(results[:2]):
                print(f"   Result {i+1}:")
                print(f"     Work: {result.get('work_title', 'Unknown')}")
                print(f"     Text: {result.get('text', '')[:80]}...")
                print(f"     Line: {result.get('line_number', 'Unknown')}")
            
        except Exception as e:
            print(f"   ❌ Search failed: {e}")


def suggest_fixes():
    """Suggest fixes based on diagnosis"""
    print("\n" + "=" * 60)
    print("5. SUGGESTED FIXES")
    print("=" * 60)
    
    print("If searches are empty, try these fixes:")
    print()
    print("🔧 Option 1: Re-run setup with verbose output")
    print("   uv run python hotspur_search/setup_search.py")
    print()
    print("🔧 Option 2: Clear and rebuild index")
    print("   rm -rf hotspur_search/index hotspur_search/data")
    print("   uv run python hotspur_search/setup_search.py")
    print()
    print("🔧 Option 3: Check data extraction")
    print("   uv run python scripts/data/extract_shakespeare.py")
    print()
    print("🔧 Option 4: Test with smaller dataset")
    print("   Create a small test file and try parsing it")


def main():
    """Run complete diagnosis"""
    print("🔍 HOTSPUR SEARCH DIAGNOSIS")
    print("Checking why searches are coming up empty...\n")
    
    # Check each component
    has_data = check_data_files()
    has_segments = check_parsed_segments() if has_data else False
    has_index, engine = check_search_index() if has_segments else (False, None)
    
    if has_index and engine:
        test_searches(engine)
    
    # Summary
    print("\n" + "=" * 60)
    print("DIAGNOSIS SUMMARY")
    print("=" * 60)
    
    print(f"✅ Source data file: {'Yes' if has_data else 'No'}")
    print(f"✅ Parsed segments: {'Yes' if has_segments else 'No'}")
    print(f"✅ Search index: {'Yes' if has_index else 'No'}")
    
    if not (has_data and has_segments and has_index):
        suggest_fixes()
    else:
        print("\n🎉 Everything looks good! Search should be working.")
        print("If searches still come up empty, try different queries or check case sensitivity.")


if __name__ == "__main__":
    main()