import subprocess
import sys
from pathlib import Path
from datetime import datetime

INGESTION_SCRIPT = Path(__file__).parent.parent / "ingestion" / "fetch_contracts.py"
DBT_DIR = Path(__file__).parent.parent / "dbt_project"
PYTHON = sys.executable
DBT = str(Path(PYTHON).parent / "dbt")

def run_step(name: str, cmd: list, cwd=None):
    print(f"\n{'='*50}")
    print(f"🚀 [{datetime.now().strftime('%H:%M:%S')}] Starting: {name}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, cwd=cwd, text=True)
    if result.returncode != 0:
        print(f"❌ FAILED: {name}")
        sys.exit(1)
    print(f"✅ DONE: {name}")

def main():
    print(f"\n🏗️  Procurement Lakehouse Pipeline")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    run_step("Ingestion", [PYTHON, str(INGESTION_SCRIPT)])
    run_step("dbt run",   [DBT, "run"],  cwd=DBT_DIR)
    run_step("dbt test",  [DBT, "test"], cwd=DBT_DIR)

    print(f"\n🎉 Pipeline completed successfully!")

if __name__ == "__main__":
    main()
