import streamlit as st

def show_market_trend_chart(df):
    if df.empty:
        st.info("Aucune donnée à afficher.")
        return

    pivot = df.pivot(index="Date", columns="Marché", values="Nombre d'annonces").fillna(0)
    st.line_chart(pivot)