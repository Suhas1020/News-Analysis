from transformers import pipeline

# Load the improved sentiment model
sentiment_model = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")


def analyze_sentiment(text):
    """
    Perform sentiment analysis using a pre-trained transformer model.
    """
    if not text.strip():  # Avoid empty text crashing the model
        return "Neutral"

    result = sentiment_model(text, truncation=True, max_length=512)[0]  # Ensure full processing
    label_map = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}

    return label_map.get(result["label"], "Neutral")  # Default to Neutral if label is missing

