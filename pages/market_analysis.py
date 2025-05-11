import streamlit as st
import pandas as pd
from services.market_data import load_market_analysis, save_market_analysis
from components.charts import show_market_trend_chart

def show_market_analysis():
    st.header("Analyse des marchés")

    # Charger les données du fichier CSV (incluant potentiellement "Marché" et "Offre")
    df = load_market_analysis()

    # Filtrer uniquement les données de type "Marché"
    df_market = df[df["Type"] == "Marché"].copy()

    # Formulaire pour ajouter une nouvelle analyse de marché
    with st.form("market_form"):
        market = st.text_input("Marché (ex: Développeur React)")
        date = st.date_input("Date")
        number = st.number_input("Nombre d'annonces", min_value=0, step=1)
        trend = st.text_input("Tendance (ex: en hausse, stable, en baisse)")
        submitted = st.form_submit_button("Ajouter")

        if submitted and market:
            # Ajouter une nouvelle entrée au DataFrame
            market_data = {
                "Date": str(date),
                "Type": "Marché",
                "Marché": market,
                "Nombre d'annonces": number,
                "Tendance": trend
            }
            save_market_analysis(market_data)
            st.success("Donnée ajoutée avec succès.")

    # Afficher l'historique uniquement des données de marché
    st.subheader("Historique")
    st.dataframe(df_market)

    # Afficher les tendances des marchés
    st.subheader("Tendances")
    show_market_trend_chart(df)
