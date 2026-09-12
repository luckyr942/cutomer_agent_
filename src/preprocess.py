# process and reconstruct customer openning tweets and brand responses into multi-turn threds

import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
from src.config import RAW_CSV_PATH, SAMPLE_CSV_PATH, PROCESSED_CONVERSATION_PATH, DEFAULT_BRAND

def reconstruct_conversations(brand_filter: str = DEFAULT_BRAND):
    """Reconstructs customer opening tweets and brand responses into full threads."""
    if RAW_CSV_PATH.exists():
        df = pd.read_csv(RAW_CSV_PATH)
    else:
        df = pd.read_csv(SAMPLE_CSV_PATH)

    # Build tweet lookup dictionary
    tweet_dict = df.set_index('tweet_id').to_dict('index')

    conversations = []
    inbound_tweets = df[(df['inbound'] == True) & (df['text'].str.contains(f"@{brand_filter}", case=False, na=False))]

    for _, row in inbound_tweets.iterrows():
        opening_text = row['text']
        response_ids = str(row['response_tweet_id']).split(',')
        
        replies = []
        for r_id in response_ids:
            try:
                r_id_int = int(float(r_id))
                if r_id_int in tweet_dict:
                    replies.append(tweet_dict[r_id_int]['text'])
            except (ValueError, TypeError):
                continue
                
        if replies:
            conversations.append({
                "conversation_id": len(conversations) + 1,
                "brand": brand_filter,
                "customer_tweet_id": row['tweet_id'],
                "customer_text": opening_text,
                "brand_replies": replies
            })

    PROCESSED_CONVERSATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_CONVERSATION_PATH, 'w') as f:
        json.dump(conversations, f, indent=2)

    print(f"✅ Reconstructed {len(conversations)} conversation threads for @{brand_filter}.")
    print(f"Saved to: {PROCESSED_CONVERSATION_PATH}")

if __name__ == "__main__":
    reconstruct_conversations()
    