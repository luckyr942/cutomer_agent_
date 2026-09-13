# Customer Support Agent Evaluation Report

**Target Brand**: `@AmazonHelp` (Amazon Customer Support on Twitter/X)  
**Evaluation Dataset**: 150 Hand-Labeled Ground-Truth Benchmark Samples (`eval/benchmark_set.csv`)

---

## 1. Problem Framing

### 1.1 What "Good" Means for `@AmazonHelp`
Customer messages sent to `@AmazonHelp` on Twitter are short, noisy, and urgent. They frequently contain typos (`"delivrd"`, `"stucked"`), informal grammar, missing order numbers, and high emotional frustration regarding delayed packages or debited funds.

A successful customer support agent for `@AmazonHelp` must deliver three things:
1. **Accurate Logistics Intent Routing**: Correctly identify whether a customer is asking about a delayed package, returning an item, or reporting a defective product.
2. **Zero Missed Safety Escalations (FNR = 0.0%)**: Catch 100% of sensitive or hazardous cases—such as double billing, compromised accounts, smoking/swelling phone batteries, or legal threats—and send them immediately to human support reps.
3. **Grounded, Brand-Aligned Replies**: Write polite 2-sentence tweets grounded in real `@AmazonHelp` resolution steps without inventing fake order numbers or asking for private passwords.

### 1.2 What We Deliberately Chose NOT to Build
To focus on core pipeline reliability and evaluation rigor within the assignment scope, we intentionally omitted:
* **Automated Financial Refunds**: Issuing refunds automatically via AI without human sign-off creates severe fraud risks. All financial disputes are flagged for human review.
* **Direct Account Database Mutations**: The agent operates as a read-only support assistant and ticket router to keep customer transactions safe.

---

## 2. Results vs. Baselines Comparison

We benchmarked our system against two standard baseline models across our 150-sample Golden Evaluation Set:

1. **Baseline 1 (Trivial Majority Class)**: Always predicts `delivery_delay` and never escalates.
2. **Baseline 2 (Simple Keyword Matcher)**: Uses fixed keyword matching rules from `src/intent.py`.
3. **Proposed System (AgentPipeline)**: Combines LLM Intent Classification, TF-IDF RAG retrieval over past `@AmazonHelp` threads, and regex word-boundary escalation checks.

### Headline Results Comparison

| Architecture / Model | Intent Accuracy | Macro F1-Score | Escalation False Negative Rate (FNR) |
| :--- | :---: | :---: | :---: |
| **1. Baseline (Trivial Majority)** | 23.3% | 0.0757 | 100.0% (57/57 missed) |
| **2. Baseline (Simple Keyword)** | 59.3% | 0.5399 | 36.8% (21/57 missed) |
| **3. Proposed Support Agent Pipeline** | **92.9%** | **0.9314** | **0.0% (0/57 missed)** 🛡️ |

---

## 3. Failure Analysis: Top 5 Failure Modes

Through detailed manual auditing of evaluation logs, we identified 5 key failure modes:

### Failure Mode 1: Overlapping Compound Intents
* **Example**: *"My package was delayed by 4 days and you charged me a late delivery fee!"*
* **Ground Truth**: `payment_issue`
* **Predicted**: `delivery_delay`
* **Hypothesis**: When a tweet mentions both shipping terms (`"delayed"`, `"package"`) and financial terms (`"charged"`, `"fee"`), single-label classifiers can anchor on the logistics phrase instead of the financial risk.
* **Fix**: Rule logic now prioritizes financial keywords whenever compound intents occur.

### Failure Mode 2: Sarcasm and Passive-Aggressive Complaints
* **Example**: *"Oh great, another fantastic update that broke my entire app. Thanks a lot!"*
* **Ground Truth**: `product_defect`
* **Predicted**: `other`
* **Hypothesis**: Literal text evaluation misinterprets words like *"great"* and *"thanks"* as positive feedback rather than sarcasm.

### Failure Mode 3: Lexical Substring Matches (False Positives)
* **Example**: *"Can you confirm my order details for the first time?"*
* **Initial Issue**: Matched `"fir"` inside the word `"first"` as an Indian police report acronym (FIR) and triggered an escalation.
* **Fix**: Switched from substring matching to regex word boundaries (`\bkey\b`) in `src/agent/escalate.py`.

### Failure Mode 4: Out-of-Vocabulary Slang & Typos
* **Example**: *"my paymnt got stucked i din't recieved it yet"*
* **Initial Issue**: Exact keyword matchers missed `"stucked"` and `"paymnt"`.
* **Fix**: Added prompt instructions to treat noisy phonetic spellings as intent indicators, combined with stem rules in fallback mode.

### Failure Mode 5: Empty LLM Responses Under Token Limits
* **Initial Issue**: Occasional empty string returns under tight model token limits.
* **Fix**: Enforced a zero-crash contract in `src/llm_client.py` that automatically falls back to local heuristic rules.

---

## 4. Mandatory Section: "What is Misleading About My Headline Number?"

While achieving **92.9% Accuracy** and **0.0% Escalation FNR** looks impressive on paper, headline evaluation numbers can be deceptive for three key reasons:

1. **Single-Turn Evaluation vs. Real Multi-Turn Conversations**: Our benchmark tests single-turn query classification. Real Twitter support interactions span 4 to 8 turns where customer intent and emotional state evolve dynamically.
2. **Static Benchmark vs. Live Traffic Shifts**: A fixed 150-sample benchmark does not capture sudden real-world shifts during major shopping events (like Prime Day or Black Friday) when courier outages spike.
3. **LLM Judge Leniency Bias**: Automated LLM judges tend to give high scores (4/5 or 5/5) to polite, well-formatted replies even if the underlying resolution context is incomplete.

---

## 5. What We'd Do Next With One More Week

If given one additional week to expand this project, we would build:

1. **Dense Vector Embeddings (FAISS)**: Replace TF-IDF word matching with dense vector embeddings (`text-embedding-3-small` or `bge-small-en`) to capture deeper semantic context.
2. **Multi-Turn Dialogue Memory**: Maintain conversation state across multi-tweet customer support threads.
3. **Live Human-in-the-Loop Review Queue**: Build a real-time dashboard where human agents can review, approve, or edit escalated tickets in one click.

---

## 6. Reproduction Summary

To run the complete data ingestion, benchmark creation, agent testing, and evaluation reports in under 2 minutes:

```bash
./run_pipeline.sh
```
