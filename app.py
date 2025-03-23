import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import uvicorn
from api import app  # Import your FastAPI app from api.py
import spacy
import os

# Configure the page
st.set_page_config(
    page_title="Company News Analyzer",
    page_icon="📰",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2c3e50;
        font-size: 3rem !important;
    }
    .article-box {
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
    .sentiment-positive {
        color: #28a745;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #dc3545;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #6c757d;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("📰 Company News Analyzer")
st.markdown("""
This tool analyzes news articles about companies, providing sentiment analysis, 
topic extraction, and comparative analysis. It also generates Hindi audio summaries.
""")

# Input section
st.sidebar.header("Settings")
company = st.sidebar.text_input("Enter Company Name", "")
analyze_button = st.sidebar.button("Analyze News")

# API endpoint
BASE_URL = "http://127.0.0.1:8000"

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

if analyze_button and company:
    with st.spinner('Fetching and analyzing news articles...'):
        try:
            # Fetch news analysis
            response = requests.get(f"{BASE_URL}/fetch-news/{company.strip()}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Display overall sentiment analysis
                st.header("📊 Overall Sentiment Analysis")
                col1, col2, col3 = st.columns(3)
                
                sentiment_dist = data["sentiment_analysis"]["sentiment_distribution"]
                with col1:
                    st.metric("Positive Articles", sentiment_dist["Positive"])
                with col2:
                    st.metric("Negative Articles", sentiment_dist["Negative"])
                with col3:
                    st.metric("Neutral Articles", sentiment_dist["Neutral"])
                
                # Create sentiment distribution pie chart
                df_sentiment = pd.DataFrame({
                    'Sentiment': list(sentiment_dist.keys()),
                    'Count': list(sentiment_dist.values())
                })
                fig = px.pie(df_sentiment, values='Count', names='Sentiment',
                           title='Sentiment Distribution',
                           color_discrete_map={'Positive': '#28a745',
                                             'Negative': '#dc3545',
                                             'Neutral': '#6c757d'})
                st.plotly_chart(fig)
                
                # Display comparative analysis insights
                st.header("🔍 Comparative Analysis")
                for insight in data["comparative_analysis"]["insights"]:
                    st.info(insight)
                
                # Display source distribution
                st.subheader("📰 News Sources")
                source_dist = data["comparative_analysis"]["source_distribution"]
                df_sources = pd.DataFrame({
                    'Source': list(source_dist.keys()),
                    'Articles': list(source_dist.values())
                })
                st.bar_chart(df_sources.set_index('Source'))
                
                # Display articles
                st.header("📑 News Articles")
                for article in data["articles"]:
                    with st.expander(f"{article['title']}"):
                        st.markdown(f"**Summary:** {article['summary']}")
                        st.markdown(f"**Source:** {article.get('source', 'Unknown')}")
                        st.markdown(f"**Published:** {article.get('publish_date', 'Date not available')}")
                        
                        sentiment = article["sentiment"]
                        sentiment_color = ("sentiment-positive" if sentiment["category"] == "Positive"
                                         else "sentiment-negative" if sentiment["category"] == "Negative"
                                         else "sentiment-neutral")
                        st.markdown(f"**Sentiment:** <span class='{sentiment_color}'>{sentiment['category']} ({sentiment['score']})</span>",
                                  unsafe_allow_html=True)
                        
                        st.markdown("**Topics:**")
                        for topic in article["topics"]:
                            st.markdown(f"- {topic}")
                        
                        st.markdown(f"[Read Full Article]({article['link']})")
                
                # Generate and display Hindi TTS
                st.header("🔊 Hindi Summary")
                tts_response = requests.get(f"{BASE_URL}/tts/{company.strip()}")
                if tts_response.status_code == 200:
                    tts_data = tts_response.json()
                    audio_file = tts_data.get("file")
                    if audio_file:
                        st.audio(audio_file, format="audio/mp3")
                    else:
                        st.warning("TTS file not available.")
                else:
                    st.error("Failed to generate Hindi summary.")
                    
            else:
                st.error("Error fetching news. Please try again with a different company name.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.info("Enter a company name and click 'Analyze News' to start the analysis.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
