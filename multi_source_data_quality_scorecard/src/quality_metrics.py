import pandas as pd
from datetime import datetime

def accuracy(df):
    current_year = datetime.now().year
    checks = []

    # Rule 1: Release year range
    checks.append(df["release_year"].between(1900, current_year).mean())

    # Rule 2: Valid type
    checks.append(df["type"].isin(["Movie", "TV Show"]).mean())

    # Rule 3: Rating present
    checks.append(df["rating"].notnull().mean())

    # Rule 4: Duration format
    checks.append(df["duration"].str.contains("min|Season", na=False).mean())

    # Rule 5: date_added parsable
    checks.append(
        df["date_added"].apply(
            lambda x: True if pd.isna(x) else _is_valid_date(x)
        ).mean()
    )

    return sum(checks) / len(checks) * 100


def _is_valid_date(date_str):
    try:
        from dateutil.parser import parse
        parse(date_str)
        return True
    except:
        return False
