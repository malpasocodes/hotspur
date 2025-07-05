"""
Whoosh-based search engine for Shakespeare texts
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re

from whoosh import index
from whoosh.fields import Schema, TEXT, ID, NUMERIC, KEYWORD, STORED
from whoosh.qparser import QueryParser, MultifieldParser, FuzzyTermPlugin
from whoosh.query import Term, Phrase, And, Or
from whoosh.highlight import UppercaseFormatter, HtmlFormatter
from whoosh import scoring


class ShakespeareSearchEngine:
    """Search engine for Shakespeare texts using Whoosh"""
    
    def __init__(self, index_dir: str = "hotspur_search/index"):
        """
        Initialize search engine
        
        Args:
            index_dir: Directory to store search index
        """
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        # Define schema for Shakespeare texts
        self.schema = Schema(
            # Unique identifier
            id=ID(stored=True, unique=True),
            
            # Text content (searchable)
            text=TEXT(stored=True, analyzer=None),  # Main text
            text_lower=TEXT(stored=False),  # Lowercase for case-insensitive search
            
            # Metadata (stored and some searchable)
            work_title=TEXT(stored=True, field_boost=2.0),
            work_type=KEYWORD(stored=True),
            line_number=NUMERIC(stored=True),
            
            # Play-specific
            act=NUMERIC(stored=True),
            scene=NUMERIC(stored=True),
            speaker=TEXT(stored=True),
            
            # Sonnet-specific
            sonnet_number=NUMERIC(stored=True),
            
            # Context
            preceding_lines=STORED,
            following_lines=STORED,
            
            # Full segment data
            segment_json=STORED
        )
        
        self._index = None
    
    def create_index(self, segments_file: str):
        """
        Create search index from parsed segments
        
        Args:
            segments_file: Path to JSON file with parsed segments
        """
        print(f"Creating search index from {segments_file}...")
        
        # Load segments
        with open(segments_file, 'r', encoding='utf-8') as f:
            segments = json.load(f)
        
        # Create or open index
        if not self._index_exists():
            self._index = index.create_in(str(self.index_dir), self.schema)
        else:
            self._index = index.open_dir(str(self.index_dir))
        
        # Index segments
        writer = self._index.writer()
        
        for i, segment in enumerate(segments):
            # Create unique ID
            segment_id = f"{segment['work_title']}_{segment['line_number']}_{i}"
            
            # Prepare document
            doc = {
                'id': segment_id,
                'text': segment['text'],
                'text_lower': segment['text'].lower(),
                'work_title': segment['work_title'],
                'work_type': segment.get('work_type', 'unknown'),
                'line_number': segment['line_number'],
                'segment_json': json.dumps(segment)
            }
            
            # Add optional fields
            for field in ['act', 'scene', 'speaker', 'sonnet_number']:
                if field in segment:
                    doc[field] = segment[field]
            
            # Add context
            if 'preceding_lines' in segment:
                doc['preceding_lines'] = json.dumps(segment['preceding_lines'])
            if 'following_lines' in segment:
                doc['following_lines'] = json.dumps(segment['following_lines'])
            
            writer.add_document(**doc)
        
        writer.commit()
        print(f"Indexed {len(segments)} segments")
    
    def search(self, 
               query_text: str,
               work_filter: Optional[str] = None,
               search_type: str = "any",
               case_sensitive: bool = False,
               fuzzy: bool = False,
               limit: int = 100) -> List[Dict]:
        """
        Search Shakespeare texts
        
        Args:
            query_text: Search query (word or phrase)
            work_filter: Filter by specific work title
            search_type: "any" (default), "phrase", or "regex"
            case_sensitive: Whether search is case-sensitive
            fuzzy: Enable fuzzy matching
            limit: Maximum results to return
            
        Returns:
            List of search results with context
        """
        if not self._index:
            self._index = index.open_dir(str(self.index_dir))
        
        results = []
        
        with self._index.searcher(weighting=scoring.BM25F()) as searcher:
            # Determine which field to search
            search_field = "text" if case_sensitive else "text_lower"
            
            # Build query based on search type
            if search_type == "phrase":
                # Phrase search
                parser = QueryParser(search_field, self._index.schema)
                if fuzzy:
                    parser.add_plugin(FuzzyTermPlugin())
                
                # Ensure phrase search by wrapping in quotes
                if not (query_text.startswith('"') and query_text.endswith('"')):
                    query_text = f'"{query_text}"'
                query = parser.parse(query_text.lower() if not case_sensitive else query_text)
                
            elif search_type == "regex":
                # Regular expression search
                # Whoosh doesn't have built-in regex, so we'll do post-filtering
                parser = QueryParser(search_field, self._index.schema)
                # Search for any document containing any word from the query
                words = query_text.split()
                query = parser.parse(" OR ".join(words))
                
            else:  # "any"
                # Default search - any of the words
                parser = QueryParser(search_field, self._index.schema)
                if fuzzy:
                    parser.add_plugin(FuzzyTermPlugin())
                query = parser.parse(query_text.lower() if not case_sensitive else query_text)
            
            # Add work filter if specified
            if work_filter and work_filter != "All Works":
                work_query = Term("work_title", work_filter)
                query = And([query, work_query])
            
            # Execute search
            search_results = searcher.search(query, limit=limit * 2)  # Get extra for regex filtering
            
            # Process results
            for hit in search_results:
                # For regex search, do additional filtering
                if search_type == "regex":
                    try:
                        if not re.search(query_text, hit['text'], 
                                        re.IGNORECASE if not case_sensitive else 0):
                            continue
                    except re.error:
                        # Invalid regex, skip
                        continue
                
                # Parse stored segment data
                segment_data = json.loads(hit['segment_json'])
                
                # Get match positions for highlighting
                if search_type == "regex":
                    matches = list(re.finditer(query_text, hit['text'], 
                                             re.IGNORECASE if not case_sensitive else 0))
                    match_positions = [(m.start(), m.end()) for m in matches]
                else:
                    # For regular search, we can use Whoosh's highlighting
                    match_positions = self._get_match_positions(hit, query_text, case_sensitive)
                
                # Build result
                result = {
                    'work_title': hit['work_title'],
                    'work_type': hit['work_type'],
                    'text': hit['text'],
                    'line_number': hit['line_number'],
                    'match_positions': match_positions,
                    'score': hit.score if hasattr(hit, 'score') else 0
                }
                
                # Add optional fields
                for field in ['act', 'scene', 'speaker', 'sonnet_number']:
                    if field in segment_data:
                        result[field] = segment_data[field]
                
                # Add context
                if 'preceding_lines' in hit:
                    result['preceding_lines'] = json.loads(hit['preceding_lines'])
                else:
                    result['preceding_lines'] = segment_data.get('preceding_lines', [])
                    
                if 'following_lines' in hit:
                    result['following_lines'] = json.loads(hit['following_lines'])
                else:
                    result['following_lines'] = segment_data.get('following_lines', [])
                
                results.append(result)
                
                if len(results) >= limit:
                    break
        
        return results
    
    def get_works_list(self) -> List[str]:
        """Get list of all works in the index"""
        if not self._index:
            self._index = index.open_dir(str(self.index_dir))
        
        works = set()
        with self._index.searcher() as searcher:
            for doc in searcher.all_stored_fields():
                works.add(doc['work_title'])
        
        return sorted(list(works))
    
    def get_statistics(self) -> Dict:
        """Get search index statistics"""
        if not self._index:
            self._index = index.open_dir(str(self.index_dir))
        
        with self._index.searcher() as searcher:
            stats = {
                'total_documents': searcher.doc_count(),
                'works': len(self.get_works_list()),
                'index_size': sum(f.stat().st_size for f in Path(self.index_dir).glob('*'))
            }
        
        return stats
    
    def _index_exists(self) -> bool:
        """Check if index already exists"""
        return index.exists_in(str(self.index_dir))
    
    def _get_match_positions(self, hit, query_text: str, case_sensitive: bool) -> List[Tuple[int, int]]:
        """Get positions of matches in text for highlighting"""
        text = hit['text']
        positions = []
        
        # Simple word/phrase matching
        search_text = query_text if case_sensitive else query_text.lower()
        compare_text = text if case_sensitive else text.lower()
        
        # Find all occurrences
        start = 0
        while True:
            pos = compare_text.find(search_text, start)
            if pos == -1:
                break
            positions.append((pos, pos + len(search_text)))
            start = pos + 1
        
        return positions
    
    def clear_index(self):
        """Clear the search index"""
        if self._index_exists():
            import shutil
            shutil.rmtree(self.index_dir)
            self.index_dir.mkdir(parents=True, exist_ok=True)
            print("Search index cleared")


def create_sample_search_index():
    """Create a sample search index for testing"""
    # Parse Shakespeare text
    from hotspur_search.utils.shakespeare_parser import parse_shakespeare_corpus
    
    input_file = Path("data/processed/shakespeare_only.txt")
    output_dir = Path("hotspur_search/data")
    
    # Parse if needed
    segments_file = output_dir / "shakespeare_segments.json"
    if not segments_file.exists():
        parse_shakespeare_corpus(input_file, output_dir)
    
    # Create search index
    engine = ShakespeareSearchEngine()
    engine.create_index(str(segments_file))
    
    # Print statistics
    stats = engine.get_statistics()
    print(f"\nSearch index created:")
    print(f"  - Total documents: {stats['total_documents']:,}")
    print(f"  - Works indexed: {stats['works']}")
    print(f"  - Index size: {stats['index_size'] / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    create_sample_search_index()