"""
Hotspur Shakespeare Search - Streamlit App
A scholarly search interface for Shakespeare's complete works
"""

import streamlit as st
import json
from pathlib import Path
import sys
import pandas as pd
from datetime import datetime
import re

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from hotspur_search.utils.search_engine import ShakespeareSearchEngine
from hotspur_search.utils.shakespeare_parser import parse_shakespeare_corpus

# Page configuration
st.set_page_config(
    page_title="Hotspur Shakespeare Search",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .search-result {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .match-highlight {
        background-color: #ffd700;
        padding: 2px 4px;
        border-radius: 3px;
        font-weight: bold;
    }
    .context-line {
        color: #666;
        font-style: italic;
        margin: 2px 0;
    }
    .matched-line {
        font-weight: bold;
        margin: 5px 0;
        font-size: 1.1em;
    }
    .work-title {
        color: #1e3a8a;
        font-size: 1.2em;
        font-weight: bold;
    }
    .metadata {
        color: #666;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_search_engine():
    """Load and cache the search engine"""
    engine = ShakespeareSearchEngine()
    
    # Check if index exists, create if not
    if not engine._index_exists():
        with st.spinner("Building search index for the first time... This may take a minute."):
            # Check if parsed segments exist
            segments_file = Path("hotspur_search/data/shakespeare_segments.json")
            if not segments_file.exists():
                # Parse Shakespeare text first
                input_file = Path("data/processed/shakespeare_only.txt")
                if input_file.exists():
                    parse_shakespeare_corpus(input_file, segments_file.parent)
                else:
                    st.error("Shakespeare text file not found. Please ensure data/processed/shakespeare_only.txt exists.")
                    return None
            
            # Create index
            engine.create_index(str(segments_file))
    
    return engine


def highlight_matches(text: str, positions: list) -> str:
    """Highlight match positions in text"""
    if not positions:
        return text
    
    # Sort positions by start index
    positions = sorted(positions, key=lambda x: x[0])
    
    # Build highlighted text
    result = []
    last_end = 0
    
    for start, end in positions:
        # Add text before match
        result.append(text[last_end:start])
        # Add highlighted match
        result.append(f'<span class="match-highlight">{text[start:end]}</span>')
        last_end = end
    
    # Add remaining text
    result.append(text[last_end:])
    
    return ''.join(result)


def format_location(result: dict) -> str:
    """Format the location information for a result"""
    parts = []
    
    if result.get('act'):
        parts.append(f"Act {result['act']}")
    if result.get('scene'):
        parts.append(f"Scene {result['scene']}")
    if result.get('sonnet_number'):
        parts.append(f"Sonnet {result['sonnet_number']}")
    
    parts.append(f"Line {result['line_number']}")
    
    return " • ".join(parts)


def export_results(results: list, query: str, format: str = "csv"):
    """Export search results in various formats"""
    if format == "csv":
        # Convert to DataFrame
        df_data = []
        for r in results:
            df_data.append({
                'Work': r['work_title'],
                'Location': format_location(r),
                'Speaker': r.get('speaker', ''),
                'Text': r['text'],
                'Line Number': r['line_number']
            })
        
        df = pd.DataFrame(df_data)
        return df.to_csv(index=False)
    
    elif format == "json":
        export_data = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'total_results': len(results),
            'results': results
        }
        return json.dumps(export_data, indent=2)
    
    elif format == "txt":
        lines = [f"Shakespeare Search Results for: {query}"]
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Total matches: {len(results)}\n")
        
        for i, r in enumerate(results, 1):
            lines.append(f"--- Result {i} ---")
            lines.append(f"Work: {r['work_title']}")
            lines.append(f"Location: {format_location(r)}")
            if r.get('speaker'):
                lines.append(f"Speaker: {r['speaker']}")
            lines.append(f"Text: {r['text']}")
            lines.append("")
        
        return '\n'.join(lines)


def main():
    # Title and description
    st.title("🎭 Hotspur Shakespeare Search")
    st.markdown("*An intelligent search interface for Shakespeare scholars and enthusiasts*")
    
    # Load search engine
    engine = load_search_engine()
    if not engine:
        st.stop()
    
    # Get list of works
    works_list = ["All Works"] + engine.get_works_list()
    
    # Sidebar for search options
    with st.sidebar:
        st.header("Search Options")
        
        # Work selection
        selected_work = st.selectbox(
            "Select Work",
            works_list,
            help="Filter results by specific work"
        )
        
        # Search type
        search_type = st.radio(
            "Search Type",
            ["Any words", "Exact phrase", "Regular expression"],
            help="Choose how to interpret your search query"
        )
        
        # Advanced options
        with st.expander("Advanced Options"):
            case_sensitive = st.checkbox("Case sensitive", value=False)
            fuzzy_search = st.checkbox("Fuzzy matching", value=False, 
                                     help="Find approximate matches")
            context_lines = st.slider("Context lines", 1, 10, 5,
                                    help="Number of lines to show before and after matches")
            max_results = st.slider("Maximum results", 10, 500, 100)
        
        # Statistics
        st.divider()
        stats = engine.get_statistics()
        st.metric("Total Lines Indexed", f"{stats['total_documents']:,}")
        st.metric("Works Available", stats['works'])
    
    # Main search interface
    col1, col2 = st.columns([5, 1])
    
    with col1:
        query = st.text_input(
            "Search Shakespeare's Works",
            placeholder='Enter a word (e.g., "love") or phrase (e.g., "to be or not to be")',
            help="Search across all of Shakespeare's texts"
        )
    
    with col2:
        st.write("")  # Spacing
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # Search history in session state
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    
    # Perform search
    if search_button and query:
        # Add to search history
        if query not in st.session_state.search_history:
            st.session_state.search_history.insert(0, query)
            st.session_state.search_history = st.session_state.search_history[:10]
        
        # Map search type to engine parameter
        search_type_map = {
            "Any words": "any",
            "Exact phrase": "phrase",
            "Regular expression": "regex"
        }
        
        # Perform search
        with st.spinner("Searching..."):
            results = engine.search(
                query_text=query,
                work_filter=selected_work if selected_work != "All Works" else None,
                search_type=search_type_map[search_type],
                case_sensitive=case_sensitive,
                fuzzy=fuzzy_search,
                limit=max_results
            )
        
        # Display results
        if results:
            # Results header
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.success(f"Found {len(results)} matches for \"{query}\"")
            with col2:
                # Export functionality
                export_format = st.selectbox("Export as:", ["CSV", "JSON", "TXT"], key="export_format")
            with col3:
                export_data = export_results(results, query, export_format.lower())
                st.download_button(
                    label=f"Download {export_format}",
                    data=export_data,
                    file_name=f"shakespeare_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format.lower()}",
                    mime=f"text/{export_format.lower()}"
                )
            
            # Display each result
            for i, result in enumerate(results):
                with st.container():
                    # Work and location info
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f'<p class="work-title">{result["work_title"]}</p>', 
                                  unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<p class="metadata">{format_location(result)}</p>', 
                                  unsafe_allow_html=True)
                    
                    # Speaker info (if available)
                    if result.get('speaker'):
                        st.markdown(f'<p class="metadata">Speaker: **{result["speaker"]}**</p>', 
                                  unsafe_allow_html=True)
                    
                    # Display context
                    context_container = st.container()
                    with context_container:
                        # Preceding lines
                        for line in result.get('preceding_lines', [])[-context_lines:]:
                            st.markdown(f'<p class="context-line">{line}</p>', unsafe_allow_html=True)
                        
                        # Matched line with highlighting
                        highlighted_text = highlight_matches(result['text'], result['match_positions'])
                        st.markdown(f'<p class="matched-line">{highlighted_text}</p>', 
                                  unsafe_allow_html=True)
                        
                        # Following lines
                        for line in result.get('following_lines', [])[:context_lines]:
                            st.markdown(f'<p class="context-line">{line}</p>', unsafe_allow_html=True)
                    
                    # Action buttons
                    col1, col2, col3 = st.columns([1, 1, 4])
                    with col1:
                        if st.button(f"📋 Copy", key=f"copy_{i}"):
                            # Create citation
                            citation = f"{result['work_title']}, {format_location(result)}: \"{result['text']}\""
                            st.code(citation)
                    
                    st.divider()
        
        else:
            st.warning(f"No matches found for \"{query}\"")
            
            # Suggest alternatives
            if not case_sensitive and not fuzzy_search:
                st.info("💡 Try enabling fuzzy matching in Advanced Options for approximate matches")
    
    # Quick search suggestions when no search is active
    if not query:
        st.subheader("Quick Searches")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Famous Phrases**")
            if st.button("'To be or not to be'"):
                st.session_state.search_text = "to be or not to be"
                st.rerun()
            if st.button("'Romeo, Romeo'"):
                st.session_state.search_text = "Romeo, Romeo"
                st.rerun()
            if st.button("'All the world's a stage'"):
                st.session_state.search_text = "All the world's a stage"
                st.rerun()
        
        with col2:
            st.markdown("**Common Themes**")
            if st.button("Love"):
                st.session_state.search_text = "love"
                st.rerun()
            if st.button("Death"):
                st.session_state.search_text = "death"
                st.rerun()
            if st.button("Crown"):
                st.session_state.search_text = "crown"
                st.rerun()
        
        with col3:
            st.markdown("**Search History**")
            if st.session_state.search_history:
                for hist_query in st.session_state.search_history[:5]:
                    if st.button(f"'{hist_query}'", key=f"hist_{hist_query}"):
                        st.session_state.search_text = hist_query
                        st.rerun()
            else:
                st.caption("No recent searches")


if __name__ == "__main__":
    main()