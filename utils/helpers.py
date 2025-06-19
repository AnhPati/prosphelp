import pandas as pd
from pathlib import Path
from typing import List

def fallback_read_csv(file_path: Path, expected_columns: List[str]) -> pd.DataFrame:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip().split('|') for line in f.readlines()]

        cleaned_lines = []
        for line in lines:
            if len(line) == len(expected_columns):
                cleaned_lines.append(line)
            elif line:
                # Truncate or pad to expected length
                adjusted = line[:len(expected_columns)] + [''] * (len(expected_columns) - len(line))
                cleaned_lines.append(adjusted)

        if not cleaned_lines:
            return pd.DataFrame(columns=expected_columns)

        header = cleaned_lines[0]
        if len(header) != len(expected_columns):
            header = expected_columns

        return pd.DataFrame(cleaned_lines[1:], columns=header)

    except Exception as e:
        print(f"Erreur dans le fallback de lecture : {str(e)}")
        return pd.DataFrame(columns=expected_columns)
