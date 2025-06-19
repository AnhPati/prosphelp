import pandas as pd
from config.settings import MARKET_OFFERS_FILE
from utils.helpers import fallback_read_csv
from constants.alerts import ERROR_LOADING_OFFERS
from constants.schema.constants import EXPECTED_COLUMNS, COLUMNS_SEP
from constants.schema.columns import COL_TYPE

def load_offers() -> pd.DataFrame:
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