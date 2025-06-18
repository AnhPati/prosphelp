import pandas as pd
from config.settings import MARKET_OFFERS_FILE
from utils.helpers import fallback_read_csv
from constants.alerts import ERROR_LOADING_OFFERS, ERROR_SAVING_OFFERS, ERROR_LOADING_MARKETS_FROM_OFFERS
from constants.schema.constants import EXPECTED_COLUMNS, COLUMNS_SEP
from constants.schema.columns import COL_TYPE, COL_MARKET

def load_offers():
    if not MARKET_OFFERS_FILE.exists():
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    try:
        df = pd.read_csv(
            MARKET_OFFERS_FILE,
            sep=COLUMNS_SEP,
            quotechar=None,
            encoding='utf-8',
            header=0,
            engine='python'
        )
    except pd.errors.ParserError:
        df = fallback_read_csv(MARKET_OFFERS_FILE, EXPECTED_COLUMNS)

    except Exception as e:
        print(ERROR_LOADING_OFFERS.format(error=str(e)))
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    return df[df[COL_TYPE] == "Offre"].copy()


def save_offer_data(offer_data):
    df = pd.DataFrame([offer_data]) if isinstance(offer_data, dict) else offer_data.copy()

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    df = df[EXPECTED_COLUMNS]

    try:
        df.to_csv(
            MARKET_OFFERS_FILE,
            sep="|",
            mode='a' if MARKET_OFFERS_FILE.exists() else 'w',
            header=not MARKET_OFFERS_FILE.exists(),
            index=False,
            encoding='utf-8',
            quoting=0
        )
        return True
    except Exception as e:
        print(ERROR_SAVING_OFFERS.format(error=str(e)))
        return False


def get_existing_markets_from_offers():
    try:
        df = load_offers()
        return sorted(df[COL_MARKET].dropna().astype(str).unique()) if not df.empty else []
    except Exception as e:
        print(ERROR_LOADING_MARKETS_FROM_OFFERS.format(error=str(e)))
        return []