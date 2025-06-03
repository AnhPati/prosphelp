import streamlit as st
import pandas as pd

def filter_dataframe_by_market(df: pd.DataFrame, markets: list[str], label: str = "Filtrer par marché") -> pd.DataFrame:
    if markets is None or len(markets) == 0:
        st.warning("⚠️ Aucun marché disponible pour le filtrage.")
        return df

    selected_market = st.selectbox(f"{label}", markets, index=0)

    return selected_market
