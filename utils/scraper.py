import requests
import nltk
from datetime import datetime
import re
import feedparser
from bs4 import BeautifulSoup
import html
from collections import Counter
from itertools import combinations
import spacy

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """Clean and normalize text content."""
    if not text:
        return ""
    # Decode HTML entities
    text = html.unescape(text)
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text

def extract_summary(text, max_sentences=3):
    """Extract a summary from text using NLTK."""
    try:
        sentences = nltk.sent_tokenize(text)
        return ' '.join(sentences[:max_sentences])
    except:
        return text[:200] + "..." if len(text) > 200 else text

def extract_topics(text):
    """Extract main topics from text using spaCy."""
    doc = nlp(text)
    
    # Extract named entities
    entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'EVENT', 'TECH']]
    
    # Extract noun phrases
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    
    # Extract important words (nouns and proper nouns)
    important_words = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
    
    # Combine and get most common topics
    all_topics = entities + noun_phrases + important_words
    topic_counter = Counter(all_topics)
    
    # Return top 5 most common topics
    return [topic for topic, _ in topic_counter.most_common(5)]

def compare_articles(articles):
    """Compare articles and generate insights."""
    if len(articles) < 2:
        return None
        
    coverage_differences = []
    all_topics = set()
    articles_topics = []
    
    # Extract topics for each article
    for article in articles:
        combined_text = f"{article['title']} {article['content']}"
        topics = extract_topics(combined_text)
        articles_topics.append(topics)
        all_topics.update(topics)
    
    # Generate comparisons between pairs of articles
    for i, (art1, art2) in enumerate(combinations(range(len(articles)), 2)):
        if i >= 5:  # Limit to 5 comparisons
            break
            
        topics1 = set(articles_topics[art1])
        topics2 = set(articles_topics[art2])
        
        # Determine the main focus of each article
        focus1 = next((t for t in topics1 if t.lower() not in ['microsoft', 'company']), list(topics1)[0] if topics1 else "general news")
        focus2 = next((t for t in topics2 if t.lower() not in ['microsoft', 'company']), list(topics2)[0] if topics2 else "general news")
        
        # Generate impact based on the topics
        impact = ""
        if any(t.lower() in ['security', 'hack', 'threat', 'vulnerability', 'attack'] for t in topics1.union(topics2)):
            impact = "This highlights potential security concerns and their implications for Microsoft's systems and users."
        elif any(t.lower() in ['ai', 'copilot', 'intelligence', 'ml'] for t in topics1.union(topics2)):
            impact = "This demonstrates Microsoft's ongoing AI initiatives and their potential impact on the technology industry."
        elif any(t.lower() in ['revenue', 'profit', 'stock', 'market', 'financial'] for t in topics1.union(topics2)):
            impact = "This shows the financial performance and market position of Microsoft in different areas."
        elif any(t.lower() in ['partnership', 'collaboration', 'deal'] for t in topics1.union(topics2)):
            impact = "This indicates Microsoft's strategic partnerships and their potential benefits for stakeholders."
        else:
            impact = f"This reveals different aspects of Microsoft's activities in {focus1} and {focus2}, which could affect various stakeholders."
        
        # Find differences in coverage
        comparison = {
            "Comparison": f"Article {art1 + 1} focuses on {focus1}, while Article {art2 + 1} covers {focus2}.",
            "Impact": impact
        }
        coverage_differences.append(comparison)
    
    # Analyze topic overlap
    common_topics = set.intersection(*map(set, articles_topics))
    unique_topics = set()
    for topics in articles_topics:
        unique_topics.update(set(topics) - common_topics)
    
    # Filter out generic topics
    generic_topics = {'microsoft', 'company', 'news', 'article', 'report'}
    common_topics = {t for t in common_topics if t.lower() not in generic_topics}
    unique_topics = {t for t in unique_topics if t.lower() not in generic_topics}
    
    topic_overlap = {
        "Common Topics": list(common_topics)[:3],
        "Unique Topics": list(unique_topics)[:5]
    }
    
    return {
        "Coverage Differences": coverage_differences,
        "Topic Overlap": topic_overlap
    }

