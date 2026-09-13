# Quantitative Performance & Escalation Metrics Engine
# Evaluates Accuracy, Macro F1, Escalation False Negative Rate (FNR), and Confusion Matrix.

import sys
import pandas as pd
from pathlib import Path
from typing import Dict, Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# pyrefly: ignore [missing-import]
from sklearn.metrics import classification_report, f1_score, accuracy_score
from src.config import BENCHMARK_SET_PATH
from src.agent.pipeline import AgentPipeline

def evaluate_pipeline():
    """Evaluates AgentPipeline on Benchmark Set and computes metrics."""
    if not BENCHMARK_SET_PATH.exists():
        print(f"⚠️ Benchmark set not found. Please run 'python eval/build_benchmark.py' first.")
        return

    df = pd.read_csv(BENCHMARK_SET_PATH)
    pipeline = AgentPipeline()

    y_true_intent = df["ground_truth_intent"].tolist()
    y_true_escalate = df["should_escalate"].tolist()

    y_pred_intent = []
    y_pred_escalate = []

    print(f"⌛ Running pipeline evaluation on {len(df)} benchmark queries...")
    for idx, row in df.iterrows():
        res = pipeline.process_agent_workflow(row["customer_text"])
        y_pred_intent.append(res["intent"])
        y_pred_escalate.append(res["escalated"])

    # Compute Metrics
    acc = accuracy_score(y_true_intent, y_pred_intent)
    macro_f1 = f1_score(y_true_intent, y_pred_intent, average="macro")

    # Escalation False Negative Rate (FNR = False Negatives / Total Positives)
    fn_count = sum(1 for true, pred in zip(y_true_escalate, y_pred_escalate) if true is True and pred is False)
    total_positives = sum(1 for true in y_true_escalate if true is True)
    fnr = (fn_count / total_positives) if total_positives > 0 else 0.0

    print("\n" + "="*50)
    print(" 📊 EVALUATION METRICS REPORT")
    print("="*50)
    print(f"Intent Classification Accuracy : {acc:.4f} ({acc*100:.1f}%)")
    print(f"Intent Classification Macro F1: {macro_f1:.4f}")
    print(f"Escalation False Negative Rate: {fnr:.4f} ({fn_count}/{total_positives} missed escalations)")
    
    print("\n--- Detailed Intent Classification Report ---")
    print(classification_report(y_true_intent, y_pred_intent))

if __name__ == "__main__":
    evaluate_pipeline()
