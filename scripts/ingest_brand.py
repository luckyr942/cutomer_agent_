# Real Brand Conversation Extraction Script
# Extracts customer inbound tweets and brand response pairs from Kaggle / sample CSVs
# into data/processed/brand_conversations.json for realistic retrieval grounding.

import sys
import json
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import RAW_CSV_PATH, SAMPLE_CSV_PATH, PROCESSED_CONVERSATION_PATH, DEFAULT_BRAND

def ingest_conversations(brand: str = DEFAULT_BRAND, max_samples: int = 1000):
    csv_path = RAW_CSV_PATH if RAW_CSV_PATH.exists() else SAMPLE_CSV_PATH
    if not csv_path.exists():
        print(f"❌ Neither {RAW_CSV_PATH} nor {SAMPLE_CSV_PATH} exists. Run 'python data/make_synthetic_sample.py' first.")
        return

    print(f"📖 Ingesting historical conversations for @{brand} from {csv_path.name}...")
    
    try:
        df = pd.read_csv(csv_path, nrows=100000, low_memory=False)
    except Exception as e:
        print(f"Error reading {csv_path}: {e}")
        return

    # Filter tweets involving the target brand
    brand_replies = df[df["author_id"].astype(str).str.lower() == brand.lower()]
    
    # Map customer inbound tweet to company response
    merged = pd.merge(
        brand_replies,
        df,
        left_on="in_response_to_tweet_id",
        right_on="tweet_id",
        suffixes=("_brand", "_customer")
    )

    conversations = []
    for idx, row in merged.head(max_samples).iterrows():
        cust_text = str(row.get("text_customer", "")).strip()
        brand_reply = str(row.get("text_brand", "")).strip()
        if cust_text and brand_reply and cust_text != "nan" and brand_reply != "nan":
            conversations.append({
                "conversation_id": len(conversations) + 1,
                "brand": brand,
                "customer_tweet_id": row.get("tweet_id_customer"),
                "customer_text": cust_text,
                "brand_replies": [brand_reply]
            })

    PROCESSED_CONVERSATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_CONVERSATION_PATH, "w", encoding="utf-8") as f:
        json.dump(conversations, f, indent=2)

    print(f"✅ Successfully extracted {len(conversations)} historical threads to {PROCESSED_CONVERSATION_PATH}")

if __name__ == "__main__":
    ingest_conversations()
