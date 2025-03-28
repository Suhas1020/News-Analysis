# Company News Analyzer

A comprehensive news analysis tool that fetches, analyzes, and presents news articles about companies. The tool performs sentiment analysis, topic extraction, and provides insights in both text and audio formats.

## Features

1. **News Extraction**
   - Fetches 10 unique news articles from multiple sources
   - Sources include Google News, Reuters, and Business Wire
   - Extracts title, summary, and metadata
   - Uses BeautifulSoup for non-JavaScript web scraping

2. **Sentiment Analysis**
   - Analyzes article sentiment (positive, negative, neutral)
   - Provides sentiment scores and confidence levels
   - Combines title and content analysis for better accuracy

3. **Comparative Analysis**
   - Cross-article sentiment comparison
   - Source distribution analysis
   - Topic distribution
   - Temporal analysis
   - Automated insights generation

4. **Text-to-Speech**
   - Converts analysis summaries to Hindi
   - Uses gTTS for high-quality audio generation
   - Provides downloadable audio files

5. **User Interface**
   - Clean, modern Streamlit interface
   - Interactive visualizations using Plotly
   - Responsive design
   - Easy-to-use controls

6. **API Backend**
   - FastAPI-based REST API
   - Structured JSON responses
   - Error handling and validation
   - Async support for better performance

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd news-analysis-project
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Backend Server**
   ```bash
   uvicorn api:app --reload
   ```

5. **Start the Streamlit Interface**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open your browser and go to `http://localhost:8501`
2. Enter a company name in the sidebar
3. Click "Analyze News"
4. View the analysis results:
   - Overall sentiment distribution
   - Comparative analysis insights
   - Individual article details
   - Hindi audio summary

## API Endpoints

1. **GET /fetch-news/{company}**
   - Fetches and analyzes news for the specified company
   - Returns structured data with articles, sentiment, and analysis

2. **GET /tts/{company}**
   - Generates Hindi TTS summary for company news
   - Returns audio file path

3. **POST /extract-topics/**
   - Extracts topics from provided text
   - Accepts JSON payload with "text" field

## Dependencies

- FastAPI & Uvicorn for backend
- Streamlit for frontend
- BeautifulSoup4 for web scraping
- Newspaper3k for article parsing
- TextBlob for sentiment analysis
- YAKE for keyword extraction
- gTTS for Hindi text-to-speech
- Plotly for visualizations
- Pandas for data manipulation

## Deployment

The application is deployed on Hugging Face Spaces. Visit https://huggingface.co/spaces/Suhas125/News-analysis to try it out.

Model Details
Summarization Model:
Model Used: The application utilizes the transformers library to load a pre-trained model for summarization. Common models for summarization include BART, T5, or Pegasus.
Purpose: The summarization model condenses news articles into shorter, more digestible summaries while retaining the main points and context.
Integration: The model is accessed via the pipeline function from the transformers library, which simplifies the process of loading and using the model for inference.
Sentiment Analysis Model:
Model Used: The application uses the cardiffnlp/twitter-roberta-base-sentiment model from the Hugging Face Model Hub, which is specifically fine-tuned for sentiment analysis on social media text.
Purpose: This model classifies the sentiment of news articles into categories such as positive, negative, or neutral.
Integration: The model is integrated using the pipeline function from the transformers library, allowing for easy sentiment classification of article content.
Text-to-Speech (TTS) Model:
Model Used: The application uses the gTTS (Google Text-to-Speech) library for converting text summaries into spoken audio.
Purpose: This feature allows users to listen to the summaries of news articles, enhancing accessibility and user experience.
Integration: The gTTS library is used to generate audio files from text, which can then be played back to users.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
