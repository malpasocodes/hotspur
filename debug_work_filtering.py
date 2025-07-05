#!/usr/bin/env python3
"""
Debug work filtering issues in search
"""

import sys
from pathlib import Path

def debug_work_filtering():
    """Debug why work-specific filtering returns empty results"""
    
    print("🔍 DEBUGGING WORK FILTERING ISSUES")
    print("=" * 60)
    
    # Import search engine
    sys.path.append(str(Path(__file__).parent))
    from hotspur_search.utils.search_engine import ShakespeareSearchEngine
    
    engine = ShakespeareSearchEngine()
    
    # 1. Check what works are available
    print("1. AVAILABLE WORKS IN INDEX:")
    print("-" * 30)
    works = engine.get_works_list()
    print(f"Total works: {len(works)}")
    for i, work in enumerate(works[:10]):
        print(f"  {i+1}. '{work}'")
    if len(works) > 10:
        print(f"  ... and {len(works) - 10} more")
    
    # 2. Test search without filter
    print(f"\n2. TESTING SEARCH WITHOUT FILTER:")
    print("-" * 30)
    results_all = engine.search("love", limit=5)
    print(f"Search 'love' (no filter): {len(results_all)} results")
    
    if results_all:
        print(f"Sample results:")
        for i, result in enumerate(results_all[:3]):
            print(f"  Result {i+1}: '{result['work_title']}' - {result['text'][:50]}...")
    
    # 3. Test with specific work filters
    print(f"\n3. TESTING WORK-SPECIFIC FILTERS:")
    print("-" * 30)
    
    test_works = [
        "THE TRAGEDY OF HAMLET, PRINCE OF DENMARK",
        "THE TRAGEDY OF ROMEO AND JULIET", 
        "THE TRAGEDY OF MACBETH"
    ]
    
    for work in test_works:
        if work in works:
            print(f"\nTesting filter: '{work}'")
            results = engine.search("love", work_filter=work, limit=5)
            print(f"  Results: {len(results)}")
            
            if results:
                for i, result in enumerate(results[:2]):
                    print(f"    {i+1}. {result['text'][:60]}...")
            else:
                print("    ❌ No results found")
        else:
            print(f"\n❌ Work not found in index: '{work}'")
    
    # 4. Check exact work title matching
    print(f"\n4. CHECKING WORK TITLE MATCHING:")
    print("-" * 30)
    
    # Look at actual work titles in segments
    with engine._index.searcher() as searcher:
        # Get a sample of documents to see work titles
        sample_docs = []
        for doc in searcher.documents():
            sample_docs.append(doc)
            if len(sample_docs) >= 10:
                break
        
        print("Sample work titles in index:")
        unique_titles = set()
        for doc in sample_docs:
            title = doc.get('work_title', 'NO TITLE')
            unique_titles.add(title)
        
        for title in sorted(unique_titles):
            print(f"  Index title: '{title}'")
    
    # 5. Test the actual filtering logic
    print(f"\n5. TESTING FILTERING LOGIC:")
    print("-" * 30)
    
    # Try to search for documents with specific work title directly
    if works:
        test_work = works[0]  # Use first work
        print(f"Testing direct work query for: '{test_work}'")
        
        with engine._index.searcher() as searcher:
            from whoosh.query import Term
            work_query = Term("work_title", test_work)
            work_results = searcher.search(work_query, limit=5)
            
            print(f"  Direct work query results: {len(work_results)}")
            for hit in work_results[:3]:
                print(f"    Found: '{hit['work_title']}' - {hit['text'][:50]}...")
    
    # 6. Test the search engine's filter logic step by step
    print(f"\n6. STEP-BY-STEP FILTER TESTING:")
    print("-" * 30)
    
    if works:
        test_work = works[0]
        print(f"Testing with work: '{test_work}'")
        
        # Try to replicate the search engine's filtering logic
        with engine._index.searcher() as searcher:
            from whoosh.qparser import QueryParser
            from whoosh.query import And, Term
            
            # Build the text query
            parser = QueryParser("text_lower", engine._index.schema)
            text_query = parser.parse("love")
            print(f"  Text query: {text_query}")
            
            # Build the work filter
            work_query = Term("work_title", test_work)
            print(f"  Work query: {work_query}")
            
            # Combine queries
            combined_query = And([text_query, work_query])
            print(f"  Combined query: {combined_query}")
            
            # Execute combined query
            combined_results = searcher.search(combined_query, limit=5)
            print(f"  Combined results: {len(combined_results)}")
            
            if combined_results:
                for hit in combined_results[:2]:
                    print(f"    Result: '{hit['work_title']}' - {hit['text'][:50]}...")


if __name__ == "__main__":
    debug_work_filtering()