from fastapi import FastAPI, HTTPException
from utils.scraper import fetch_news, extract_topics
from utils.extract_topics import extract_topics
from utils.comparative_analysis import generate_comparative_analysis
from utils.sentiment_analysis import compare_sentiment
from utils.tts_generator import generate_tts
from typing import Dict, List, Union, Optional

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Analysis API"}

@app.get("/fetch-news/{company_name}")
def get_news(company_name: str) -> Dict[str, Union[List[Dict], Dict]]:
    """
    Fetch and analyze news articles for a given company.
    Returns:
        - Articles with their content and metadata
        - Topic analysis for each article
        - Sentiment analysis across all articles
        - Comparative analysis between articles
    """
    result = fetch_news(company_name)
    
    # Check if there was an error
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    articles = result["articles"]
    
    # Process articles and add topics
    for article in result["articles"]:
        article["topics"] = extract_topics(article.get("content", ""))
    
    # Perform sentiment analysis
    sentiment_analysis = compare_sentiment(articles)
    
    # Generate comparative analysis
    comparative = generate_comparative_analysis(articles)
    
    # Format comparative analysis for frontend compatibility
    comparative_analysis = {
        "coverage_summary": comparative["thematic_summary"],
        "insights": [
            f"Comparison {i+1}: {comp['comparison']} - {comp['impact']}"
            for i, comp in enumerate(comparative["article_comparisons"])
        ],
        "key_differences": comparative["key_differences"],
        "article_comparisons": comparative["article_comparisons"],
        "source_distribution": {
            "sources": [{"name": source, "count": count} for source, count in comparative["source_distribution"].items()],
            "total_sources": len(comparative["source_distribution"])
        }
    }
    
    # Structure the complete response
    complete_response = {
        "articles": articles,
        "analysis": result["analysis"],
        "sentiment_analysis": sentiment_analysis,
        "comparative_analysis": comparative_analysis
    }
    
    return complete_response

@app.get("/tts/{company}")
def get_tts(company: str):
    """
    Generate Hindi TTS summary for company news sentiment.
    """
    company = company.strip()
    result = fetch_news(company)

    # Check if there was an error
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    # Get articles from the result
    articles = result["articles"]
    
    if not articles:
        raise HTTPException(status_code=404, detail="No valid news articles found.")

    # Perform sentiment analysis
    sentiment_data = compare_sentiment(articles)
    
    # Create a more detailed summary
    summary_text = (
        f"कंपनी {company} के लिए समाचार विश्लेषण। "
        f"कुल {len(articles)} समाचार लेख मिले, जिनमें से "
        f"{sentiment_data['sentiment_distribution']['Positive']} सकारात्मक, "
        f"{sentiment_data['sentiment_distribution']['Negative']} नकारात्मक, और "
        f"{sentiment_data['sentiment_distribution']['Neutral']} तटस्थ हैं। "
        f"समग्र भावना {sentiment_data['overall_sentiment']['category']} है।"
    )

    file_path = generate_tts(summary_text)

    if not file_path:
        raise HTTPException(status_code=500, detail="Failed to generate TTS file.")

    return {"message": "TTS generated", "file": file_path}


@app.post("/extract-topics/")
async def get_topics(payload: dict):
    text = payload.get("text", "").strip()
    print("🟢 Received Text for Topic Extraction:", repr(text))

    if not text:
        return {"topics": ["No valid content to extract topics"]}

    topics = extract_topics(text)

    print("🟢 Extracted Topics Before Returning:", topics)  # Debugging

    return {"topics": topics}


