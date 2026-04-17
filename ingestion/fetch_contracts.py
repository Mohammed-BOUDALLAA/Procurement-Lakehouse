import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

# =========================
# Config
# =========================
RAW_DIR = Path("data/raw/contracts")
RAW_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# Fetch البيانات
# =========================
def fetch_worldbank_documents(page: int = 1, page_size: int = 50) -> dict:
    url = "https://search.worldbank.org/api/v2/wds"

    params = {
        "format": "json",
        "rows": page_size,
        "os": (page - 1) * page_size,
    }

    try:
        response = requests.get(url, params=params, timeout=30)

        print(f"🌐 Fetching: {response.url} | Status: {response.status_code}")

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return {}


# =========================
# Extract
# =========================
def extract_documents(result: dict) -> list[dict]:
    if not result or "documents" not in result:
        return []

    return list(result["documents"].values())


# =========================
# Save (Parquet + fallback CSV)
# =========================
def save_data(data: list[dict], page: int):
    df = pd.DataFrame(data)
    today = datetime.now().strftime("%Y-%m-%d")

    # حاول Parquet
    try:
        file_path = RAW_DIR / f"contracts_{today}_page{page}.parquet"
        df.to_parquet(file_path, index=False)
        print(f"✅ Saved {len(df)} records → {file_path}")

    except Exception:
        print("⚠️ Parquet not available, fallback to CSV")

        file_path = RAW_DIR / f"contracts_{today}_page{page}.csv"
        df.to_csv(file_path, index=False)
        print(f"✅ Saved {len(df)} records → {file_path}")


# =========================
# Ingestion Pipeline
# =========================
def ingest(pages: int = 3, page_size: int = 50):
    print("🚀 Starting ingestion...")

    total_records = 0

    for page in range(1, pages + 1):
        print(f"\n📄 Page {page}")

        result = fetch_worldbank_documents(page, page_size)
        documents = extract_documents(result)

        if not documents:
            print("⚠️ No data found, stopping...")
            break

        save_data(documents, page)
        total_records += len(documents)

        time.sleep(1)  # avoid rate limiting

    # fallback إذا API عطا والو
    if total_records == 0:
        print("⚠️ Using fallback dummy data...")

        dummy_data = [
            {"id": 1, "title": "Sample Contract A", "amount": 1000},
            {"id": 2, "title": "Sample Contract B", "amount": 2000},
        ]

        save_data(dummy_data, page=0)

    print(f"\n✅ Ingestion complete! Total records: {total_records}")


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    ingest(pages=3, page_size=50)