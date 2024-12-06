from transformers import pipeline

# Load pre trained XLM-RoBERTa model for sentiment-analysis
roberta_sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")

# Label mapping for the sentiment output
label_mapping = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVE"
}

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text using the XLM-RoBERTa model.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: A dictionary with the raw output of the model.
    """
    roberta_output = roberta_sentiment_pipeline(text)[0]
    return {
                "label": roberta_output["label"],
                "score": roberta_output["score"]
             }    
    