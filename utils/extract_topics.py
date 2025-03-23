import re
import yake

def extract_topics(text, max_keywords=5):
    """Extracts key topics from text using YAKE"""

    if not text or not text.strip():
        return ["No valid content to extract topics"]

    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    text = re.sub(r"\s+", " ", text).strip()  # Normalize spaces

    if len(text.split()) < 5:
        return ["Not enough content for topic extraction"]

    kw_extractor = yake.KeywordExtractor(
        lan="en",
        n=2,  # Allow up to 2-word phrases
        top=max_keywords,
        dedupLim=0.7
    )

    keywords = kw_extractor.extract_keywords(text)

    # Convert YAKE output to plain Python lists
    extracted_topics = [str(kw[0]) for kw in keywords]

    return extracted_topics if extracted_topics else ["No topics identified"]
