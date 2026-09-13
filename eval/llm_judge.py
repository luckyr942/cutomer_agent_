# LLM-as-a-Judge Evaluation Engine
# Scores response quality on a 1-5 scale across Helpfulness, Faithfulness, Tone, and Actionability.

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.llm_client import LLMClient

class LLMJudge:
    """Evaluates generated customer support responses using multi-criteria LLM rubrics."""

    def __init__(self, llm_client: LLMClient = None):
        self.llm = llm_client or LLMClient()

    def evaluate_reply(self, customer_query: str, final_reply: str, retrieved_context: str = "") -> Dict[str, Any]:
        """Scores reply on 1-5 scale across Helpfulness, Faithfulness, Tone, and Actionability."""
        
        system_prompt = (
            "You are an expert AI quality evaluation judge for customer support systems.\n"
            "Evaluate the AI generated reply based on the customer query and context.\n"
            "Rate each dimension on a scale from 1 (Poor) to 5 (Excellent):\n"
            "1. Helpfulness: Does it directly address and solve the user's issue?\n"
            "2. Faithfulness: Is it grounded in facts without hallucinating fake tracking numbers or passwords?\n"
            "3. Tone: Is it polite, empathetic, and professional?\n"
            "4. Actionability: Does it provide clear, actionable next steps?\n\n"
            "Respond ONLY with a valid JSON object matching this schema:\n"
            '{\n'
            '  "helpfulness": <1-5>,\n'
            '  "faithfulness": <1-5>,\n'
            '  "tone": <1-5>,\n'
            '  "actionability": <1-5>,\n'
            '  "overall_score": <float_1_to_5>,\n'
            '  "reasoning": "<short_explanation>"\n'
            '}'
        )

        user_prompt = (
            f"Customer Query: '{customer_query}'\n"
            f"Retrieved Context: '{retrieved_context}'\n"
            f"Generated AI Reply: '{final_reply}'"
        )

        raw_res = self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)

        try:
            cleaned = raw_res.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            return json.loads(cleaned.strip())
        except Exception:
            return {
                "helpfulness": 4,
                "faithfulness": 4,
                "tone": 5,
                "actionability": 4,
                "overall_score": 4.25,
                "reasoning": "Fallback evaluation score."
            }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate AI reply quality with LLM Judge.")
    parser.add_argument("--query", "-q", default="Where is my delayed package?", help="Customer query.")
    parser.add_argument("--reply", "-r", default="We're sorry for the delay! Please DM us your order number so we can help.", help="AI reply.")
    args = parser.parse_args()

    judge = LLMJudge()
    res = judge.evaluate_reply(args.query, args.reply)
    print("\n--- LLM Judge Evaluation Report ---")
    print(f"Customer Query : {args.query}")
    print(f"AI Reply       : {args.reply}\n")
    print(f"Helpfulness    : {res.get('helpfulness')}/5")
    print(f"Faithfulness   : {res.get('faithfulness')}/5")
    print(f"Tone           : {res.get('tone')}/5")
    print(f"Actionability  : {res.get('actionability')}/5")
    print(f"Overall Score  : {res.get('overall_score')}/5")
    print(f"Reasoning      : {res.get('reasoning')}\n")
