# tabs/offer_dissection.py

import streamlit as st
from config.settings import MARKET_OFFERS_FILE
from services.offer_service import load_offers, save_offer_data, get_existing_markets_from_offers
from components.forms import show_offer_form

def show_offer_dissection():
    st.header("Dissection des offres")

    markets = get_existing_markets_from_offers()
    if not markets:
        st.warning("⚠️ Aucun marché détecté dans le fichier `offers.csv`. Veuillez d'abord en créer via l'onglet Analyse des marchés.")
        return

    source = st.radio("Source de données :", ["offre", "contact"], horizontal=True)
    offer_data = show_offer_form(markets, source=source)
    if offer_data:
        save_offer_data(offer_data)
        st.success("✅ Offre enregistrée avec succès !")

    st.subheader("📄 Offres enregistrées")
    if MARKET_OFFERS_FILE.exists():
        offers_df = load_offers()
        display_columns = [
            "Date", "Marché", "Intitulé", "TJM", "Séniorité",
            "Technos principales", "Technos secondaires",
            "Compétences principales", "Compétences secondaires",
            "Secteur", "Localisation", "Rythme",
            "Entreprise", "Contact", "Lien"
        ]

        if "Type" in offers_df.columns:
            offers_df = offers_df[offers_df["Type"] == "Offre"]

        selected_market = st.selectbox("🔍 Filtrer les offres par marché", ["Tous"] + markets)
        if selected_market != "Tous":
            offers_df = offers_df[offers_df["Marché"] == selected_market]

        st.dataframe(offers_df[display_columns])
    else:
        st.info("Aucune offre enregistrée pour le moment.")
