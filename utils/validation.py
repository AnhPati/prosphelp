import pandas as pd

def is_entry_unique(df: pd.DataFrame, conditions: dict[str, str | int | float]) -> bool:
    query = pd.Series([True] * len(df))
    for column, value in conditions.items():
        query &= df[column] == value
    return df[query].empty
