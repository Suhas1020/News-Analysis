from textblob import TextBlob
from collections import Counter

def analyze_sentiment(text):
    """
    Analyze sentiment of a given text using TextBlob.
    Returns sentiment category and score.
    """
    if not text:
        return {"category": "Neutral", "score": 0.0}
        
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity
    
    # Categorize sentiment
    if score > 0.1:
        category = "Positive"
    elif score < -0.1:
        category = "Negative"
    else:
        category = "Neutral"
        
    return {
        "category": category,
        "score": round(score, 2)
    }

def compare_sentiment(articles):
    """
    Compare sentiment across multiple articles.
    Returns sentiment distribution and overall sentiment.
    """
    if not articles:
        return {
            "sentiment_distribution": {
                "Positive": 0,
                "Negative": 0,
                "Neutral": 0
            },
            "overall_sentiment": {
                "category": "Neutral",
                "score": 0.0
            }
        }
    
    # Analyze sentiment for each article
    sentiments = []
    total_score = 0.0
    
    for article in articles:
        # Combine title and content for better sentiment analysis
        text = f"{article.get('title', '')} {article.get('content', '')}"
        sentiment = analyze_sentiment(text)
        sentiments.append(sentiment["category"])
        total_score += sentiment["score"]
        
        # Add sentiment to article
        article["sentiment"] = sentiment
    
    # Calculate sentiment distribution
    sentiment_counts = Counter(sentiments)
    sentiment_distribution = {
        "Positive": sentiment_counts.get("Positive", 0),
        "Negative": sentiment_counts.get("Negative", 0),
        "Neutral": sentiment_counts.get("Neutral", 0)
    }
    
    # Calculate overall sentiment
    avg_score = total_score / len(articles)
    overall_category = "Positive" if avg_score > 0.1 else "Negative" if avg_score < -0.1 else "Neutral"
    
    return {
        "sentiment_distribution": sentiment_distribution,
        "overall_sentiment": {
            "category": overall_category,
            "score": round(avg_score, 2)
        }
    }
