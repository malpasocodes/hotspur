#!/usr/bin/env python3
"""
Setup script for Hotspur Search Component
Parses Shakespeare texts and creates search index
"""

import sys
from pathlib import Path
import subprocess

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from hotspur_search.utils.shakespeare_parser import parse_shakespeare_corpus
from hotspur_search.utils.search_engine import ShakespeareSearchEngine


def install_requirements():
    """Install required packages"""
    print("Installing search component requirements...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    
    return True


def setup_search_component():
    """Set up the search component"""
    print("🎭 Setting up Hotspur Shakespeare Search Component\n")
    
    # Check if Shakespeare text exists
    shakespeare_file = Path("data/processed/shakespeare_only.txt")
    if not shakespeare_file.exists():
        print(f"❌ Shakespeare text file not found: {shakespeare_file}")
        print("Please ensure you have the Shakespeare text file in the data/processed/ directory")
        return False
    
    print(f"✅ Found Shakespeare text: {shakespeare_file}")
    
    # Parse Shakespeare texts
    print("\n📖 Parsing Shakespeare texts...")
    output_dir = Path("hotspur_search/data")
    segments_file = output_dir / "shakespeare_segments.json"
    
    if not segments_file.exists():
        try:
            segments = parse_shakespeare_corpus(shakespeare_file, output_dir)
            print(f"✅ Parsed {len(segments)} text segments")
        except Exception as e:
            print(f"❌ Failed to parse Shakespeare texts: {e}")
            return False
    else:
        print("✅ Shakespeare texts already parsed")
    
    # Create search index
    print("\n🔍 Creating search index...")
    try:
        engine = ShakespeareSearchEngine()
        
        if not engine._index_exists():
            engine.create_index(str(segments_file))
            print("✅ Search index created successfully")
        else:
            print("✅ Search index already exists")
        
        # Test the search
        print("\n🧪 Testing search functionality...")
        results = engine.search("love", limit=5)
        print(f"✅ Search test successful - found {len(results)} results for 'love'")
        
        # Show statistics
        stats = engine.get_statistics()
        print(f"\n📊 Search Index Statistics:")
        print(f"   • Total documents: {stats['total_documents']:,}")
        print(f"   • Works indexed: {stats['works']}")
        print(f"   • Index size: {stats['index_size'] / 1024 / 1024:.1f} MB")
        
    except Exception as e:
        print(f"❌ Failed to create search index: {e}")
        return False
    
    return True


def main():
    """Main setup function"""
    print("Starting Hotspur Search Component setup...\n")
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed - could not install requirements")
        return
    
    # Setup search component
    if setup_search_component():
        print("\n🎉 Hotspur Search Component setup complete!")
        print("\nTo start the search interface, run:")
        print("   streamlit run hotspur_search/streamlit_app/app.py")
        print("\nOr run the search API:")
        print("   python hotspur_search/utils/search_engine.py")
    else:
        print("\n❌ Setup failed - please check the error messages above")


if __name__ == "__main__":
    main()