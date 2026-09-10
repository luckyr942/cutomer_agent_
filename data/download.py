import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import RAW_DATA_DIR, RAW_CSV_PATH


def download_twcs():
    """Downloads and extracts the Customer Support on Twitter dataset from Kaggle."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if RAW_CSV_PATH.exists():
        print(f"✅ Real dataset already exists at:\n   {RAW_CSV_PATH}")
        return

    print("⏬ Initiating Kaggle download for 'thoughtvector/customer-support-on-twitter'...")

    try:
        from kaggle.api.kaggle_api_extended import KaggleApi

        api = KaggleApi()
        api.authenticate()

        api.dataset_download_files(
            dataset="thoughtvector/customer-support-on-twitter",
            path=RAW_DATA_DIR,
            unzip=True
        )

        print(f"✅ Successfully downloaded and extracted twcs.csv to:\n   {RAW_CSV_PATH}")

    except Exception as e:
        print(f"\n⚠️ Kaggle API Download failed: {e}")
        print("\n" + "=" * 60)
        print("MANUAL DOWNLOAD INSTRUCTIONS:")
        print("1. Download twcs.csv from Kaggle:")
        print("   https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter")
        print(f"2. Unzip and place twcs.csv inside:\n   {RAW_DATA_DIR}/twcs.csv")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    download_twcs()