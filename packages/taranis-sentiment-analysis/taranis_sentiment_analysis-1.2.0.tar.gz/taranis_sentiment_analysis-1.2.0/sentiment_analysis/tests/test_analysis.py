import pytest
import json
from sentiment_analysis.sentiment_analysis_multimodel import analyze_sentiment

@pytest.fixture
def test_data():
    with open("sentiment_analysis/tests/clustered_news_item_list.json") as f:
        data = json.load(f)
    return [item["content"] for cluster in data for item in cluster["news_items"] if "content" in item]

@pytest.mark.parametrize("text", [
    "",  
    "Good day!",  
    "This is a very long text that requires processing by the sentiment analyzer." * 10 
])
def test_analyze_sentiment_basic(text):
    result = analyze_sentiment(text)
    if text == "":
        assert "error" in result, "Expected 'error' in result for empty text"
    else:
        assert "label" in result, "Expected 'label' in result"
        assert "score" in result, "Expected 'score' in result"
        assert isinstance(result["score"], float), "Expected score to be a float"

def test_analyze_sentiment_with_test_data(test_data):
    for content in test_data:
        result = analyze_sentiment(content)
        assert "label" in result, f"Expected 'label' in result for content: {content[:30]}"
        assert "score" in result, f"Expected 'score' in result for content: {content[:30]}"
