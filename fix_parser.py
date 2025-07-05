#!/usr/bin/env python3
"""
Fix the Shakespeare parser to handle the actual file structure
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple

def find_actual_content_start(lines: List[str]) -> int:
    """Find where the actual Shakespeare content starts (after table of contents)"""
    
    # Look for patterns that indicate actual play content
    content_indicators = [
        r"^\s*ACT\s+[IVX]+",
        r"^\s*SCENE\s+[IVX]+", 
        r"^\s*Enter\s+",
        r"^\s*[A-Z]+\.",  # Character speaking (e.g., "HAMLET.")
        r"^\s*\d+\s*$",   # Sonnet number alone on line
    ]
    
    for i, line in enumerate(lines):
        # Skip the table of contents section
        if i < 50:  # First ~50 lines are likely TOC
            continue
            
        line_stripped = line.strip()
        
        # Look for content indicators
        for pattern in content_indicators:
            if re.match(pattern, line_stripped):
                print(f"Found content start at line {i+1}: {line_stripped[:50]}...")
                return i
        
        # Also look for Shakespeare's characteristic verse patterns
        if (len(line_stripped) > 20 and 
            not line_stripped.isupper() and
            any(word in line_stripped.lower() for word in ['the', 'and', 'to', 'of', 'in', 'that'])):
            # Check if this looks like actual content (not just a title)
            if i > 50:  # Make sure we're past TOC
                print(f"Found content start at line {i+1}: {line_stripped[:50]}...")
                return i
    
    return 50  # Default fallback


def find_work_boundaries(lines: List[str], start_idx: int) -> List[Tuple[str, int, int]]:
    """Find the boundaries of each work in the file"""
    
    works = []
    current_work = None
    current_start = start_idx
    
    # Common work title patterns
    work_patterns = [
        r"THE SONNETS",
        r"THE TRAGEDY OF (.+)",
        r"THE COMEDY OF (.+)", 
        r"THE HISTORY OF (.+)",
        r"THE LIFE (?:AND DEATH )?OF (.+)",
        r"THE FIRST PART OF (.+)",
        r"THE SECOND PART OF (.+)",
        r"THE THIRD PART OF (.+)",
        r"ALL'S WELL THAT ENDS WELL",
        r"AS YOU LIKE IT",
        r"A MIDSUMMER NIGHT'S DREAM",
        r"LOVE'S LABOUR'S LOST",
        r"THE MERCHANT OF VENICE",
        r"THE TAMING OF THE SHREW",
        r"THE TEMPEST",
        r"TWELFTH NIGHT",
        r"THE WINTER'S TALE",
        r"MUCH ADO ABOUT NOTHING",
        r"MEASURE FOR MEASURE",
        r"THE MERRY WIVES OF WINDSOR",
    ]
    
    for i in range(start_idx, len(lines)):
        line = lines[i].strip()
        
        # Check if this line is a work title
        is_work_title = False
        work_title = None
        
        for pattern in work_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                is_work_title = True
                work_title = line
                break
        
        # If we found a new work title
        if is_work_title:
            # Save previous work if exists
            if current_work:
                works.append((current_work, current_start, i-1))
            
            # Start new work
            current_work = work_title
            current_start = i + 1
            print(f"Found work: {work_title} starting at line {current_start}")
    
    # Don't forget the last work
    if current_work:
        works.append((current_work, current_start, len(lines)-1))
    
    return works


def parse_single_work(lines: List[str], work_title: str, start_idx: int, end_idx: int) -> List[Dict]:
    """Parse a single work into segments"""
    
    segments = []
    current_act = None
    current_scene = None
    current_speaker = None
    
    # Determine work type
    if "SONNET" in work_title.upper():
        work_type = "sonnet"
    else:
        work_type = "play"
    
    # Regular expressions for parsing
    act_pattern = re.compile(r'^\s*ACT\s+([IVX]+|\d+)', re.IGNORECASE)
    scene_pattern = re.compile(r'^\s*SCENE\s+([IVX]+|\d+)', re.IGNORECASE)
    speaker_pattern = re.compile(r'^\s*([A-Z][A-Z\s]+)\.\s*(.*)', re.IGNORECASE)
    sonnet_pattern = re.compile(r'^\s*([IVXLCDM]+|\d+)\s*$')
    
    for i in range(start_idx, end_idx + 1):
        if i >= len(lines):
            break
            
        line = lines[i].strip()
        if not line:
            continue
        
        # Check for act
        act_match = act_pattern.match(line)
        if act_match:
            current_act = roman_to_int(act_match.group(1))
            continue
        
        # Check for scene
        scene_match = scene_pattern.match(line)
        if scene_match:
            current_scene = roman_to_int(scene_match.group(1))
            continue
        
        # Check for sonnet number
        if work_type == "sonnet":
            sonnet_match = sonnet_pattern.match(line)
            if sonnet_match:
                # This is a sonnet number, skip
                continue
        
        # Check for speaker (for plays)
        speaker_match = speaker_pattern.match(line)
        if speaker_match and work_type == "play":
            current_speaker = speaker_match.group(1).strip()
            dialogue = speaker_match.group(2).strip()
            
            if dialogue:  # If there's dialogue on the same line
                line = dialogue
            else:
                continue  # Speaker name only, get dialogue from next line
        
        # Skip stage directions
        if line.startswith('[') or line.startswith('(') or line.startswith('<'):
            continue
        
        # Skip very short lines (likely formatting artifacts)
        if len(line) < 3:
            continue
        
        # Create segment
        segment = {
            'work_title': work_title,
            'work_type': work_type,
            'text': line,
            'line_number': i + 1,
        }
        
        # Add optional fields
        if current_act:
            segment['act'] = current_act
        if current_scene:
            segment['scene'] = current_scene
        if current_speaker:
            segment['speaker'] = current_speaker
        
        # Add context (previous and following lines)
        context_lines = 5
        preceding = []
        for j in range(max(start_idx, i - context_lines), i):
            if j < len(lines) and lines[j].strip():
                preceding.append(lines[j].strip())
        
        following = []
        for j in range(i + 1, min(len(lines), i + context_lines + 1)):
            if j <= end_idx and lines[j].strip():
                following.append(lines[j].strip())
        
        segment['preceding_lines'] = preceding[-context_lines:]
        segment['following_lines'] = following[:context_lines]
        
        segments.append(segment)
    
    return segments


def roman_to_int(roman: str) -> int:
    """Convert Roman numeral to integer"""
    if roman.isdigit():
        return int(roman)
    
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0
    
    for char in reversed(roman.upper()):
        value = roman_values.get(char, 0)
        if value >= prev_value:
            total += value
        else:
            total -= value
        prev_value = value
    
    return total


def reparse_shakespeare():
    """Re-parse the Shakespeare file with the fixed parser"""
    
    print("🔧 FIXING SHAKESPEARE PARSING")
    print("=" * 60)
    
    # Load the file
    shakespeare_file = Path("data/processed/shakespeare_only.txt")
    with open(shakespeare_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Loaded {len(lines):,} lines")
    
    # Find where actual content starts
    content_start = find_actual_content_start(lines)
    print(f"Content starts at line {content_start}")
    
    # Find work boundaries
    works = find_work_boundaries(lines, content_start)
    print(f"Found {len(works)} works")
    
    # Parse each work
    all_segments = []
    for work_title, start_idx, end_idx in works:
        print(f"\nParsing: {work_title} (lines {start_idx}-{end_idx})")
        segments = parse_single_work(lines, work_title, start_idx, end_idx)
        all_segments.extend(segments)
        print(f"  → {len(segments)} segments")
    
    print(f"\nTotal segments: {len(all_segments)}")
    
    # Save new segments
    output_file = Path("hotspur_search/data/shakespeare_segments_fixed.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_segments, f, indent=2, ensure_ascii=False)
    
    print(f"Saved fixed segments to: {output_file}")
    
    # Show some statistics
    works_count = {}
    for segment in all_segments:
        work = segment['work_title']
        works_count[work] = works_count.get(work, 0) + 1
    
    print(f"\nSegments per work:")
    for work, count in sorted(works_count.items()):
        print(f"  {work}: {count:,}")
    
    # Test for famous quotes
    print(f"\n🎭 Testing for famous quotes:")
    test_quotes = ["to be or not to be", "romeo, romeo", "friends, romans"]
    
    for quote in test_quotes:
        found = False
        for segment in all_segments:
            if quote.lower() in segment['text'].lower():
                print(f"✅ Found '{quote}' in {segment['work_title']}")
                print(f"   Text: {segment['text'][:80]}...")
                found = True
                break
        if not found:
            print(f"❌ Still missing '{quote}'")
    
    return output_file


if __name__ == "__main__":
    reparse_shakespeare()