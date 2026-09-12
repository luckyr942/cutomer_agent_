# Changelog & System Upgrades

All notable technical upgrades, bug fixes, and architectural guardrails applied to the Customer Support Agent are documented below.

---

## [v0.2.0] - Robust Intent Classification, Error Resiliency & Eval Guardrails

### 1. Architectural Guardrails & Defensive Handling

* **Zero-Crash Return Contract (`src/llm_client.py`)**:
  * Fixed an OpenAI SDK `Choice` schema regression where `.messages` was called instead of the singular `.message`.
  * Guaranteed strict string returns (`return content.strip()`) even on empty, partial, or anomalous LLM responses, eliminating downstream `AttributeError: 'NoneType' object has no attribute 'strip'` crashes.

* **Strict API Endpoint Alignment (`src/config.py`)**:
  * Corrected invalid base URL routing from OpenRouter model paths to the standard endpoint: `https://openrouter.ai/api/v1`.
  * Added `override=True` inside `load_dotenv` to protect against stale shell exports overriding project `.env` definitions.

* **Markdown Fence & Sanitization Stripping (`src/agent/classify.py`)**:
  * Added defensive JSON extraction that strips markdown backticks (```` ```json ```` and ```` ``` ````).
  * Implemented an outer curly-brace extraction fallback to cleanly isolate JSON payloads even when the LLM appends conversational commentary.

* **Two-Tier Failover Architecture (`src/agent/classify.py`)**:
  * Implemented seamless failover to keyword heuristics if the LLM API times out, fails rate limits, or outputs unparseable JSON.
  * System remains operational even during external network outages.

---

### 2. Typo, Slang & Noisy Text Tolerance

* **Stem-Based Keyword Fallback (`src/intent.py`)**:
  * Corrected an indentation bug in `classify_intent_by_keywords()` where `return "other"` was placed inside the loop body, terminating evaluation after inspecting only the first category.
  * Upgraded keyword rules from strict exact-match tokens to linguistic stems (`pay`, `stuck`, `charg`, `deliver`, `packag`, `deduct`, `broken`). This catches plural forms, altered tenses, and typos without external spellcheck libraries.

* **Contextual Prompt Framing**:
  * Injected explicit system prompt instructions informing the model that customer messages contain phonetic spellings, typos, and fragmented grammar, allowing semantic normalization.

---

### 3. Transparent Explainability & Observability

* **Dynamic Fallback Reasoning**:
  * Replaced the static `"Fallback to keyword classifier."` string with an explainability function that cites the specific lexical stems matched during classification.

* **CLI Dual-Mode Execution**:
  * Added CLI support using `argparse`:
    * One-shot evaluation: `python src/agent/classify.py --text "<query>"`
    * Interactive REPL mode: `python src/agent/classify.py`

---

### 4. Automated Evaluation & Quality Assurance

* **Benchmark Suite (`eval/test_classifier.py`)**:
  * Created an automated test suite covering:
    * Typo tolerance & truncated text.
    * SMS shorthand and informal syntax.
    * Non-actionable noise vs. clear customer complaints.
    * Prompt injection defense.
  * Added validation assertions ensuring predicted labels conform to `INTENT_TAXONOMY` and confidence values remain bounded within `[0.0, 1.0]`.