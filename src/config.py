# import os 
# from pathlib import Path
# # pyrefly: ignore [missing-import]
# from dotenv import load_dotenv

# load_dotenv()

# #Root dir
# BASE_DIR = Path(__file__).resolve().parent.parent

# #Data paths
# DATA_DIR = BASE_DIR / "data"
# RAW_DATA_DIR = DATA_DIR / "raw"
# PROCESSED_DATA_DIR = DATA_DIR / "processed"
# SAMPLE_DATA_DIR = DATA_DIR / "sample"

# RAW_CSV_PATH = RAW_DATA_DIR / "twcs.csv"
# PROCESSED_CONVERSATION_PATH = PROCESSED_DATA_DIR / "brand_conversations.json"
# GOLDEN_SET_PATH = BASE_DIR / "eval" / "golden_set.csv"

# #LLM configuration
# OPENAI_API_KEY = os.getenv("OPENROUTER_API_KEY_NEX_N2.5") or os.getenv("OPENAI_API_KEY", "")
# OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/nex-agi/nex-n2.5-mini:free")
# DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "nex-agi/nex-n2.5-mini:free")


import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Root directory path
BASE_DIR = Path(__file__).resolve().parent.parent

# Data paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"

RAW_CSV_PATH = RAW_DATA_DIR / "twcs.csv"
SAMPLE_CSV_PATH = SAMPLE_DATA_DIR / "sample_twcs.csv"
PROCESSED_CONVERSATION_PATH = PROCESSED_DATA_DIR / "brand_conversations.json"
GOLDEN_SET_PATH = BASE_DIR / "eval" / "golden_set.csv"

# LLM Configuration (OpenRouter API)
OPENAI_API_KEY = os.getenv("OPENROUTER_API_KEY_NEX_N2.5") or os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "nex-agi/nex-n2.5-mini:free")

# Target Brand default
DEFAULT_BRAND = "AmazonHelp"
