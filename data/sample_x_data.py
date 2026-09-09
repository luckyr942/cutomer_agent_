import sys
from pathlib import Path

# Ensure project root is in sys.path when running as a standalone script
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd 
from src.config import SAMPLE_DATA_DIR, SAMPLE_CSV_PATH

def generate_sample_synthetic_twcs():
    """Generates a small synthetic TWCS dataset matching Kaggle's schema."""
    SAMPLE_DATA_DIR.mkdir(parents=True, exist_ok=True)

    synthetic_data = [
        # Conversation1 :  Delivery Delay (AmazonHelp)
        {
            "tweet_id": 0,
            "author_id": "customer_1",
            "inbound": True,
            "created_at": "Wed Oct 11 10:00:00 +0000 2017",
            "text": "My package was supposed to arrive yesterday but it still says in transit. Where is my order #12345? @AmazonHelp",
            "response_tweet_id": "102",
            "in_response_to_tweet_id": None
        },
        {
            "tweet_id": 102,
            "author_id": "AmazonHelp",
            "inbound": False,
            "created_at": "Wed Oct 11 10:05:00 +0000 2017",
            "text": "We are sorry to hear that! Please send us a DM with your order number and full address so we can investigate.",
            "response_tweet_id": "103",
            "in_response_to_tweet_id": "101"
        },
        {
            "tweet_id": 103,
            "author_id": "customer_1",
            "inbound": True,
            "created_at": "Wed Oct 11 10:10:00 +0000 2017",
            "text": "I just sent you a DM with the order details.",
            "response_tweet_id": "104",
            "in_response_to_tweet_id": "102"
        },
        {
            "tweet_id": 104,
            "author_id": "AmazonHelp",
            "inbound": False,
            "created_at": "Wed Oct 11 10:15:00 +0000 2017",
            "text": "Thanks for the info! We checked your shipment and it is out for delivery today by 5 PM.",
            "response_tweet_id": None,
            "in_response_to_tweet_id": "103"
        },

        # Conversation 2: Payment Issue (AmazonHelp)
        {
            "tweet_id": 201,
            "author_id": "customer_2",
            "inbound": True,
            "created_at": "Wed Oct 11 11:00:00 +0000 2017",
            "text": "I was charged twice for my subscription this month! $14.99 deducted two times. Fix this immediately @AmazonHelp",
            "response_tweet_id": "202",
            "in_response_to_tweet_id": None
        },
        {
            "tweet_id": 202,
            "author_id": "AmazonHelp",
            "inbound": False,
            "created_at": "Wed Oct 11 11:03:00 +0000 2017",
            "text": "Apologies for the inconvenience! Please DM us your account email so our billing team can process a refund.",
            "response_tweet_id": None,
            "in_response_to_tweet_id": "201"
        },

        # Conversation 3: Product Defect / Inquiry (AppleSupport)
        {
            "tweet_id": 301,
            "author_id": "customer_3",
            "inbound": True,
            "created_at": "Wed Oct 11 12:00:00 +0000 2017",
            "text": "My iPhone screen keeps freezing after the latest iOS update. Any fix? @AppleSupport",
            "response_tweet_id": "302",
            "in_response_to_tweet_id": None
        },
        {
            "tweet_id": 302,
            "author_id": "AppleSupport",
            "inbound": False,
            "created_at": "Wed Oct 11 12:05:00 +0000 2017",
            "text": "We are here to help! Try restarting your device. If the issue persists, send us a DM with your iOS version.",
            "response_tweet_id": None,
            "in_response_to_tweet_id": "301"
        }
    ]

    df = pd.DataFrame(synthetic_data)
    df.to_csv(SAMPLE_CSV_PATH, index=False)
    print(f"Created Synthetic sample dataset with {len(df)} tweets at:\n {SAMPLE_CSV_PATH}")

if __name__ == "__main__":
    generate_sample_synthetic_twcs()


