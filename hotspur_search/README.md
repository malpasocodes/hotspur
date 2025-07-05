# Hotspur Search Component

A sophisticated search interface for Shakespeare's complete works, designed for scholars, students, and enthusiasts.

## Features

### 🔍 Advanced Search Capabilities
- **Word search**: Find all occurrences of any word
- **Phrase search**: Search for exact phrases with quotes
- **Regular expressions**: Advanced pattern matching
- **Fuzzy matching**: Find approximate matches for typos
- **Case sensitivity options**: Control exact vs. flexible matching

### 📚 Comprehensive Coverage
- **All Shakespeare works**: Plays, sonnets, and complete corpus
- **Contextual results**: See surrounding lines for better understanding
- **Metadata**: Work titles, act/scene numbers, speakers, line numbers
- **Line-by-line indexing**: Precise reference for citations

### 🎓 Scholar-Friendly Features
- **Export functionality**: Download results as CSV, JSON, or text
- **Citation format**: Easy copy-paste citations
- **Search history**: Track your research queries
- **Statistics**: Index information and search metrics

### 🖥️ User Interface
- **Streamlit web app**: Clean, intuitive interface
- **Quick searches**: Pre-defined searches for common phrases
- **Customizable context**: Adjust number of surrounding lines
- **Work filtering**: Search within specific plays or sonnets

## Quick Start

### 1. Setup
```bash
# From the project root directory
cd hotspur_search
python setup_search.py
```

This will:
- Install required dependencies
- Parse Shakespeare texts into searchable format
- Create the search index
- Test the functionality

### 2. Launch Search Interface
```bash
# Start the Streamlit app
streamlit run streamlit_app/app.py
```

### 3. Use the Search
- Open your web browser to the URL shown (usually http://localhost:8501)
- Enter a word or phrase to search
- Use the sidebar to filter by work and adjust options
- Export results for research use

## Search Examples

### Basic Word Search
```
Query: "love"
Results: All occurrences of the word "love" across all works
```

### Phrase Search
```
Query: "to be or not to be"
Results: Exact matches of this famous phrase
```

### Regular Expression
```
Query: "love.*death"
Results: Lines containing "love" followed by "death"
```

### Work-Specific Search
```
Query: "crown"
Filter: "Hamlet"
Results: All mentions of "crown" in Hamlet only
```

## API Usage

You can also use the search engine programmatically:

```python
from hotspur_search import ShakespeareSearchEngine

# Initialize search engine
engine = ShakespeareSearchEngine()

# Search for a phrase
results = engine.search(
    query_text="eye",
    work_filter=None,  # Search all works
    search_type="any",  # Word search
    limit=50
)

# Process results
for result in results:
    print(f"Work: {result['work_title']}")
    print(f"Text: {result['text']}")
    print(f"Context: {result['preceding_lines']}")
    print("---")
```

## Architecture

### Components

1. **Parser** (`utils/shakespeare_parser.py`)
   - Processes raw Shakespeare text
   - Identifies plays vs. sonnets
   - Extracts act/scene/speaker information
   - Creates structured segments with context

2. **Search Engine** (`utils/search_engine.py`)
   - Whoosh-based full-text search
   - Multiple search types (word, phrase, regex)
   - Metadata filtering
   - Result highlighting and formatting

3. **Streamlit App** (`streamlit_app/app.py`)
   - Web-based user interface
   - Search controls and options
   - Results display with context
   - Export functionality

### Data Flow

```
Raw Shakespeare Text
         ↓
    Parser (segments)
         ↓
   Search Index (Whoosh)
         ↓
   Search Engine API
         ↓
   Streamlit Interface
```

## File Structure

```
hotspur_search/
├── README.md                 # This file
├── setup_search.py          # Setup script
├── requirements.txt         # Dependencies
├── __init__.py             # Module initialization
├── data/                   # Parsed data storage
│   └── shakespeare_segments.json
├── index/                  # Search index files
│   ├── _MAIN_*.toc
│   └── ...
├── utils/                  # Core components
│   ├── __init__.py
│   ├── shakespeare_parser.py
│   └── search_engine.py
└── streamlit_app/          # Web interface
    └── app.py
```

## Performance

### Index Statistics
- **Documents**: ~200,000 text segments
- **Works**: 37+ plays and sonnet collections
- **Index size**: ~50-100 MB
- **Search speed**: <200ms for most queries

### Search Capabilities
- **Exact matches**: Instant results
- **Phrase search**: <100ms
- **Fuzzy matching**: <500ms
- **Regular expressions**: <1s

## Troubleshooting

### Common Issues

1. **"Shakespeare text file not found"**
   - Ensure `data/processed/shakespeare_only.txt` exists
   - Run the data extraction script from the main project

2. **"Module not found" errors**
   - Run `python setup_search.py` to install dependencies
   - Make sure you're in the project root directory

3. **Search index errors**
   - Delete the `index/` directory and re-run setup
   - Check file permissions

4. **Streamlit won't start**
   - Install streamlit: `pip install streamlit`
   - Check port availability (default 8501)

### Performance Tips

1. **Large result sets**: Use the limit parameter to avoid slow responses
2. **Regex searches**: Be specific to avoid scanning entire corpus
3. **Context lines**: Reduce for faster rendering of many results

## Future Enhancements

### Planned Features
- [ ] Semantic search using embeddings
- [ ] Character-specific search filters
- [ ] Theme and motif tracking
- [ ] Cross-reference analysis
- [ ] Annotation system
- [ ] API endpoints for external integration

### Technical Improvements
- [ ] Caching for common queries
- [ ] Database backend for metadata
- [ ] Advanced highlighting
- [ ] Search suggestions and autocomplete

## Contributing

Contributions welcome! Areas for improvement:
- Parser accuracy for different text formats
- Search result ranking algorithms
- UI/UX enhancements
- Performance optimizations
- Additional export formats

## Dependencies

- **whoosh**: Full-text search engine
- **streamlit**: Web application framework
- **pandas**: Data manipulation for exports
- **pathlib**: File system operations
- **json/re**: Text processing utilities