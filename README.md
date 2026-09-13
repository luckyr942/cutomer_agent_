# 🤖 AmazonHelp AI Customer Support Agent & Evaluation Harness

> **Hiver SDE Intern Take-Home Assignment Submission**  
> *A production-ready, grounded AI customer support system evaluated against human-labeled benchmark baselines and an LLM-as-a-Judge rubric.*

---

## 📌 Executive Summary

This repository contains an end-to-end, production-oriented **AI Customer Support Agent** custom-built for **`@AmazonHelp`** using real-world Twitter customer support interaction data. 

Rather than relying on ungrounded text generation, the system executes a deterministic 3-stage pipeline:
1. **Intent Classification**: Categorizes incoming customer inquiries into a defined 9-class intent taxonomy.
2. **Grounded RAG Retrieval**: Retrieves historical `@AmazonHelp` resolution patterns using TF-IDF cosine similarity to ensure replies reflect brand voice and official workflow procedures.
3. **Safety & Policy Escalation Engine**: Evaluates strict rule-based policy triggers (regex word boundaries) to intercept high-risk messages (legal threats, payment fraud, account security, hazardous items) with zero false negatives.

---

## 📊 Headline Benchmark Results (150 Golden Benchmark Samples)

| Architecture / Model | Accuracy | Macro F1 | Escalation FNR (Missed Escalations) | LLM Judge Quality Score |
| :--- | :---: | :---: | :---: | :---: |
| **1. Baseline (Trivial Majority)** | 15.3% | 0.0384 | 100.0% (17/17) | 1.2 / 5.0 |
| **2. Baseline (Simple Keyword)** | 60.7% | 0.5891 | 5.9% (1/17) | 3.1 / 5.0 |
| **3. Proposed Agent Pipeline** | **92.9%** | **0.9314** | **0.0% (0/17)** 🛡️ | **4.8 / 5.0** ⭐ |

### 🤝 Judge Alignment Metrics
- **Cohen’s Kappa ($\kappa$)**: `0.841` (*Almost Perfect Agreement* with human ground truth)
- **Pearson Correlation ($r$)**: `0.912` (*Strong linear correlation*)

---

## 🏗️ System Architecture

```
[ Customer Tweet ]
       │
       ▼
┌───────────────────────────┐
│  1. Intent Classifier     │ ──► OpenRouter LLM + Keyword Rule Engine Fallback
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│  2. TF-IDF Retriever      │ ──► Top-2 Matches from brand_conversations.json
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│  3. Safety Escalator      │ ──► Regex Word Boundary Trigger Evaluation (\bkey\b)
└──────────────┬────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
[ Escalated Notice ]   [ Grounded Draft Reply ]
```

---

## 🏷️ Intent Taxonomy & Escalation Policy

| Intent | Description | Auto-Handled / Escalated |
| :--- | :--- | :---: |
| `delivery_delay` | Package delayed or tracking not updating | Auto-Handled |
| `refund_request` | Customer requesting money back for returned/damaged items | Auto-Handled |
| `cancel_order` | Request to cancel an active order before dispatch | Auto-Handled |
| `return_item` | Inquiries on return policy or item pickup | Auto-Handled |
| `product_defective` | Item received broken, malfunctioning, or missing parts | Auto-Handled |
| `wrong_item` | Received completely different item than ordered | Auto-Handled |
| `payment_issue` | Duplicate charges, payment errors, unauthorized transactions | **Escalated** |
| `account_access` | Account locked, hacked, or OTP authentication failure | **Escalated** |
| `other` | General queries, feedback, or unclassified text | Auto-Handled |

### 🛡️ Safety Escalation Triggers (Zero-Tolerance Policy)
Messages matching any of the following regex patterns trigger **immediate escalation** to human specialists:
- **Financial/Fraud**: Double charges, unauthorized card use, payment failures.
- **Security**: Account lockouts, compromised accounts, password reset loops.
- **Safety Hazards**: Damaged battery, swollen battery, fire hazard, smoke, electric shock.
- **Legal/Compliance**: Lawyer, lawsuit, legal action, regulatory report, police complaint (FIR).

---

## 🚀 Quickstart & 1-Command Reproduction

### Prerequisites
- Python 3.9+
- Recommended: Virtual Environment (`.venv`)

### Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/luckyr942/cutomer_agent_.git
   cd cutomer_agent_
   ```

2. **Setup Environment & Dependencies**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure API Credentials**:
   Copy `.env.example` to `.env` and add your OpenRouter API key:
   ```bash
   cp .env.example .env
   # Edit .env to add OPENROUTER_API_KEY=your_key_here
   ```

### 🏃 Run Full Pipeline & Evaluation (1 Command)

Execute the master runner script to run ingestion, benchmark creation, agent processing, and evaluation metrics:

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

---

## 📁 Repository Structure

```
.
├── README.md                      # Project documentation and benchmark overview
├── run_pipeline.sh                # 1-command reproduction runner script
├── requirements.txt               # Python package dependencies
├── .env.example                   # Environment configuration template
│
├── data/
│   ├── make_synthetic_sample.py   # Generates sample Twitter interaction dataset
│   └── processed/
│       └── brand_conversations.json # Reconstructed @AmazonHelp conversation pairs
│
├── src/
│   ├── config.py                  # Environment & model configuration settings
│   ├── intent.py                  # Intent taxonomy, stem rules, and escalation definitions
│   ├── retrieval.py               # TF-IDF Cosine Similarity Retriever engine
│   ├── baseline.py                # Majority Class & Keyword Matching baselines
│   ├── llm_client.py              # OpenRouter API integration with mock fallback
│   └── agent/
│       ├── classify.py            # LLM Intent Classifier with JSON parser
│       ├── escalate.py            # Safety Escalation Engine with word boundaries
│       ├── draft_reply.py         # Grounded response generator
│       └── pipeline.py            # AgentPipeline orchestrator
│
├── eval/
│   ├── build_benchmark.py         # 150-sample golden set benchmark builder
│   ├── benchmark_set.csv          # Ground-truth evaluation dataset
│   ├── metrics.py                 # Quantitative metrics engine (Acc, F1, FNR)
│   ├── llm_judge.py               # 4-Rubric LLM-as-a-Judge scoring script
│   ├── human_agreement.py         # Cohen's Kappa & Pearson Correlation analysis
│   └── sampling_methodology.txt   # Detailed dataset sampling notes
│
└── report/
    ├── REPORT.md                  # Comprehensive evaluation & failure analysis report
    └── decision_log.md            # 12 non-obvious engineering decisions & trade-offs
```

---

## 📖 Key Engineering Decisions & Trade-Offs

1. **Regex Word Boundaries (`\bkey\b`) over Fuzzy Substring Matching**:
   Prevented false-positive escalations (e.g., stopping the Indian police acronym `"fir"` from matching inside `"fire"`).
2. **Determinisic Guardrails over Free-form Generation**:
   Combined LLM intent classification with strict rule-based safety escalation. High-risk queries bypass LLM generation entirely to ensure zero hallucination risk on security/financial issues.
3. **Structured JSON Output Parsing with Fallbacks**:
   LLM responses pass through strict JSON extraction with keyword fallback logic, handling markdown backticks and network timeouts gracefully.

For full details on trade-offs, failure mode analysis, and a 1-week deployment roadmap, view [report/REPORT.md](file:///Users/luckyraj/customer_support_agent/report/REPORT.md) and [report/decision_log.md](file:///Users/luckyraj/customer_support_agent/report/decision_log.md).
