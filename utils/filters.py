import pandas as pd
import streamlit as st
from constants.labels import ALL_MARKETS_OPTION

def select_market_filter(markets: list[str], label: str = "Filtrer par marché") -> str:
    return st.selectbox(label, [ALL_MARKETS_OPTION] + sorted(markets)) if markets else ALL_MARKETS_OPTION

def filter_by_market_selection(df: pd.DataFrame, selected_market: str, all_option: str = ALL_MARKETS_OPTION) -> pd.DataFrame:
    if selected_market and selected_market != all_option:
        return df[df["Marché"] == selected_market]
    return df