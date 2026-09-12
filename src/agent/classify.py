# # # this classify customer messages into structured json using LLMClient
# # #  --> delivery delay, payment issue, profduct defect, general query, & other

# # import sys
# # import json
# # from pathlib import Path
# # from typing import Dict, Any


# # ROOT_DIR = Path(__file__).resolve().parent.parent.parent
# # if str(ROOT_DIR) not in sys.path:
# #     sys.path.insert(0,str(ROOT_DIR))


# # from src.llm_client import LLMClient
# # from src.intent import INTENT_TAXONOMY, classify_intent_by_keywords

# # class LLMIntentClassifier:
# #     """Classify customer messages using strucutred JSON output."""
    
# #     def __init__(self, llmClient: LLMClient = None):
# #         self.llm = llmClient or LLMClient()

# #     def classify(self, text:str) -> Dict[str, Any]:
# #         """Returns a dictionary containing intent, confidence and reasoning."""
# #         taxonomy_desc = "\n".join([f"- {intent}: {desc}" for intent, desc in INTENT_TAXONOMY.items()])

# #         # Guardrails -> instruct the LLM on its role
# #         system_prompt = (
# #             "You are a customer support intent classification engine.\n"
# #             "Classify the customer message into exactly ONE of the following intents:\n"
# #             f"{taxonomy_desc}\n\n"
# #             "Respond ONLY with a valid JSON object matching this schema:\n"
# #             '{"intent": "<intent_name>", "confidence": <float_0_to_1>, "reasoning": "<short_explanation>"}'
# #         )

# #         user_prompt = f"Customer Message: '{text}'"

# #         raw_response = self.llm.generate(prompt = user_prompt, system_prompt = system_prompt)


# #         try:
# #             #Parse JSON from LLM response
# #             parsed = json.loads(raw_response)
# #             if "intent" in parsed and parsed["intent"] in INTENT_TAXONOMY:
# #                 return parsed
# #         except Exception:
# #             pass

# #         # Fallback to rule-based keyword classifier if JSON parsing fails
# #         fallback_intent = classify_intent_by_keywords(text)
# #         return {
# #             "intent": fallback_intent,
# #             "confidence": 0.70,
# #             "reasoning": "Fallback to keyword classifier."
# #         }


# # if __name__ == "__main__":
# #     classifier = LLMIntentClassifier()
# #     sample = "I was charged twice for my subscription this month!"
# #     res = classifier.classify(sample)
# #     print(f"Text: '{sample}'")
# #     print(f"Classification Result: {res}")



import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.llm_client import LLMClient
from src.intent import INTENT_TAXONOMY, classify_intent_by_keywords


class LLMIntentClassifier:
    """Classify customer messages using structured JSON output."""

    def __init__(self, llm_client: LLMClient | None = None):
        self.llm = llm_client or LLMClient()

    def classify(self, text: str) -> Dict[str, Any]:
        """Returns a dictionary containing intent, confidence and reasoning."""
        taxonomy_desc = "\n".join(
            [f"- {intent}: {desc}" for intent, desc in INTENT_TAXONOMY.items()]
        )

        system_prompt = (
            "You are a customer support intent classification engine.\n"
            "Customer messages contain frequent typos, slang, broken grammar, and phonetic spelling.\n"
            "Infer the user's core intent despite noise and classify into exactly ONE of:\n"
            f"{taxonomy_desc}\n\n"
            "Respond ONLY with a valid JSON object matching this schema:\n"
            '{"intent": "<intent_name>", "confidence": <float_0_to_1>, "reasoning": "<short_explanation>"}'
        )

        user_prompt = f"Customer Message: '{text}'"
        raw_response = self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        print(f"\n[DEBUG RAW RESPONSE]: {repr(raw_response)}\n")
        # 1. Defensive check: Ensure raw_response is a valid string
        if raw_response:
            # 2. Simple clean: strip whitespace and markdown ```json / ``` wrappers
            cleaned = raw_response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            # 3. Parse and validate against taxonomy
            try:
                parsed = json.loads(cleaned)
                if "intent" in parsed and parsed["intent"] in INTENT_TAXONOMY:
                    parsed["confidence"] = float(parsed.get("confidence", 0.90))
                    return parsed
            except Exception:
                pass

        # 4. Fallback to keyword rules if API drops, returns None, or fails JSON
        fallback_intent = classify_intent_by_keywords(text)
        return {
            "intent": fallback_intent,
            "confidence": 0.70,
            "reasoning": "Fallback to keyword classifier.",
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify customer message intent.")
    parser.add_argument("--text", "-t", type=str, help="Customer message text to classify.")
    args = parser.parse_args()

    classifier = LLMIntentClassifier()

    if args.text:
        res = classifier.classify(args.text)
        print("\n--- Result ---")
        print(f"Message:    {args.text}")
        print(f"Intent:     {res.get('intent')}")
        print(f"Confidence: {res.get('confidence')}")
        print(f"Reasoning:  {res.get('reasoning')}\n")
    else:
        print("Interactive Mode (Press Ctrl+C or type 'exit' to quit):")
        while True:
            try:
                user_msg = input("\nEnter customer message: ").strip()
                if not user_msg or user_msg.lower() == "exit":
                    break
                res = classifier.classify(user_msg)
                print(f"-> Intent:     {res.get('intent')}")
                print(f"-> Confidence: {res.get('confidence')}")
                print(f"-> Reasoning:  {res.get('reasoning')}")
            except KeyboardInterrupt:
                print("\nExiting.")
                break