import pandas as pd
from config.settings import MARKET_DATA_FILE

def load_market_data():
    if MARKET_DATA_FILE.exists() and MARKET_DATA_FILE.stat().st_size > 0:
        return pd.read_csv(MARKET_DATA_FILE)
    return pd.DataFrame(columns=["Date", "Marché", "Nombre d'annonces"])

def save_market_data(df):
    df.to_csv(MARKET_DATA_FILE, index=False)
