# 🏗️ Procurement Lakehouse

A production-grade data engineering portfolio project that ingests World Bank procurement documents, transforms them through a medallion architecture, and serves interactive dashboards.

## 🏛️ Architecture
World Bank API
↓
Python Ingestion → Parquet (Bronze)
↓
dbt Silver Layer (cleaned + typed)
↓
dbt Gold Layer (business marts)
↓
DuckDB + Streamlit Dashboard
## 🛠️ Stack

| Layer | Tool |
|-------|------|
| Ingestion | Python + requests |
| Storage | Parquet files |
| Transform | dbt-core + DuckDB |
| Quality | dbt tests + Great Expectations |
| Orchestration | Python pipeline |
| Dashboard | Streamlit + Plotly |
| CI/CD | GitHub Actions |

## 🚀 Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run full pipeline
python3 orchestration/pipeline.py

# Run data quality checks
python3 quality/ge_checks.py

# Launch dashboard
streamlit run dashboards/app.py
```

## ✅ Data Quality
- 10 dbt schema tests (not_null + unique)
- 5 Great Expectations checks
- Bronze / Silver / Gold medallion architecture

## 📊 Dashboard
- 150+ World Bank procurement documents
- 8 regions, 114 projects, 18 document types
- Interactive charts + full-text search
