#!/usr/bin/env python3
"""
Prepare project for deployment - final cleanup and checks
"""

import subprocess
import shutil
from pathlib import Path

def prepare_for_deployment():
    """Final preparation for deployment"""
    
    print("🚀 PREPARING FOR DEPLOYMENT")
    print("=" * 50)
    
    # 1. Remove large files that shouldn't be deployed
    print("1. Cleaning up large files...")
    
    # Remove search index (will be rebuilt on deploy)
    index_dir = Path("hotspur_search/index")
    if index_dir.exists():
        shutil.rmtree(index_dir)
        print("   ✅ Removed search index (will rebuild on deploy)")
    
    # Remove .venv (not needed on Render)
    venv_dir = Path(".venv")
    if venv_dir.exists() and not Path(".venv/.keep").exists():
        print("   ⚠️  .venv directory found - consider removing before git push")
        print("   (Render will create its own virtual environment)")
    
    # 2. Verify critical files exist
    print("\n2. Verifying deployment files...")
    
    required_files = [
        "requirements.txt",
        "build.sh", 
        "hotspur_search/streamlit_app/app.py",
        "data/processed/shakespeare_only.txt",
        "render.yaml",
        "DEPLOYMENT.md"
    ]
    
    all_good = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            all_good = False
    
    # 3. Check git status
    print("\n3. Checking git status...")
    try:
        # Check if we're in a git repo
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            print("   ⚠️  Uncommitted changes found:")
            print(result.stdout)
            print("   Consider committing changes before deployment")
        else:
            print("   ✅ Working directory clean")
            
    except subprocess.CalledProcessError:
        print("   ⚠️  Not a git repository - initialize git first")
        all_good = False
    except FileNotFoundError:
        print("   ⚠️  Git not installed")
    
    # 4. Test local build (optional)
    print("\n4. Testing build process...")
    shakespeare_file = Path("data/processed/shakespeare_only.txt")
    if shakespeare_file.exists():
        size_mb = shakespeare_file.stat().st_size / 1024 / 1024
        print(f"   ✅ Shakespeare data: {size_mb:.1f} MB")
        
        # Quick test of setup script
        try:
            import hotspur_search
            print("   ✅ Search module imports successfully")
        except ImportError as e:
            print(f"   ❌ Import error: {e}")
            all_good = False
    else:
        print("   ❌ Shakespeare data missing")
        all_good = False
    
    # 5. Final recommendations
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 READY FOR DEPLOYMENT!")
        print("\nNext steps:")
        print("1. git add .")
        print("2. git commit -m 'Prepare for deployment'")
        print("3. git push origin main")
        print("4. Deploy to Render using the GitHub repository")
        
        print("\nRender deployment options:")
        print("• Manual: Connect repo at render.com")
        print("• One-click: Add deploy button to README")
        print("• Config file: Use included render.yaml")
        
    else:
        print("⚠️ NOT READY - Fix issues above first")
    
    return all_good


if __name__ == "__main__":
    prepare_for_deployment()