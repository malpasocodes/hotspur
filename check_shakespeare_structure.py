#!/usr/bin/env python3
"""
Check the structure of the Shakespeare file to understand parsing issues
"""

from pathlib import Path

def analyze_shakespeare_file():
    """Analyze the structure of the Shakespeare file"""
    shakespeare_file = Path("data/processed/shakespeare_only.txt")
    
    print("🔍 ANALYZING SHAKESPEARE FILE STRUCTURE")
    print("=" * 60)
    
    with open(shakespeare_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Total lines: {len(lines):,}")
    print()
    
    # Look for work titles and structure
    print("📚 LOOKING FOR WORK TITLES AND STRUCTURE")
    print("-" * 40)
    
    work_patterns = [
        "THE SONNETS",
        "HAMLET",
        "ROMEO AND JULIET", 
        "MACBETH",
        "OTHELLO",
        "KING LEAR",
        "A MIDSUMMER",
        "ALL'S WELL",
        "ANTONY AND CLEOPATRA",
        "AS YOU LIKE IT",
        "COMEDY OF ERRORS",
        "ACT ",
        "SCENE ",
        "Enter ",
        "Exit"
    ]
    
    found_patterns = {}
    for i, line in enumerate(lines[:1000]):  # Check first 1000 lines
        line_clean = line.strip().upper()
        for pattern in work_patterns:
            if pattern in line_clean:
                if pattern not in found_patterns:
                    found_patterns[pattern] = []
                found_patterns[pattern].append((i+1, line.strip()[:80]))
    
    for pattern, occurrences in found_patterns.items():
        print(f"\n'{pattern}' found {len(occurrences)} times:")
        for line_num, content in occurrences[:3]:
            print(f"  Line {line_num}: {content}")
        if len(occurrences) > 3:
            print(f"  ... and {len(occurrences) - 3} more")
    
    # Show the actual beginning of the file
    print(f"\n📄 FIRST 20 LINES OF FILE:")
    print("-" * 40)
    for i, line in enumerate(lines[:20]):
        print(f"{i+1:3d}: {line.rstrip()}")
    
    # Look for work separators
    print(f"\n🔍 LOOKING FOR WORK SEPARATORS:")
    print("-" * 40)
    
    separators = []
    for i, line in enumerate(lines[:2000]):
        line_clean = line.strip()
        # Look for lines that might separate works
        if (line_clean.isupper() and len(line_clean) > 5 and 
            any(word in line_clean for word in ['THE', 'TRAGEDY', 'COMEDY', 'HISTORY'])):
            separators.append((i+1, line_clean))
    
    print(f"Found {len(separators)} potential work separators:")
    for line_num, content in separators[:10]:
        print(f"  Line {line_num}: {content}")
    
    # Check for specific famous quotes
    print(f"\n🎭 LOOKING FOR FAMOUS QUOTES:")
    print("-" * 40)
    
    famous_quotes = [
        "to be or not to be",
        "romeo, romeo",
        "wherefore art thou",
        "friends, romans, countrymen"
    ]
    
    for quote in famous_quotes:
        found = False
        for i, line in enumerate(lines):
            if quote.lower() in line.lower():
                print(f"✅ Found '{quote}' at line {i+1}: {line.strip()[:80]}...")
                found = True
                break
        if not found:
            print(f"❌ Could not find '{quote}'")


if __name__ == "__main__":
    analyze_shakespeare_file()