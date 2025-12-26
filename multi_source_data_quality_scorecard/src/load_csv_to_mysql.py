import os
import pandas as pd
from sqlalchemy import create_engine

# -----------------------
# Read CSV
# -----------------------
csv_path = "data/raw/netflix_titles.csv"
df = pd.read_csv(csv_path)

# -----------------------
# MySQL credentials from env
# -----------------------
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_DB = os.getenv("MYSQL_DB", "data_quality_db")

if not MYSQL_USER or not MYSQL_PASSWORD:
    raise EnvironmentError(
        "MySQL credentials not found. "
        "Please set MYSQL_USER and MYSQL_PASSWORD environment variables."
    )

engine = create_engine(
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
)

# -----------------------
# Load into MySQL
# -----------------------
df.to_sql(
    name="netflix_titles",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data successfully loaded into MySQL")
