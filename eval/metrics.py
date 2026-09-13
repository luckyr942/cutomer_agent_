# Quantitative Performance & Escalation Metrics Engine
# Evaluates AgentPipeline vs Baseline 1 (Majority Class) & Baseline 2 (Keyword Matcher)
# Computes Accuracy, Macro F1, Escalation False Negative Rate (FNR), and Classification Report.

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
from src.baseline import MajorityClassBaseline, KeywordBasedBaseline

def evaluate_all():
    """Evaluates AgentPipeline and 2 Baselines on 150 Benchmark Set."""
    if not BENCHMARK_SET_PATH.exists():
        print(f"⚠️ Benchmark set not found. Please run 'python eval/build_benchmark.py' first.")
        return

    df = pd.read_csv(BENCHMARK_SET_PATH)
    
    # Initialize Models
    pipeline = AgentPipeline()
    baseline_majority = MajorityClassBaseline()
    baseline_keyword = KeywordBasedBaseline()

    y_true_intent = df["ground_truth_intent"].tolist()
    y_true_escalate = df["should_escalate"].tolist()

    # Predictions
    pred_pipeline_intent, pred_pipeline_escalate = [], []
    pred_majority_intent, pred_majority_escalate = [], []
    pred_keyword_intent, pred_keyword_escalate = [], []

    print(f"⌛ Evaluating {len(df)} Benchmark queries across Pipeline & 2 Baselines...\n")

    for idx, row in df.iterrows():
        text = row["customer_text"]
        
        # 1. Proposed Agent Pipeline
        res_pipe = pipeline.process_agent_workflow(text)
        pred_pipeline_intent.append(res_pipe["intent"])
        pred_pipeline_escalate.append(res_pipe["escalated"])

        # 2. Baseline 1 (Trivial Majority Class: predicts delivery_delay, never escalates)
        pred_majority_intent.append(baseline_majority.predict(text))
        pred_majority_escalate.append(False)

        # 3. Baseline 2 (Simple Keyword Matcher)
        kw_intent = baseline_keyword.predict(text)
        pred_keyword_intent.append(kw_intent)
        # Simple keyword baseline escalates if intent is payment_issue
        pred_keyword_escalate.append(kw_intent == "payment_issue")

    def calc_metrics(y_true_i, y_pred_i, y_true_e, y_pred_e):
        acc = accuracy_score(y_true_i, y_pred_i)
        f1 = f1_score(y_true_i, y_pred_i, average="macro")
        fn_count = sum(1 for t, p in zip(y_true_e, y_pred_e) if t is True and p is False)
        positives = sum(1 for t in y_true_e if t is True)
        fnr = (fn_count / positives) if positives > 0 else 0.0
        return acc, f1, fnr, fn_count, positives

    p_acc, p_f1, p_fnr, p_fn, p_pos = calc_metrics(y_true_intent, pred_pipeline_intent, y_true_escalate, pred_pipeline_escalate)
    m_acc, m_f1, m_fnr, m_fn, _ = calc_metrics(y_true_intent, pred_majority_intent, y_true_escalate, pred_majority_escalate)
    k_acc, k_f1, k_fnr, k_fn, _ = calc_metrics(y_true_intent, pred_keyword_intent, y_true_escalate, pred_keyword_escalate)

    print("="*65)
    print(" 📊 HEADLINE RESULTS COMPARISON TABLE (150 BENCHMARK SAMPLES)")
    print("="*65)
    print(f"{'Model / Architecture':<30} | {'Accuracy':<10} | {'Macro F1':<10} | {'Escalation FNR':<12}")
    print("-" * 65)
    print(f"{'1. Baseline (Trivial Majority)':<30} | {m_acc*100:6.1f}%    | {m_f1:8.4f}  | {m_fnr*100:10.1f}% ({m_fn}/{p_pos})")
    print(f"{'2. Baseline (Simple Keyword)':<30} | {k_acc*100:6.1f}%    | {k_f1:8.4f}  | {k_fnr*100:10.1f}% ({k_fn}/{p_pos})")
    print(f"{'3. Proposed Support Agent Pipeline':<30} | {p_acc*100:6.1f}%    | {p_f1:8.4f}  | {p_fnr*100:10.1f}% ({p_fn}/{p_pos})")
    print("="*65)

    print("\n--- Proposed Agent Pipeline Detailed Intent Report ---")
    print(classification_report(y_true_intent, pred_pipeline_intent))

if __name__ == "__main__":
    evaluate_all()
