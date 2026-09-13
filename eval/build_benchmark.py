# Benchmark Dataset Generator
#build benchmark csv contianeing intents
#escalates flags

import sys
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from src.config import BENCHMARK_SET_PATH

BENCHMARK_SAMPLES = [
    # Delivery Delay
    {"customer_text": "My package was supposed to arrive yesterday but tracking has not updated. Where is order #12345?", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Where is my shipment? It has been stuck in transit for 5 days.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "My tracking number says delivered but I haven't received my box.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    
    # Payment Issue (High Risk -> Escalate)
    {"customer_text": "I was charged twice for my subscription this month! $14.99 deducted two times.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "My payment got stucked i din't recieved refund yet", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Why did you charge my credit card again without permission?", "ground_truth_intent": "payment_issue", "should_escalate": True},
    
    # Product Defect
    {"customer_text": "My iPhone screen keeps freezing after the latest iOS update.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "The charger I bought caught fire and burned my desk!", "ground_truth_intent": "product_defect", "should_escalate": True}, # Safety trigger
    {"customer_text": "The app keeps crashing every time I open settings.", "ground_truth_intent": "product_defect", "should_escalate": False},
    
    # General Inquiry
    {"customer_text": "What are your customer support store hours on weekends?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "How do I update my profile shipping address?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    
    # Safety / Legal Triggers -> Escalate
    {"customer_text": "Someone made an unauthorized order on my account, I think I was hacked.", "ground_truth_intent": "other", "should_escalate": True},
    {"customer_text": "I am filing a lawsuit with my attorney if this isn't resolved today.", "ground_truth_intent": "other", "should_escalate": True},
    {"customer_text": "Hello, good morning!", "ground_truth_intent": "other", "should_escalate": False}
]

def benchmark_build_set():
    """Generates benchark_set.csv for benchmark evaluation."""

    BENCHMARK_SET_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(BENCHMARK_SAMPLES)
    df.to_csv(BENCHMARK_SET_PATH, index=False)
    print(f"✅ Generated Benchmark set with {len(df)} samples at:\n   {BENCHMARK_SET_PATH}")
    
if __name__ == "__main__":
    benchmark_build_set()