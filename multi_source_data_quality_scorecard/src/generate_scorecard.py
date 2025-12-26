"""
Main entry point for generating the multi-source data quality scorecard.
Safely handles unavailable data sources.
"""

import pandas as pd
from csv_profiling import profile_csv
from mysql_profiling import load_mysql
from quality_metrics import accuracy
from consistency_check import consistency

# -----------------------
# Load CSV profiling
# -----------------------
csv_summary, csv_df, csv_col_profile = profile_csv(
    "data/raw/netflix_titles.csv"
)

# -----------------------
# Load MySQL profiling
# -----------------------
try:
    sql_summary, sql_df, sql_col_profile = load_mysql()
    mysql_available = True
except Exception:
    print("MySQL not available. Skipping MySQL profiling.")
    sql_summary, sql_df, sql_col_profile = None, None, None
    mysql_available = False

# -----------------------
# Build scorecard data
# -----------------------
sources = ["CSV"]
completeness = [round(csv_summary["completeness"], 2)]
accuracy_scores = [round(accuracy(csv_df), 2)]
consistency_scores = [100.0]  # CSV baseline

if mysql_available:
    sources.append("MySQL")
    completeness.append(round(sql_summary["completeness"], 2))
    accuracy_scores.append(round(accuracy(sql_df), 2))
    consistency_scores.append(round(consistency(csv_df, sql_df), 2))

scorecard = pd.DataFrame({
    "Source": sources,
    "Completeness %": completeness,
    "Accuracy %": accuracy_scores,
    "Consistency %": consistency_scores
})

scorecard["Overall Score %"] = scorecard.iloc[:, 1:].mean(axis=1).round(2)

# -----------------------
# Write to Excel + conditional formatting
# -----------------------
with pd.ExcelWriter(
    "output/Data_Quality_Scorecard.xlsx",
    engine="xlsxwriter"
) as writer:

    scorecard.to_excel(writer, sheet_name="Summary", index=False)
    csv_col_profile.to_excel(writer, sheet_name="CSV_Column_Profile", index=False)

    if mysql_available:
        sql_col_profile.to_excel(writer, sheet_name="MySQL_Column_Profile", index=False)

    workbook = writer.book
    worksheet = writer.sheets["Summary"]

    # Formats
    green = workbook.add_format({"bg_color": "#C6EFCE"})
    yellow = workbook.add_format({"bg_color": "#FFEB9C"})
    red = workbook.add_format({"bg_color": "#FFC7CE"})

    last_row = len(scorecard) + 1  # header = row 1

    # Apply conditional formatting
    for col in ["B", "C", "D", "E"]:
        worksheet.conditional_format(
            f"{col}2:{col}{last_row}",
            {"type": "cell", "criteria": ">=", "value": 90, "format": green}
        )
        worksheet.conditional_format(
            f"{col}2:{col}{last_row}",
            {
                "type": "cell",
                "criteria": "between",
                "minimum": 75,
                "maximum": 89.99,
                "format": yellow,
            }
        )
        worksheet.conditional_format(
            f"{col}2:{col}{last_row}",
            {"type": "cell", "criteria": "<", "value": 75, "format": red}
        )

print("Data Quality Scorecard generated successfully!")
