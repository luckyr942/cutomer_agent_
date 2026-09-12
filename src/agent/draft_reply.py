#THIS is the response generator 
#  working -> Customer Message + Intent
#            │
#            ▼
# [Retrieved Past Cases] (from retrieval.py)
#            │
#            ▼
# [ResponseDrafter] (draft_reply.py)
#            │
#            ▼
# Empathetic, Grounded 2-3 Sentence Reply

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from src.llm_client import LLMClient

class ResponseDrafter:
    """Generates grounded customer support replies using historical retrieved context."""

    def __init__(self, llm_client:LLMClient = None):
        self.llm = llm_client or LLMClient()

    def draft(self, customer_text: str, intent: str, retrieved_context: List[Dict[str, Any]] = None) -> str:
        """Drafts a grounded response for a customer query."""
        context_str = ""
        
        if retrieved_context:
            context_str = "\n".join([
                f"Past Resolved Query: {item.get('customer_text', '')}\nPast Support Reply: {' '.join(item.get('brand_replies', []))}"
                for item in retrieved_context
            ])
        else:
            context_str = "No past historical context available."
        system_prompt = (
            "You are an empathetic, professional customer support agent for Twitter/X.\n"
            "Draft a concise, helpful response (max 2-3 sentences).\n"
            "Ground your answer strictly using the provided past resolved examples when relevant.\n"
            "Do NOT invent fake tracking numbers or ask for passwords."
        )
        user_prompt = (
            f"Customer Intent: {intent}\n"
            f"Customer Message: '{customer_text}'\n\n"
            f"Historical Context:\n{context_str}\n\n"
            "Draft Response:"
        )
        return self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Draft grounded customer response.")
    parser.add_argument("--text", "-t", type=str, default="Where is my package #12345?", help="Customer message.")
    parser.add_argument("--intent", "-i", type=str, default="delivery_delay", help="Intent label.")
    args = parser.parse_args()
    drafter = ResponseDrafter()
    reply = drafter.draft(args.text, args.intent)
    print("\n--- Response Drafter Output ---")
    print(f"Customer Text : '{args.text}'")
    print(f"Intent        : {args.intent}")
    print(f"Drafted Reply :\n{reply}\n")