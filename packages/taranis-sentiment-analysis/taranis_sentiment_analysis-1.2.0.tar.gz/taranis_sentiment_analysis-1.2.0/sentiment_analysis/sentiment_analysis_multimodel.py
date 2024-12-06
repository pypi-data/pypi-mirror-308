from transformers import pipeline, LongformerForSequenceClassification, LongformerTokenizer


roberta_sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")
longformer_tokenizer = LongformerTokenizer.from_pretrained("allenai/longformer-base-4096")
longformer_model = LongformerForSequenceClassification.from_pretrained("allenai/longformer-base-4096")

label_mapping = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text. Select model based on text length.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: A dictionary with the raw output of the model.
    """
    if not text or len(text.strip()) == 0:
        return {"error": "Empty text provided"}

    try:
        # Tokenize the text with RoBERTa tokenizer
        roberta_tokens = roberta_sentiment_pipeline.tokenizer(text)
        
        if len(roberta_tokens["input_ids"]) > 512:
            inputs = longformer_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            outputs = longformer_model(**inputs)
            logits = outputs.logits
            predicted_class_id = logits.argmax().item()
            
            # Map class ID to sentiment label with better readability
            sentiment = label_mapping[f"LABEL_{predicted_class_id}"]

            return {"label": sentiment, "score": logits.softmax(dim=1).max().item()}
        else:
            roberta_output = roberta_sentiment_pipeline(text)[0]
            
            return {
                "label": roberta_output["label"],
                "score": roberta_output["score"]
             }
    except Exception as e:
        return {"error": str(e)}
