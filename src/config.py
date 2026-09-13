import os
from pathlib import Path
from dotenv import load_dotenv

# Root directory path
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Data paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"
EVAL_DIR = BASE_DIR / "eval"

RAW_CSV_PATH = RAW_DATA_DIR / "twcs.csv"
SAMPLE_CSV_PATH = SAMPLE_DATA_DIR / "sample_twcs.csv"
PROCESSED_CONVERSATION_PATH = PROCESSED_DATA_DIR / "brand_conversations.json"
BENCHMARK_SET_PATH = EVAL_DIR / "benchmark_set.csv"

# LLM Configuration (OpenRouter API)
OPENAI_API_KEY = (
    os.getenv("OPENROUTER_API_KEY_NEX_N2.5") 
    or os.getenv("OPENROUTER_API_KEY") 
    or os.getenv("OPENAI_API_KEY", "")
)
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "nex-agi/nex-n2.5-mini:free")

# Target Brand default
DEFAULT_BRAND = "AmazonHelp"