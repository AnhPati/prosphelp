import streamlit as st
import pandas as pd
from constants.labels import ALL_MARKETS_OPTION

def filter_dataframe_by_market(df: pd.DataFrame, markets: list[str], label: str = "Filtrer par marché") -> pd.DataFrame:
    if markets is None or len(markets) == 0:
        st.warning("⚠️ Aucun marché disponible pour le filtrage.")
        return ALL_MARKETS_OPTION

    selected_market = st.selectbox(f"{label}", markets, index=0)

    return selected_market
