#!/usr/bin/env python3
"""
Fix git repository by removing large files that shouldn't be tracked
"""

import subprocess
import shutil
from pathlib import Path

def fix_git_large_files():
    """Remove large files from git and update gitignore"""
    
    print("🔧 FIXING GIT LARGE FILES ISSUE")
    print("=" * 50)
    
    # 1. Remove large files from git tracking
    print("1. Removing large files from git...")
    
    large_files = [
        "hotspur_search/data/shakespeare_segments_fixed.json",
        "hotspur_search/index/",
    ]
    
    for file_path in large_files:
        try:
            # Remove from git index
            result = subprocess.run(['git', 'rm', '-r', '--cached', file_path], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ Removed {file_path} from git tracking")
            else:
                print(f"   ⚠️  {file_path} not in git or already removed")
        except Exception as e:
            print(f"   ⚠️  Error removing {file_path}: {e}")
    
    # 2. Remove the actual large files/directories
    print("\n2. Removing large files from working directory...")
    
    # Remove search index (will be rebuilt on deployment)
    index_dir = Path("hotspur_search/index")
    if index_dir.exists():
        shutil.rmtree(index_dir)
        print("   ✅ Removed hotspur_search/index/")
    
    # Remove large segments file (will be rebuilt from source)
    segments_file = Path("hotspur_search/data/shakespeare_segments_fixed.json")
    if segments_file.exists():
        segments_file.unlink()
        print("   ✅ Removed shakespeare_segments_fixed.json")
    
    # Keep the data directory but remove large files
    data_dir = Path("hotspur_search/data")
    if data_dir.exists():
        for file in data_dir.glob("*.json"):
            if file.stat().st_size > 10 * 1024 * 1024:  # >10MB
                file.unlink()
                print(f"   ✅ Removed large data file: {file.name}")
    
    # 3. Update .gitignore to be more specific
    print("\n3. Updating .gitignore...")
    
    gitignore_path = Path(".gitignore")
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    # Add more specific ignores for search component
    additional_ignores = """
# Search component - generated files (rebuild on deployment)
hotspur_search/index/
hotspur_search/data/*.json
hotspur_search/data/shakespeare_segments*.json

# Large model files
*.seg
*_segments_fixed.json
"""
    
    if "hotspur_search/index/" not in content:
        with open(gitignore_path, 'a') as f:
            f.write(additional_ignores)
        print("   ✅ Updated .gitignore with search component ignores")
    else:
        print("   ✅ .gitignore already contains search ignores")
    
    # 4. Check current git status
    print("\n4. Checking git status...")
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("   Current changes:")
            for line in result.stdout.strip().split('\n'):
                print(f"     {line}")
        else:
            print("   ✅ Working directory clean")
            
    except Exception as e:
        print(f"   ⚠️  Error checking git status: {e}")
    
    # 5. Show what should be committed
    print("\n5. Next steps:")
    print("   1. Review the changes above")
    print("   2. git add .gitignore")
    print("   3. git commit -m 'Remove large files, update gitignore'")
    print("   4. git push origin main")
    
    print("\n📝 Note: Search index and data will be rebuilt on Render deployment")
    print("   The build.sh script handles this automatically")


if __name__ == "__main__":
    fix_git_large_files()