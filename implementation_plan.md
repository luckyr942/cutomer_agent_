# Implementation Plan: Hiver AI Customer Support Agent & Evaluation System

This document provides a comprehensive, phased roadmap to build, evaluate, and document the **AI Customer Support & Evaluation Framework** for the Hiver assignment.

## User Review Required

> [!IMPORTANT]
> **Manual Code Writing Mode**: The user has requested to write all terminal commands and code files line-by-line themselves. Each step in this plan will provide exact bash commands, code snippets, and rationale so the user can execute and understand every line.

> [!NOTE]
> **Data Download Requirement**: Kaggle credentials (`kaggle.json`) are required to fetch the dataset `thoughtvector/customer-support-on-twitter`. Step 2 provides complete setup instructions for local Kaggle API authentication.

---

## 1. Project Directory Structure

Target root directory: `hiver-support-agent`

```
hiver-support-agent/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── run_pipeline.sh
├── data/
│   ├── download.py
│   ├── make_sample.py
│   ├── raw/                  # (git-ignored) twcs.csv
│   ├── processed/            # (git-ignored) brand_conversations.json
│   └── sample/               # sample_twcs.csv for quick testing
├── src/
│   ├── __init__.py
│   ├── config.py             # Global paths and model settings
│   ├── explore.py            # Dataset column and data-type inspection
│   ├── analyze_brands.py     # Brand volume & conversation quality analyzer
│   ├── preprocess.py         # Conversation graph thread reconstruction
│   ├── intents.py           # Intent taxonomy definitions
│   ├── baselines.py          # Majority & Keyword matching baselines
│   ├── retrieval.py          # TF-IDF historical conversation retriever
│   ├── llm_client.py         # OpenAI / LLM API wrapper with retry logic
│   └── agent/
│       ├── __init__.py
│       ├── classify.py       # LLM-based intent classifier
│       ├── draft_reply.py    # Grounded response generator
│       ├── escalate.py       # Safety escalation engine
│       └── pipeline.py       # End-to-end agent orchestrator
├── eval/
│   ├── __init__.py
│   ├── build_golden_set.py   # Golden evaluation set sampler
│   ├── metrics.py            # Accuracy, Macro-F1, FNR, Precision/Recall
│   ├── llm_judge.py          # LLM-as-Judge scoring (1-5 scales)
│   ├── build_human_calib.py  # Human annotation sampling script
│   └── human_agreement.py    # Pearson/Kappa agreement calculator
├── tests/
│   ├── test_preprocess.py
│   ├── test_retrieval.py
│   ├── test_escalation.py
│   └── test_agent.py
└── report/
    ├── REPORT.md             # Final evaluation & failure analysis report
    └── decision_log.md       # Architectural decisions & trade-offs
```

---

## 2. Phased Execution Roadmap

### Phase 1: Environment Setup & Data Pipeline (Steps 1–6)
- **Goal**: Initialize environment, download dataset from Kaggle, inspect columns/authors, and reconstruct conversation threads.
- **Commands**:
  ```bash
  mkdir hiver-support-agent
  cd hiver-support-agent
  python3 -m venv .venv
  source .venv/bin/activate
  ```
- **Files Created**: `requirements.txt`, `.gitignore`, `.env.example`, `src/config.py`, `data/download.py`, `src/explore.py`, `src/analyze_brands.py`, `src/preprocess.py`.

### Phase 2: Brand Selection & Conversation Threading (Steps 7–10)
- **Goal**: Analyze top 30 brands by tweet count, multi-turn ratio, and average conversation length. Reconstruct conversation graph using `in_response_to_tweet_id` pointers.
- **Files Created**: `src/analyze_brands.py`, `src/preprocess.py`.
- **Output**: `data/processed/brand_conversations.json`.

### Phase 3: Intent Taxonomy Discovery & Simple Baselines (Steps 11–13)
- **Goal**: Sample 150 opening customer messages to establish intent categories (`delivery_delay`, `payment_issue`, `refund_request`, etc.). Implement Majority Class and Keyword Regex baselines.
- **Files Created**: `src/intents.py`, `src/baselines.py`.

### Phase 4: Grounded AI Agent Development (Steps 14–16)
- **Goal**: Build TF-IDF retriever for historical resolved conversations, LLM structured intent classifier, grounded reply generator, and rule-based escalation filter.
- **Files Created**: `src/retrieval.py`, `src/llm_client.py`, `src/agent/classify.py`, `src/agent/draft_reply.py`, `src/agent/escalate.py`, `src/agent/pipeline.py`.

### Phase 5: Golden Benchmark & Evaluation Suite (Steps 17–19)
- **Goal**: Construct 150–250 sample golden benchmark with ground-truth intent labels and escalation flags. Calculate Intent F1, Confusion Matrix, and Escalation FNR.
- **Files Created**: `eval/build_golden_set.py`, `eval/metrics.py`.

### Phase 6: LLM-as-Judge, Human Calibration & Failure Analysis (Steps 20–22)
- **Goal**: Implement multi-criteria LLM Judge (Faithfulness, Helpfulness, Actionability, Tone). Annotate 30–50 human calibration samples and calculate agreement metrics. Analyze failure cases.
- **Files Created**: `eval/llm_judge.py`, `eval/build_human_calib.py`, `eval/human_agreement.py`, `report/REPORT.md`, `report/decision_log.md`.

### Phase 7: Verification, Automated Tests & Final Packaging (Steps 23–25)
- **Goal**: Write unit tests (`pytest`), build unified script `run_pipeline.sh`, write comprehensive `README.md`, and perform final verification.
- **Files Created**: `tests/test_*.py`, `run_pipeline.sh`, `README.md`.

---

## 3. Verification Plan

### Automated Tests
```bash
# Run pytest suite
pytest tests/ -v

# Verify full end-to-end pipeline execution
bash run_pipeline.sh --sample-mode
```

### Manual Verification Steps
1. Verify `data/raw/twcs.csv` is correctly downloaded and parsed.
2. Confirm top brands analysis outputs clear metrics (conversation count, avg length).
3. Validate reconstructed conversations contain both customer prompt and brand response.
4. Verify baseline classifiers achieve deterministic predictions.
5. Verify escalation rules correctly trigger on high-risk intents (e.g., `payment_issue`).
6. Check confusion matrix and LLM judge agreement outputs.
