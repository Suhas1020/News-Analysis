# utils/__init__.py
# This file makes utils a Python package.
# utils/__init__.py

from .scraper import fetch_news
from .sentiment import analyze_sentiment
from .tts import generate_tts
from .analysis import compare_sentiment

__all__ = ["extract_news", "analyze_sentiment", "text_to_speech", "compare_articles"]
