import pandas as pd

from clean import normalize_columns


def test_normalize_columns_handles_spaces_and_symbols():
    data = pd.DataFrame(
        {
            "Customer Name": ["Ali"],
            "Total-Sales": [100],
            "Age (Years)": [25],
        }
    )

    result = normalize_columns(data)

    assert list(result.columns) == [
        "customer_name",
        "total_sales",
        "age_years",
    ]