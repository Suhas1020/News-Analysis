from collections import Counter
from itertools import combinations
import spacy
from urllib.parse import urlparse

try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_key_points(text):
    """Extract key points from text using spaCy."""
    doc = nlp(text)
    
    # Extract named entities
    entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'EVENT', 'TECH', 'MONEY', 'GPE']]
    
    # Extract important noun phrases
    noun_phrases = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) > 1]
    
    # Combine and get unique key points
    key_points = list(set(entities + noun_phrases))
    return key_points[:5]  # Return top 5 key points

def extract_source_from_url(url):
    """Extract source name from URL."""
    try:
        domain = urlparse(url).netloc
        # Remove www. and .com/.org/etc
        source = domain.replace('www.', '').split('.')[0]
        return source.capitalize()
    except:
        return "Unknown Source"

def generate_comparative_analysis(articles):
    """
    Generate comparative analysis between articles.
    Focuses on content differences, key points, and thematic variations.
    """
    if not articles or len(articles) < 2:
        return {
            "article_comparisons": [],
            "key_differences": [],
            "thematic_summary": "Insufficient articles for comparison",
            "source_distribution": {}
        }

    comparisons = []
    all_key_points = set()
    sources = []
    
    # Collect sources and generate comparisons
    for article in articles:
        # Extract source from URL or use provided source
        if article.get('link'):
            source = extract_source_from_url(article['link'])
        else:
            source = article.get('source', 'Unknown Source')
        sources.append(source)
    
    # Generate source distribution
    source_counts = Counter(sources)
    source_distribution = {
        source: count for source, count in source_counts.most_common()
    }
    
    # Generate pairwise comparisons
    for i, (art1, art2) in enumerate(combinations(articles, 2)):
        if i >= 5:  # Limit to 5 comparisons to keep it manageable
            break
            
        # Extract key points from both articles
        points1 = extract_key_points(f"{art1.get('title', '')} {art1.get('content', '')}")
        points2 = extract_key_points(f"{art2.get('title', '')} {art2.get('content', '')}")
        
        # Find unique points in each article
        unique_points1 = set(points1) - set(points2)
        unique_points2 = set(points2) - set(points1)
        
        # Generate impact analysis based on sentiment and content
        sentiment1 = art1.get('sentiment', {}).get('category', 'Neutral')
        sentiment2 = art2.get('sentiment', {}).get('category', 'Neutral')
        
        impact = ""
        if sentiment1 != sentiment2:
            impact = f"Articles present contrasting perspectives: {sentiment1} vs {sentiment2} outlook"
        else:
            impact = f"Articles share a similar {sentiment1.lower()} perspective but focus on different aspects"
        
        comparison = {
            "article_1": {
                "title": art1.get('title', ''),
                "key_points": list(unique_points1)[:3],
                "sentiment": sentiment1,
                "source": extract_source_from_url(art1.get('link', '')) if art1.get('link') else art1.get('source', 'Unknown Source')
            },
            "article_2": {
                "title": art2.get('title', ''),
                "key_points": list(unique_points2)[:3],
                "sentiment": sentiment2,
                "source": extract_source_from_url(art2.get('link', '')) if art2.get('link') else art2.get('source', 'Unknown Source')
            },
            "comparison": f"Article 1 focuses on {', '.join(list(unique_points1)[:2])} while Article 2 emphasizes {', '.join(list(unique_points2)[:2])}",
            "impact": impact
        }
        
        comparisons.append(comparison)
        all_key_points.update(unique_points1)
        all_key_points.update(unique_points2)
    
    # Generate key differences summary
    key_differences = []
    if all_key_points:
        key_differences = list(all_key_points)[:5]
    
    # Generate thematic summary
    total_articles = len(articles)
    positive_count = sum(1 for a in articles if a.get('sentiment', {}).get('category') == 'Positive')
    negative_count = sum(1 for a in articles if a.get('sentiment', {}).get('category') == 'Negative')
    
    thematic_summary = (
        f"Analysis of {total_articles} articles from {len(source_distribution)} different sources reveals diverse coverage. "
        f"{positive_count} articles present positive developments, while {negative_count} focus on challenges. "
        f"Key themes include: {', '.join(key_differences[:3])}"
    )
    
    return {
        "article_comparisons": comparisons,
        "key_differences": key_differences,
        "thematic_summary": thematic_summary,
        "source_distribution": source_distribution
    }
