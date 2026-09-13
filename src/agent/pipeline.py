# central system -> orchestrator 

import sys
import argparse
from pathlib import Path
from typing import Dict, Any

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.llm_client import LLMClient
from src.retrieval import TFIDFRetriever
from src.agent.classify import LLMIntentClassifier
from src.agent.escalate import EscalationEngine
from src.agent.draft_reply import ResponseDrafter


class AgentPipeline:
    """Support agent unified orchestrator Classification , Retrieval, Escalation, reply drafting"""

    def __init__(self):
        self.llm = LLMClient()
        self.retriever = TFIDFRetriever()
        self.classifier = LLMIntentClassifier(self.llm)
        self.escalation_engine = EscalationEngine()
        self.drafter = ResponseDrafter(self.llm)


    def process_agent_workflow(self, customer_text:str) -> Dict[str, Any]:
        """Processes customer message through full AI support pipeline."""

        # flow 1: Classify Intent
        classification = self.classifier.classify(customer_text)
        intent = classification.get("intent", "other")
        confidence = float(classification.get("confidence", 0.0))

        # flow 2: retrive context grounded
        retrieved_items = self.retriever.retrieve(customer_text, top_k=2)

        # flow 3: Evaluate Escalation Policy
        escalation_result = self.escalation_engine.evaluate(intent, confidence, customer_text)

        # flow 4: Draft Reply (or Escalation notice)
        if escalation_result["escalate"]:
            reply = f"Thank you for contacting us. Your request has been escalated to a human specialist. Reason: {escalation_result['reason']}"
        else:
            reply = self.drafter.draft(customer_text, intent, retrieved_items)
        return {
            "customer_text": customer_text,
            "intent": intent,
            "confidence": confidence,
            "reasoning": classification.get("reasoning", ""),
            "escalated": escalation_result["escalate"],
            "escalation_reason": escalation_result["reason"],
            "retrieved_context": retrieved_items,
            "final_reply": reply
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process customer message through AI Support Pipeline.")
    parser.add_argument("--text", "-t", type=str, help="Customer message to process.")
    args = parser.parse_args()
    pipeline = AgentPipeline()
    if args.text:
        res = pipeline.process_agent_workflow(args.text)
        print("\n" + "="*50)
        print(" PIPELINE EXECUTION RESULT")
        print("="*50)
        print(f"Customer Query    : {res['customer_text']}")
        print(f"Intent            : {res['intent']} (Conf: {res['confidence']})")
        print(f"Escalated         : {res['escalated']}")
        print(f"Escalation Reason : {res['escalation_reason']}")
        print(f"Final Reply       :\n{res['final_reply']}\n")
    else:
        sample_query = "My package was supposed to arrive yesterday but it still says in transit. Where is my order #12345?"
        res = pipeline.process_agent_workflow(sample_query)
        print("\n" + "="*50)
        print(" PIPELINE EXECUTION DEMO")
        print("="*50)
        print(f"Customer Query    : {res['customer_text']}")
        print(f"Intent            : {res['intent']} (Conf: {res['confidence']})")
        print(f"Escalated         : {res['escalated']}")
        print(f"Final Reply       :\n{res['final_reply']}\n")