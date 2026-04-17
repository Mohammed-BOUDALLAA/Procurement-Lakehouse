import duckdb
from pathlib import Path

RAW_DIR = Path("data/raw/contracts")

df = duckdb.query(f"""
    SELECT * FROM read_parquet('{RAW_DIR}/*.parquet', union_by_name=True)
""").df()

print(f"📊 Total records: {len(df)}")
print(f"📋 Columns ({len(df.columns)}):")
for col in df.columns:
    print(f"   - {col}")

print(f"\n🔍 Sample:")
print(df[['id', 'display_title', 'docty', 'docdt']].head(5).to_string())
