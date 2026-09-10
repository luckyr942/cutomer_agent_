# for keyword matching rules &  taxonomy + escalation policy defaults
####. agent's single rulebook ####

import sys
from pathlib import Path 

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

#Intent taxonomy defination / mattching keywords
INTENT_TAXANOMY ={
    "delivery_delay": "Inquiries regarding package tracking, shipment delays, or missing orders.",
    "payment_issue": "Issues with double charges, billing errors, payment failures, or refund requests.",
    "product_defect": "App crashes, software freezing, broken hardware, or technical glitches.",
    "general_inquiry": "Questions about store hours, features, policies, or general information.",
    "other": "General feedback, greetings, or uncategorized messages."
}

#Kewords rules for clarification
KEYWORD_RULES = {
    "delivery_delay": ["delivery", "transit", "where is my order", "package", "shipment", "tracking", "arrive"],
    "payment_issue": ["charge", "charged", "billing", "refund", "subscription", "deducted", "$", "money"],
    "product_defect": ["freeze", "freezing", "crash", "broken", "update", "issue", "error", "not working"],
    "general_inquiry": ["how to", "what is", "hours", "info", "question"]
}

# High-risk intents triggering mandatory human escalation
ESCALATION_INTENTS = {"payment_issue", "legal_threat", "safety_concern"}

def classify_intent_by_keywords(text: str) -> str:
    """Simple keyword matching baseline classifier."""
    text_lower = text.lower()
    for intent, keywords in KEYWORD_RULES.items():
        if any (key in text_lower for key in keywords):
            return intent
        return "other"

if __name__ == "__main__":
    test_cases = [
        "I was charged twice for my order!",
        "My app keeps freezing after the update",
        "What are your store hours?",
        "My package has not arrived yet",
        "Hello!"
    ]
    
    print("Testing Intent Classifier...")
    for text in test_cases:
        intent = classify_intent_by_keywords(text)
        escalate = intent in ESCALATION_INTENTS
        print(f"\nText: {text}")
        print(f"   -> Intent: {intent} | Escalate: {escalate}")