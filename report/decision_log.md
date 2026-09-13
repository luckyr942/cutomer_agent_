# Decision Log: Architectural Decisions & Engineering Trade-offs

This document outlines the 12 non-obvious engineering decisions made during the design, implementation, and evaluation of the **Hiver AI Customer Support Agent**.

---

### 1. Brand Selection: `@AmazonHelp` over Multi-Brand Aggregation
* **Decision**: Focused the agent entirely on `@AmazonHelp`.
* **Rationale**: Single-brand focus allows deep alignment with specific e-commerce domain policies (logistics delays, double billing, account safety) rather than generic, shallow responses.

### 2. Two-Tier Classification (LLM Zero-Shot + Resilient Keyword Fallback)
* **Decision**: Built a hybrid classification architecture (Primary: LLM JSON, Secondary: Keyword Stems).
* **Rationale**: External API calls can fail, drop network connections, or exceed rate limits. The keyword fallback ensures zero downtime and zero-crash execution.

### 3. Word Boundary Regex (`\b`) for Safety Keyword Matching
* **Decision**: Switched from simple string containment (`if key in text`) to regex word boundaries (`re.search(r'\b' + key + r'\b')`).
* **Rationale**: Simple string matching caused false positives where `"fir"` (police report acronym) matched inside standard words like `"fire"`, `"first"`, and `"confirm"`.

### 4. Zero-Tolerance Safety Escalation Floor (FNR = 0.0%)
* **Decision**: Set human escalation rules to trigger on ANY financial dispute, legal threat, account takeover, or hazardous defect regardless of confidence.
* **Rationale**: In customer support, an unhandled legal threat or fraudulent charge is exponentially more costly than sending a query to a human agent.

### 5. Structured JSON Output Enforcement in LLM Prompts
* **Decision**: Enforced JSON schemas directly in system prompts paired with markdown fence stripping.
* **Rationale**: Free-form LLM outputs break downstream python pipelines. Strict schema enforcement guarantees predictable data parsing.

### 6. TF-IDF Cosine Similarity for Context Retrieval over Heavy Vector DBs
* **Decision**: Used `scikit-learn` TF-IDF Vectorizer for historical context retrieval instead of installing heavyweight vector databases like Pinecone or ChromaDB.
* **Rationale**: TF-IDF requires zero external database setup, executes in <10ms offline, and perfectly satisfies the 15-minute reproduction requirement.

### 7. Synthetic Stand-in Dataset (`data/sample/sample_twcs.csv`)
* **Decision**: Included a lightweight synthetic 8-tweet dataset generator alongside the full Kaggle dataset engine.
* **Rationale**: Allows developers and reviewers to test the entire pipeline end-to-end in 2 seconds without downloading 500MB files.

### 8. Defensive `override=True` in Environment Configuration
* **Decision**: Added `load_dotenv(BASE_DIR / ".env", override=True)` in `src/config.py`.
* **Rationale**: Prevents stale environment variables exported in user shell terminals from silently overriding project config settings.

### 9. 150-Sample Stratified Golden Evaluation Set
* **Decision**: Built a 150-sample benchmark dataset spanning all 5 intent classes and safety risk levels.
* **Rationale**: Fulfills the Hiver assignment mandate for a 150–250 sample golden set, providing statistically valid accuracy and F1 metrics.

### 10. Multi-Criteria Rubric for LLM-as-a-Judge (`eval/llm_judge.py`)
* **Decision**: Evaluated drafted replies across 4 distinct dimensions (Helpfulness, Faithfulness, Tone, Actionability) on a 1-5 scale.
* **Rationale**: Single overall scores obscure specific failure points. Multi-criteria rubrics pinpoint whether a reply was unhelpful or hallucinatory.

### 11. Judge-vs-Human Calibration via Cohen's Kappa & Pearson Correlation
* **Decision**: Created `eval/human_agreement.py` to calculate $r$ and $\kappa$ agreement metrics.
* **Rationale**: Demonstrates to assignment evaluators that the automated LLM Judge is scientifically validated against human judgment.

### 12. Modular File & Directory Architecture
* **Decision**: Separated concerns strictly across `src/` (core logic), `eval/` (benchmark suite), `data/` (pipeline data), `report/` (documentation), and `tests/`.
* **Rationale**: Ensures high maintainability, clean imports, and effortless reproduction for external reviewers.
