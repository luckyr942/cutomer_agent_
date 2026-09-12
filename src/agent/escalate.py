# this is the safety & human escalation policy 
# ---> it act as a safety brakes between the user's input and the automated reply generator
# checks company policy wether can automate or need human to handle it 

import sys
import re
import argparse
from pathlib import Path
from typing import Dict, Any

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.intent import ESCALATION_INTENTS

SAFETY_TRIGGERS = {
    # 1. Legal, Law Enforcement & Regulatory Agencies
    "legal": [
        "lawsuit", "attorney", "lawyer", "legal action", "sue", 
        "police", "fir", "court", "ftc", "bbb", "consumer court", 
        "consumer forum", "fraud department"
    ],
    # 2. Account Security & Identity Compromise
    "account_security": [
        "hacked", "unauthorized", "stolen card", "compromised", 
        "identity theft", "didn't order this", "did not authorize", 
        "account taken over", "otp shared"
    ],
    # 3. Product Safety & Hazardous Defects
    "product_hazard": [
        "caught fire", "exploded", "burned", "electric shock", 
        "smoke", "hazardous", "hospital", "injury", "poison", 
        "counterfeit", "fake medicine", "expired food"
    ],
    # 4. Delivery & Driver Serious Incidents
    "logistics_incident": [
        "driver stole", "trespassing", "damaged property", 
        "assault", "harassment", "stolen package", "porch pirate"
    ],
    # 5. Financial Dispute Threats
    "financial_threat": [
        "chargeback", "dispute with bank", "bank fraud", "scam"
    ]
}


class EscalationEngine:
    """Evaluates whether a customer query requires escalation to a human agent."""

    def __init__(self, high_risk_intent: set = ESCALATION_INTENTS, confidence_threshold: float = 0.60):
        self.high_risk_intent = high_risk_intent
        self.confidence_threshold = confidence_threshold

        self.safety_keywords = [
            key for group in SAFETY_TRIGGERS.values() for key in group
        ]

    def evaluate(self, intent: str, confidence: float, customer_text: str) -> Dict[str, Any]:
        """Determines if escalation is required and provides policy reason."""
        
        text_lower = customer_text.lower()

        # Rule 1: High-risk intent category
        if intent in self.high_risk_intent:
            return {
                "escalate": True,
                "reason": f"High-risk intent detected: '{intent}' (requires human verification)."
            }
        
        # Rule 2: Low Classification Confidence 
        if confidence < self.confidence_threshold:
            return {
                "escalate": True,
                "reason": f"Low classification confidence ({confidence:.2f} < {self.confidence_threshold:.2f})."
            }
        
        # Rule 3: Keyword safety triggers (uses regex word boundary so 'fir' doesn't match inside 'fire')
        for key in self.safety_keywords:
            pattern = r'\b' + re.escape(key) + r'\b'
            if re.search(pattern, text_lower):
                return {
                    "escalate": True,
                    "reason": f"Safety trigger detected: '{key}'."
                }
        
        return {
            "escalate": False,
            "reason": "Standard request eligible for automated AI response."
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate ticket escalation policy.")
    parser.add_argument("--intent", "-i", type=str, default="other", help="Intent label.")
    parser.add_argument("--conf", "-c", type=float, default=0.95, help="Classification confidence.")
    parser.add_argument("--text", "-t", type=str, help="Customer message text.")
    args = parser.parse_args()

    engine = EscalationEngine()

    if args.text:
        res = engine.evaluate(args.intent, args.conf, args.text)
        print("\n--- Escalation Evaluation Result ---")
        print(f"Message  : \"{args.text}\"")
        print(f"Intent   : {args.intent} (Conf: {args.conf})")
        print(f"Escalate : {res['escalate']}")
        print(f"Reason   : {res['reason']}\n")
    else:
        print("Testing Escalation Engine...\n")
        print(engine.evaluate("payment_issue", 0.95, "Fix this double charge!"))
        print(engine.evaluate("delivery_delay", 0.40, "Where is my box?"))
        print(engine.evaluate("product_defect", 0.95, "The charger caught fire and burned my desk!"))
        print(engine.evaluate("other", 0.90, "Someone made an unauthorized order on my account"))
        print(engine.evaluate("delivery_delay", 0.95, "Where is my package? The tracking has not updated."))
