"""
Shakespeare Text Parser for Hotspur Search
Parses Shakespeare texts into structured, searchable format
"""

import re
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class TextSegment:
    """Represents a searchable segment of Shakespeare text"""
    work_title: str
    work_type: str  # 'play' or 'sonnet'
    text: str
    line_number: int
    
    # For plays
    act: Optional[int] = None
    scene: Optional[int] = None
    speaker: Optional[str] = None
    
    # For sonnets  
    sonnet_number: Optional[int] = None
    
    # Metadata
    preceding_lines: List[str] = None
    following_lines: List[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage/indexing"""
        return {k: v for k, v in asdict(self).items() if v is not None}


class ShakespeareParser:
    """Parser for Shakespeare texts"""
    
    def __init__(self, context_lines: int = 5):
        """
        Initialize parser
        
        Args:
            context_lines: Number of lines to include before/after for context
        """
        self.context_lines = context_lines
        self.segments: List[TextSegment] = []
        
    def parse_file(self, filepath: Path) -> List[TextSegment]:
        """Parse a Shakespeare text file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Detect type of work
        text_content = ''.join(lines[:100])  # Check first 100 lines
        
        if self._is_play(text_content):
            return self._parse_play(lines)
        elif self._is_sonnet_collection(text_content):
            return self._parse_sonnets(lines)
        else:
            # Try to detect what type it is from content
            return self._parse_generic(lines)
    
    def _is_play(self, text: str) -> bool:
        """Check if text is a play"""
        play_indicators = ['ACT ', 'SCENE ', 'Dramatis Personae', 'Enter ', 'Exit', 'Exeunt']
        return any(indicator in text for indicator in play_indicators)
    
    def _is_sonnet_collection(self, text: str) -> bool:
        """Check if text is sonnets"""
        return 'THE SONNETS' in text or re.search(r'Sonnet [IVXLCDM]+', text)
    
    def _parse_play(self, lines: List[str]) -> List[TextSegment]:
        """Parse a play into segments"""
        segments = []
        current_act = None
        current_scene = None
        current_speaker = None
        work_title = self._extract_title(lines)
        
        # Regular expressions for parsing
        act_pattern = re.compile(r'ACT\s+([IVX]+|\d+)', re.IGNORECASE)
        scene_pattern = re.compile(r'SCENE\s+([IVX]+|\d+)', re.IGNORECASE)
        speaker_pattern = re.compile(r'^([A-Z][A-Z\s]+)\.')  # HAMLET. or KING LEAR.
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Check for act
            act_match = act_pattern.search(line)
            if act_match:
                current_act = self._roman_to_int(act_match.group(1))
                continue
                
            # Check for scene
            scene_match = scene_pattern.search(line)
            if scene_match:
                current_scene = self._roman_to_int(scene_match.group(1))
                continue
                
            # Check for speaker
            speaker_match = speaker_pattern.match(line)
            if speaker_match:
                current_speaker = speaker_match.group(1).strip()
                # Get the actual dialogue (after speaker name)
                dialogue_start = len(speaker_match.group(0))
                if dialogue_start < len(line):
                    dialogue = line[dialogue_start:].strip()
                else:
                    continue
            else:
                # Continuation of previous speaker's dialogue
                dialogue = line
            
            # Skip stage directions (usually in brackets or parentheses)
            if line.startswith('[') or line.startswith('('):
                continue
                
            # Create segment if we have dialogue
            if dialogue and current_speaker:
                preceding = [lines[j].strip() for j in range(max(0, i-self.context_lines), i) if lines[j].strip()]
                following = [lines[j].strip() for j in range(i+1, min(len(lines), i+self.context_lines+1)) if j < len(lines) and lines[j].strip()]
                
                segment = TextSegment(
                    work_title=work_title,
                    work_type='play',
                    text=dialogue,
                    line_number=i + 1,
                    act=current_act,
                    scene=current_scene,
                    speaker=current_speaker,
                    preceding_lines=preceding[-self.context_lines:],
                    following_lines=following[:self.context_lines]
                )
                segments.append(segment)
        
        return segments
    
    def _parse_sonnets(self, lines: List[str]) -> List[TextSegment]:
        """Parse sonnets into segments"""
        segments = []
        current_sonnet = None
        sonnet_lines = []
        work_title = "Shakespeare's Sonnets"
        
        sonnet_pattern = re.compile(r'^\s*([IVXLCDM]+|\d+)\s*\.?\s*$')
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Check if this is a sonnet number
            sonnet_match = sonnet_pattern.match(line_stripped)
            if sonnet_match:
                # Save previous sonnet if exists
                if current_sonnet and sonnet_lines:
                    segments.extend(self._create_sonnet_segments(
                        current_sonnet, sonnet_lines, work_title, i - len(sonnet_lines)
                    ))
                
                # Start new sonnet
                current_sonnet = self._roman_to_int(sonnet_match.group(1))
                sonnet_lines = []
            elif current_sonnet and line_stripped:
                # Add line to current sonnet
                sonnet_lines.append((i, line_stripped))
        
        # Don't forget the last sonnet
        if current_sonnet and sonnet_lines:
            segments.extend(self._create_sonnet_segments(
                current_sonnet, sonnet_lines, work_title, len(lines) - len(sonnet_lines)
            ))
        
        return segments
    
    def _create_sonnet_segments(self, sonnet_num: int, lines: List[Tuple[int, str]], 
                               work_title: str, start_idx: int) -> List[TextSegment]:
        """Create segments for a sonnet"""
        segments = []
        
        for idx, (line_idx, text) in enumerate(lines):
            preceding = [lines[j][1] for j in range(max(0, idx-self.context_lines), idx)]
            following = [lines[j][1] for j in range(idx+1, min(len(lines), idx+self.context_lines+1))]
            
            segment = TextSegment(
                work_title=work_title,
                work_type='sonnet',
                text=text,
                line_number=line_idx + 1,
                sonnet_number=sonnet_num,
                preceding_lines=preceding,
                following_lines=following
            )
            segments.append(segment)
        
        return segments
    
    def _parse_generic(self, lines: List[str]) -> List[TextSegment]:
        """Parse generic text when type cannot be determined"""
        segments = []
        work_title = self._extract_title(lines)
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            preceding = [lines[j].strip() for j in range(max(0, i-self.context_lines), i) if lines[j].strip()]
            following = [lines[j].strip() for j in range(i+1, min(len(lines), i+self.context_lines+1)) if j < len(lines) and lines[j].strip()]
            
            segment = TextSegment(
                work_title=work_title,
                work_type='text',
                text=line,
                line_number=i + 1,
                preceding_lines=preceding[-self.context_lines:],
                following_lines=following[:self.context_lines]
            )
            segments.append(segment)
        
        return segments
    
    def _extract_title(self, lines: List[str]) -> str:
        """Try to extract work title from beginning of file"""
        # Look for title patterns in first 20 lines
        for line in lines[:20]:
            line = line.strip()
            # Common title patterns
            if line and not any(skip in line for skip in ['Project Gutenberg', 'http', 'www']):
                if line.isupper() or (len(line) > 10 and line[0].isupper()):
                    return line
        return "Unknown Work"
    
    def _roman_to_int(self, roman: str) -> int:
        """Convert Roman numeral to integer"""
        # Handle if it's already an integer
        if roman.isdigit():
            return int(roman)
            
        roman_values = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }
        
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
    
    def save_segments(self, segments: List[TextSegment], output_path: Path):
        """Save parsed segments to JSON file"""
        data = [segment.to_dict() for segment in segments]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(segments)} segments to {output_path}")


def parse_shakespeare_corpus(input_file: Path, output_dir: Path, context_lines: int = 5):
    """Parse the complete Shakespeare corpus"""
    parser = ShakespeareParser(context_lines=context_lines)
    
    print(f"Parsing {input_file}...")
    segments = parser.parse_file(input_file)
    
    # Save parsed segments
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'shakespeare_segments.json'
    parser.save_segments(segments, output_file)
    
    # Print statistics
    print(f"\nParsing complete!")
    print(f"Total segments: {len(segments)}")
    
    # Group by work
    works = {}
    for seg in segments:
        work = seg.work_title
        if work not in works:
            works[work] = 0
        works[work] += 1
    
    print(f"\nWorks found: {len(works)}")
    for work, count in sorted(works.items()):
        print(f"  - {work}: {count} segments")
    
    return segments


if __name__ == "__main__":
    # Test the parser
    input_file = Path("data/processed/shakespeare_only.txt")
    output_dir = Path("hotspur_search/data")
    
    if input_file.exists():
        parse_shakespeare_corpus(input_file, output_dir)
    else:
        print(f"Input file not found: {input_file}")