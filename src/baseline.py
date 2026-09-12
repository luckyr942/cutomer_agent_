import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.intent import classify_intent_by_keywords

class MajorityClassBaseline:
    """Majority class baseline that always predicts the majority intent class."""
    def __init__(self, majority_intent: str = 'delivery_delay'):
        self.majority_intent = majority_intent

    def predict(self, text:str) -> str:
        return self.majority_intent

class KeywordBasedBaseline:
    """Rule-based keyword matching baseline classifier."""
    def predict(self, text: str) -> str:
        return classify_intent_by_keywords(text)

if __name__ == "__main__":
    majority_model = MajorityClassBaseline()
    keyword_model = KeywordBasedBaseline()

    sample_texts = [
        "Where is my package?",
        "I was charged twice!",
        "My app crashed on Startup"
    ]

    print("BaseLine Predictions:")
    for text in sample_texts:
        print(f"\nText: '{text}'")
        print(f"Majority: {majority_model.predict(text)}")
        print(f"Keyword: {keyword_model.predict(text)}")
        