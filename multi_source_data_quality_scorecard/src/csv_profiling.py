import pandas as pd
from datetime import datetime
from dateutil.parser import parse

def is_valid_date(x):
    try:
        parse(str(x))
        return True
    except:
        return False


def profile_csv(path):
    df = pd.read_csv(path, low_memory=False)

    summary = {
        "rows": len(df),
        "duplicate_rows": df.duplicated().sum(),
        "completeness": (1 - df.isnull().mean()).mean() * 100
    }

    column_profile = []

    for col in df.columns:
        null_pct = df[col].isnull().mean() * 100
        unique_count = df[col].nunique(dropna=True)
        invalid_count = 0
        min_val = None
        max_val = None

        # Numeric checks
        if col in ["release_year"]:
            numeric_col = pd.to_numeric(df[col], errors="coerce")
            min_val = numeric_col.min()
            max_val = numeric_col.max()
            invalid_count = ((numeric_col < 1900) | (numeric_col > datetime.now().year)).sum()

        # Date format checks
        elif col == "date_added":
            invalid_count = df[col].dropna().apply(lambda x: not is_valid_date(x)).sum()

        # Categorical checks
        elif col == "type":
            invalid_count = (~df[col].isin(["Movie", "TV Show"])).sum()

        column_profile.append({
            "column": col,
            "null_pct": round(null_pct, 2),
            "unique_values": unique_count,
            "min": min_val,
            "max": max_val,
            "invalid_values": invalid_count
        })

    column_profile_df = pd.DataFrame(column_profile)

    return summary, df, column_profile_df
