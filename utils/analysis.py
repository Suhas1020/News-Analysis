from utils import analyze_sentiment


def compare_sentiment(articles):
    """
    Compute sentiment distribution from multiple articles.
    """
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for article in articles:
        sentiment = analyze_sentiment(article["title"])  # Use title as a sample text
        sentiment_counts[sentiment] += 1
        article["sentiment"] = sentiment

    return {"articles": articles, "sentiment_distribution": sentiment_counts}
