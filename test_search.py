#!/usr/bin/env python3
"""
Quick test script for Hotspur Search functionality
"""

import sys
from pathlib import Path

def test_search_component():
    """Test the search component setup and basic functionality"""
    print("🧪 Testing Hotspur Search Component\n")
    
    # Check if Shakespeare data exists
    shakespeare_file = Path("data/processed/shakespeare_only.txt")
    if not shakespeare_file.exists():
        print(f"❌ Shakespeare text file not found: {shakespeare_file}")
        print("   Please run the data extraction first:")
        print("   python scripts/data/extract_shakespeare.py")
        return False
    
    print(f"✅ Found Shakespeare text: {shakespeare_file}")
    
    # Test imports
    try:
        from hotspur_search.utils.shakespeare_parser import ShakespeareParser
        from hotspur_search.utils.search_engine import ShakespeareSearchEngine
        print("✅ Search modules import successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Try installing dependencies: pip install whoosh streamlit pandas")
        return False
    
    # Test parsing (small sample)
    try:
        parser = ShakespeareParser(context_lines=3)
        print("✅ Parser initialized")
        
        # Parse just first 1000 lines for testing
        with open(shakespeare_file, 'r', encoding='utf-8') as f:
            test_lines = f.readlines()[:1000]
        
        # Write test file
        test_file = Path("hotspur_search/data/test_sample.txt")
        test_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.writelines(test_lines)
        
        segments = parser.parse_file(test_file)
        print(f"✅ Parsed {len(segments)} segments from test sample")
        
        # Clean up
        test_file.unlink()
        
    except Exception as e:
        print(f"❌ Parser error: {e}")
        return False
    
    # Test search engine (if whoosh is available)
    try:
        engine = ShakespeareSearchEngine(index_dir="hotspur_search/test_index")
        print("✅ Search engine initialized")
        
        # Test creating index from sample
        if segments:
            # Save test segments
            import json
            test_segments_file = Path("hotspur_search/data/test_segments.json")
            with open(test_segments_file, 'w', encoding='utf-8') as f:
                json.dump([seg.to_dict() for seg in segments[:100]], f, indent=2)
            
            engine.create_index(str(test_segments_file))
            print("✅ Test search index created")
            
            # Test search
            results = engine.search("love", limit=5)
            print(f"✅ Search test successful - found {len(results)} results")
            
            # Show a sample result
            if results:
                result = results[0]
                print(f"   Sample: \"{result['text'][:50]}...\" from {result['work_title']}")
            
            # Clean up test files
            test_segments_file.unlink()
            import shutil
            shutil.rmtree("hotspur_search/test_index", ignore_errors=True)
            
    except Exception as e:
        print(f"❌ Search engine error: {e}")
        return False
    
    print("\n🎉 Search component test completed successfully!")
    print("\nNext steps:")
    print("1. Run full setup: python hotspur_search/setup_search.py")
    print("2. Launch search interface: streamlit run hotspur_search/streamlit_app/app.py")
    
    return True


def check_dependencies():
    """Check if required dependencies are available"""
    print("📦 Checking dependencies...\n")
    
    required_packages = [
        ('whoosh', 'Full-text search engine'),
        ('streamlit', 'Web interface framework'), 
        ('pandas', 'Data export functionality'),
        ('pathlib', 'File operations'),
        ('json', 'Data serialization'),
        ('re', 'Regular expressions')
    ]
    
    missing = []
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"❌ {package} - {description} (MISSING)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    else:
        print("\n✅ All dependencies available")
        return True


if __name__ == "__main__":
    print("=" * 60)
    print("Hotspur Search Component Test")
    print("=" * 60)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        sys.exit(1)
    
    print()
    
    # Test search component
    if test_search_component():
        sys.exit(0)
    else:
        print("\n❌ Tests failed - please check the errors above")
        sys.exit(1)