def fetch_news(company_name, num_articles=10):
    """
    Fetch news articles about a company using Google News RSS feed.
    Returns:
        dict: A dictionary containing either:
            - 'articles' and 'analysis' keys with the fetched articles and their analysis
            - 'error' key with an error message if something went wrong
    """
    print(f"Fetching news for {company_name}...")
    
    # Google News RSS feed URL
    base_url = "https://news.google.com/rss/search"
    
    # Try different query formats with proper encoding
    queries = [
        {"q": f"{company_name} company", "desc": "company news"},
        {"q": f"{company_name} business", "desc": "business news"},
        {"q": f"{company_name} news", "desc": "general news"},
        {"q": company_name, "desc": "direct search"}  # Simple company name search
    ]
    
    all_articles = []
    
    for query in queries:
        try:
            # Properly encode the query parameters
            params = {
                "q": query["q"].strip(),
                "hl": "en-US",
                "gl": "US",
                "ceid": "US:en"
            }
            
            print(f"\nTrying {query['desc']}: '{query['q']}'")
            
            # Use requests to get the RSS feed
            response = requests.get(
                base_url,
                params=params,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                },
                timeout=10
            )
            
            # Check response status
            if response.status_code != 200:
                print(f"Query failed with status code: {response.status_code}")
                continue
                
            # Parse the feed
            feed = feedparser.parse(response.text)
            
            if not feed.entries:
                print("No entries found in feed")
                continue
                
            print(f"Found {len(feed.entries)} articles")
            
            # Process articles
            for entry in feed.entries:
                try:
                    # Extract content
                    title = clean_text(entry.get("title", ""))
                    content = clean_text(entry.get("description", ""))
                    
                    # Try alternate content fields if primary is empty
                    if not content:
                        content = clean_text(entry.get("summary", ""))
                    if not content:
                        content = clean_text(entry.get("content", [{"value": ""}])[0].get("value", ""))
                    
                    # Skip if no title or content
                    if not title or not content:
                        continue
                    
                    # Generate summary
                    summary = extract_summary(content)
                    
                    # Format publish date
                    pub_date = None
                    try:
                        if entry.get("published"):
                            pub_date = datetime.strptime(
                                entry.get("published"),
                                "%a, %d %b %Y %H:%M:%S %Z"
                            ).isoformat()
                    except Exception as e:
                        print(f"Date parsing error: {e}")
                    
                    # Get source
                    source = "Unknown Source"
                    if entry.get("source"):
                        source = entry.source.get("title", "Unknown Source")
                    
                    # Create article object
                    article = {
                        "title": title,
                        "link": entry.get("link", ""),
                        "content": content,
                        "summary": summary,
                        "publish_date": pub_date,
                        "source": source
                    }
                    
                    # Check for duplicates
                    if not any(a["link"] == article["link"] for a in all_articles):
                        all_articles.append(article)
                        print(f"Added article {len(all_articles)}: {title[:50]}...")
                    
                    # Break if we have enough articles
                    if len(all_articles) >= num_articles:
                        break
                        
                except Exception as e:
                    print(f"Error processing article: {str(e)}")
                    continue
            
            # Break if we have enough articles
            if len(all_articles) >= num_articles:
                break
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            continue
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            continue
    
    # Check if we found any articles
    if not all_articles:
        print("No articles found with any query")
        return {"error": "No news articles found. Please try a different company name."}
    
    # Limit to requested number of articles
    all_articles = all_articles[:num_articles]
    
    try:
        # Generate article comparisons and topic analysis
        analysis = compare_articles(all_articles)
        
        result = {
            "articles": all_articles,
            "analysis": analysis if analysis else {}
        }
        
        print(f"\nSuccessfully fetched and analyzed {len(all_articles)} articles")
        return result
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        # Return articles with empty analysis if analysis fails
        return {
            "articles": all_articles,
            "analysis": {}
        }

# 🔹 Run the script
if __name__ == "__main__":
    company = "Tesla"
    print(fetch_news(company))
