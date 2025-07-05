#!/usr/bin/env python3
"""
Check if the project is ready for Render deployment
"""

from pathlib import Path
import subprocess
import sys

def check_render_readiness():
    """Check deployment readiness for Render"""
    
    print("🚀 RENDER DEPLOYMENT READINESS CHECK")
    print("=" * 60)
    
    checks = []
    recommendations = []
    
    # 1. Check for requirements.txt (Render prefers this over pyproject.toml)
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        checks.append(("✅", "requirements.txt exists"))
    else:
        checks.append(("❌", "requirements.txt missing"))
        recommendations.append("Create requirements.txt from pyproject.toml")
    
    # 2. Check for Streamlit app entry point
    streamlit_app = Path("hotspur_search/streamlit_app/app.py")
    if streamlit_app.exists():
        checks.append(("✅", "Streamlit app exists"))
    else:
        checks.append(("❌", "Streamlit app missing"))
    
    # 3. Check for .gitignore
    gitignore = Path(".gitignore")
    if gitignore.exists():
        checks.append(("✅", ".gitignore exists"))
        
        # Check if important items are ignored
        with open(gitignore, 'r') as f:
            content = f.read()
        
        important_ignores = [
            "hotspur_search/index/",
            "hotspur_search/data/",
            "__pycache__/",
            ".env"
        ]
        
        missing_ignores = []
        for ignore in important_ignores:
            if ignore not in content:
                missing_ignores.append(ignore)
        
        if missing_ignores:
            recommendations.append(f"Add to .gitignore: {', '.join(missing_ignores)}")
    else:
        checks.append(("❌", ".gitignore missing"))
        recommendations.append("Create .gitignore")
    
    # 4. Check project size (Render has limits)
    try:
        result = subprocess.run(['du', '-sh', '.'], capture_output=True, text=True)
        size = result.stdout.split()[0]
        checks.append(("ℹ️", f"Project size: {size}"))
        
        # Check for large files
        large_files = []
        for file_path in Path('.').rglob('*'):
            if file_path.is_file():
                size_mb = file_path.stat().st_size / 1024 / 1024
                if size_mb > 100:  # Files larger than 100MB
                    large_files.append(f"{file_path}: {size_mb:.1f}MB")
        
        if large_files:
            checks.append(("⚠️", f"Large files found: {len(large_files)}"))
            for large_file in large_files[:3]:
                recommendations.append(f"Consider excluding: {large_file}")
    except:
        checks.append(("⚠️", "Could not check project size"))
    
    # 5. Check for environment variables needed
    env_vars_needed = [
        "STREAMLIT_SERVER_PORT",
        "STREAMLIT_SERVER_ADDRESS"
    ]
    checks.append(("ℹ️", f"Environment variables needed: {len(env_vars_needed)}"))
    
    # 6. Check if search index can be built on deployment
    segments_file = Path("hotspur_search/data/shakespeare_segments_fixed.json")
    shakespeare_file = Path("data/processed/shakespeare_only.txt")
    
    if shakespeare_file.exists() and segments_file.exists():
        checks.append(("✅", "Search data available for build"))
    elif shakespeare_file.exists():
        checks.append(("⚠️", "Raw data available, needs processing"))
        recommendations.append("Include build script in deployment")
    else:
        checks.append(("❌", "No Shakespeare data found"))
        recommendations.append("Ensure data files are included or downloadable")
    
    # 7. Check for build script
    build_script = Path("build.sh")
    if build_script.exists():
        checks.append(("✅", "Build script exists"))
    else:
        checks.append(("❌", "Build script missing"))
        recommendations.append("Create build.sh for Render deployment")
    
    # 8. Check Python version compatibility
    try:
        python_version = sys.version_info
        if python_version >= (3, 9):
            checks.append(("✅", f"Python {python_version.major}.{python_version.minor} compatible"))
        else:
            checks.append(("⚠️", f"Python {python_version.major}.{python_version.minor} may be too old"))
    except:
        checks.append(("⚠️", "Could not check Python version"))
    
    # Print results
    print("\n📋 DEPLOYMENT READINESS:")
    for status, message in checks:
        print(f"{status} {message}")
    
    # Print recommendations
    if recommendations:
        print(f"\n🔧 RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    
    # Summary
    ready_count = sum(1 for status, _ in checks if status == "✅")
    total_checks = len([c for c in checks if c[0] in ["✅", "❌"]])
    
    print(f"\n📊 READINESS SCORE: {ready_count}/{total_checks}")
    
    if ready_count >= total_checks * 0.8:  # 80% ready
        print("\n🎉 MOSTLY READY FOR DEPLOYMENT!")
        print("Address the recommendations above, then deploy to Render.")
    else:
        print("\n⚠️ NEEDS MORE PREPARATION")
        print("Please address the missing items before deployment.")
    
    return ready_count >= total_checks * 0.8


if __name__ == "__main__":
    check_render_readiness()