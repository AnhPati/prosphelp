import streamlit as st
import pandas as pd

def show_market_trend_chart(df):
    if df.empty:
        st.info("Aucune donnée à afficher.")
        return

    # S'assurer que la colonne Date est bien en datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Filtrer les données de type "Marché"
    df_market = df[df["Type"] == "Marché"]

    if df_market.empty:
        st.warning("Aucune donnée de type 'Marché' à afficher.")
        return

    # Pivot et affichage
    pivot = df_market.pivot(index="Date", columns="Marché", values="Nombre d'annonces").fillna(0)
    st.line_chart(pivot)
