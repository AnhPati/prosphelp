import pandas as pd

def fallback_read_csv(MARKET_OFFERS_FILE, EXPECTED_COLUMNS):
    try:
        with open(MARKET_OFFERS_FILE, 'r', encoding='utf-8') as f:
            lines = [line.strip().split('|') for line in f.readlines()]

        cleaned_lines = []
        for line in lines:
            if len(line) == len(EXPECTED_COLUMNS):
                cleaned_lines.append(line)
            elif len(line) > 0:
                adjusted = line[:len(EXPECTED_COLUMNS)] + [''] * (len(EXPECTED_COLUMNS) - len(line))
                cleaned_lines.append(adjusted)

        return pd.DataFrame(cleaned_lines[1:], columns=cleaned_lines[0] if cleaned_lines else EXPECTED_COLUMNS)

    except Exception as e:
        print(f"Erreur dans le fallback de lecture : {str(e)}")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)