# Multi-Source Data Quality Scorecard

## Overview
This project builds a **comprehensive data quality scorecard** that evaluates datasets across multiple sources (**CSV** and **MySQL**) and generates a consolidated **Excel report** with **column-level metrics** and **visual quality indicators**.

The scorecard helps identify:
- Missing values  
- Duplicate records  
- Invalid data  
- Cross-source inconsistencies  
- Overall data health  

---

## Technologies Used
- Python
- Pandas
- SQLAlchemy
- MySQL
- Excel (XlsxWriter)

---

## Data Sources
- **CSV:** Netflix Movies and TV Shows dataset (Kaggle)
- **MySQL:** Same dataset loaded into a relational database

---

## Data Quality Metrics

### Completeness
Measures the proportion of non-null values.

Completeness = 1 - (Null Values / Total Values)


---

### Accuracy
Rule-based validation:
- Valid release year (1900–current year)
- Valid type (`Movie` / `TV Show`)
- Non-null rating
- Valid duration format
- Valid `date_added` format

Final accuracy is computed as the **average of all rule checks**.

---

### Consistency
Evaluated using:
- Primary key overlap between CSV and MySQL
- Schema consistency
- Row count consistency

Final consistency is the **average of these checks**.

---

## Output
An Excel data quality scorecard containing:
- Summary quality metrics
- Column-level profiling for each source
- Visual-ready quality indicators

---

## Features
- Connects to **CSV** (mandatory) and **MySQL** (optional)
- Profiles each source for:
  - Completeness
  - Accuracy
  - Consistency
  - Duplicate rows
  - Column-level statistics (null %, unique values, min/max, invalid values)
- Generates an Excel report with conditional formatting:
  - 🟢 Green → Good (>90%)
  - 🟡 Yellow → Medium (75–90%)
  - 🔴 Red → Poor (<75%)

---

## Folder Structure

multi_source_data_quality_scorecard/
│
├── data/
│ └── raw/
│ └── netflix_titles.csv
│
├── src/
│ ├── csv_profiling.py
│ ├── mysql_profiling.py
│ ├── quality_metrics.py
│ ├── consistency_check.py
│ ├── generate_scorecard.py
│ └──load_csv_to_mysql.py
│
├── output/
│ └── Data_Quality_Scorecard.xlsx
│
├── requirements.txt
└── README.md



---

## Installation & Setup

### 1. Clone the repository

git clone <repo_url>
cd multi_source_data_quality_scorecard

### 2. Install dependencies

pip install -r requirements.txt


**Dependencies:**
- pandas
- sqlalchemy
- mysql-connector-python
- python-dateutil
- xlsxwriter

---

### 3. Create MySQL database

- Place CSV file at: data/raw/netflix_titles.csv

- Create MySQL database `data_quality_db`
  
  CREATE DATABASE data_quality_db;

### 4. Set MySQL credentials using environment variables

⚠️ Credentials are NOT hardcoded for security and portability.

**Linux / macOS**:

export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_HOST=localhost
export MYSQL_DB=data_quality_db

**Windows (PowerShell)**:

setx MYSQL_USER "root"
setx MYSQL_PASSWORD "your_password"
setx MYSQL_HOST "localhost"
setx MYSQL_DB "data_quality_db"

### 5. Load CSV data into MySQL

python src/load_csv_to_mysql.py

This script:
- Reads the full CSV dataset
- Loads it into MySQL table netflix_titles
- Replaces the table if it already exists


## Running the Project

python src/generate_scorecard.py


### What happens:
- Always generates CSV metrics
- If MySQL is available:
  - Generates MySQL metrics
  - Performs cross-source consistency checks
- Outputs Excel report at: output/Data_Quality_Scorecard.xlsx


### Excel Sheets:
- **Summary** – overall scores with conditional formatting  
- **CSV_Column_Profile** – CSV column-level statistics  
- **MySQL_Column_Profile** – MySQL column-level statistics (if available)

---

## Graceful Handling of Data Sources
The MySQL data source is wrapped in a `try–except` block to ensure the pipeline continues execution even if the database is unavailable.

If MySQL is not accessible:
- CSV profiling still runs
- Database profiling is skipped
- A message is logged instead of failing the pipeline

This mirrors real-world resilient data engineering pipelines.

---

## Optional: API Integration

Example API loader:
```python
import requests
import pandas as pd

def load_api(url):
  response = requests.get(url)
  data = response.json()
  df = pd.DataFrame(data)

  summary = {
      "rows": len(df),
      "duplicate_rows": df.duplicated().sum(),
      "completeness": (1 - df.isnull().mean()).mean() * 100
  }

  return summary, df

API data can be profiled using the same logic as CSV/MySQL and added to the Excel scorecard.