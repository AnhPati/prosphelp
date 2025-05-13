import streamlit as st
import pandas as pd
from services.market_data import load_market_analysis, save_market_analysis
from components.charts import show_market_trend_chart

def show_market_analysis():
    st.header("Analyse des marchés")

    # Charger toutes les données
    df = load_market_analysis()

    # Formulaire pour ajouter une nouvelle analyse de marché
    with st.form("market_form"):
        market = st.text_input("Marché (ex: Développeur React)")
        date = st.date_input("Date")
        number = st.number_input("Nombre d'annonces", min_value=0, step=1)
        trend = st.text_input("Tendance (ex: en hausse, stable, en baisse)")
        submitted = st.form_submit_button("Ajouter")

        if submitted and market:
            market_data = {
                "Date": str(date),
                "Type": "Marché",
                "Marché": market,
                "Nombre d'annonces": number,
                "Tendance": trend
            }
            save_market_analysis(market_data)
            st.success("✅ Donnée ajoutée avec succès.")

    # Affichage du tableau : ne conserver que les colonnes utiles
    st.subheader("📊 Historique des marchés")
    if not df.empty:
        display_columns = ["Date", "Marché", "Nombre d'annonces", "Tendance"]
        st.dataframe(df[display_columns])
    else:
        st.info("Aucune donnée d'analyse de marché disponible.")

    # Affichage du graphique uniquement pour les données de type "Marché"
    st.subheader("📈 Tendances des marchés")
    show_market_trend_chart(df)
