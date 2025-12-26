def consistency(csv_df, sql_df):
    # Primary key consistency
    csv_ids = set(csv_df["show_id"])
    sql_ids = set(sql_df["show_id"])
    id_overlap = len(csv_ids & sql_ids) / max(len(csv_ids), len(sql_ids))

    # Schema consistency
    schema_match = int(list(csv_df.columns) == list(sql_df.columns))

    # Row count consistency
    row_diff = abs(len(csv_df) - len(sql_df)) / len(csv_df)
    row_consistency = 1 - row_diff

    return ((id_overlap + schema_match + row_consistency) / 3) * 100
