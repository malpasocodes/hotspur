"""
Hotspur Search Component
A RAG-based search interface for Shakespeare's works
"""

from .utils.shakespeare_parser import ShakespeareParser, parse_shakespeare_corpus
from .utils.search_engine import ShakespeareSearchEngine

__version__ = "0.1.0"
__all__ = ["ShakespeareParser", "ShakespeareSearchEngine", "parse_shakespeare_corpus"]