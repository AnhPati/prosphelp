import pandas as pd
from constants.schema.columns import COL_MARKET
from config.settings import get_market_offers_file

def get_all_existing_markets(user_id: str) -> list[str]:
    filepath = get_market_offers_file(user_id)
    if not filepath.exists():
        return []

    try:
        df = pd.read_csv(filepath, sep="|")
        return sorted(df[COL_MARKET].dropna().unique())
    except Exception:
        return []