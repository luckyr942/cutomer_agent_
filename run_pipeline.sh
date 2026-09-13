#!/usr/bin/env bash
# ==============================================================================
# Hiver SDE Intern Assignment — End-to-End Execution & Evaluation Pipeline
# Brand: @AmazonHelp | Customer Support AI Agent
# ==============================================================================

set -e

# Detect Python interpreter
if [ -d ".venv" ]; then
    PYTHON_CMD=".venv/bin/python"
else
    PYTHON_CMD="python3"
fi

echo "========================================================================"
echo "🚀 1. DATA PREPROCESSING & BRAND CONVERSATION INGESTION (@AmazonHelp)"
echo "========================================================================"
$PYTHON_CMD data/make_synthetic_sample.py
$PYTHON_CMD scripts/ingest_brand.py

echo ""
echo "========================================================================"
echo "🎯 2. GOLDEN BENCHMARK DATASET GENERATION (150 Ground-Truth Samples)"
echo "========================================================================"
$PYTHON_CMD eval/build_benchmark.py

echo ""
echo "========================================================================"
echo "🤖 3. AGENT PIPELINE DEMO EXECUTION (Single Sample Query)"
echo "========================================================================"
$PYTHON_CMD src/agent/pipeline.py --text "My package was supposed to arrive yesterday but tracking has not updated. Where is order #12345?"

echo ""
echo "========================================================================"
echo "📊 4. QUANTITATIVE METRICS EVALUATION (Pipeline vs 2 Baselines)"
echo "========================================================================"
$PYTHON_CMD eval/metrics.py

echo ""
echo "========================================================================"
echo "⚖️ 5. LLM-AS-A-JUDGE RESPONSE QUALITY EVALUATION"
echo "========================================================================"
$PYTHON_CMD eval/llm_judge.py

echo ""
echo "========================================================================"
echo "🤝 6. HUMAN-JUDGE AGREEMENT & CORRELATION ANALYSIS"
echo "========================================================================"
$PYTHON_CMD eval/human_agreement.py

echo ""
echo "========================================================================"
echo "✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!"
echo "📄 Summary Reports Available:"
echo "   - Main Report: report/REPORT.md"
echo "   - Decision Log: report/decision_log.md"
echo "   - Golden Set Notes: eval/sampling_methodology.txt"
echo "========================================================================"
