import great_expectations as gx
import duckdb
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "lakehouse.duckdb"

def run_checks():
    print("🧪 Running Great Expectations checks...")

    con = duckdb.connect(str(DB_PATH), read_only=True)
    df = con.execute("SELECT * FROM silver_contracts").df()
    con.close()

    context = gx.get_context(mode="ephemeral")

    ds = context.data_sources.add_pandas(name="silver")
    da = ds.add_dataframe_asset(name="silver_contracts")
    batch_def = da.add_batch_definition_whole_dataframe("batch")
    batch = batch_def.get_batch(batch_parameters={"dataframe": df})

    suite = gx.ExpectationSuite(name="silver_suite")
    suite = context.suites.add(suite)

    suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="id"))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="id"))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="document_type"))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="document_date"))
    suite.add_expectation(gx.expectations.ExpectTableRowCountToBeBetween(min_value=100, max_value=10000))

    results = batch.validate(suite)

    print(f"\n📊 Results:")
    print(f"   ✅ Success: {results['statistics']['successful_expectations']}")
    print(f"   ❌ Failed:  {results['statistics']['unsuccessful_expectations']}")
    print(f"   📋 Total:   {results['statistics']['evaluated_expectations']}")

    if results['success']:
        print("\n🎉 All checks passed!")
    else:
        print("\n⚠️ Some checks failed!")

    return results

if __name__ == "__main__":
    run_checks()
