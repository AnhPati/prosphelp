import pandas as pd
from config.settings import MARKET_OFFERS_FILE
from constants.alerts import ERROR_SAVING_OFFERS
from constants.schema.constants import EXPECTED_COLUMNS

def save_offer_data(offer_data: dict | pd.DataFrame) -> bool:
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