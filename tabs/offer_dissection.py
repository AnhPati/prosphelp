# tabs/offer_dissection.py

import streamlit as st
from config.settings import MARKET_OFFERS_FILE
from services.offer_service import load_offers, save_offer_data, get_existing_markets_from_offers
from components.forms import show_offer_form
from constants.alerts import OFFER_SAVED_SUCCESS, NO_OFFERS_DATA
from constants.labels import HEADER_OFFER_DISSECTION, LABEL_DATA_SOURCE, SECTION_OFFERS, LABEL_MARKET_FILTER, ALL_MARKETS_OPTION, DATA_SOURCE_OPTIONS

def show_offer_dissection():
    st.header(HEADER_OFFER_DISSECTION)

    markets = get_existing_markets_from_offers()

    source = st.radio(LABEL_DATA_SOURCE, DATA_SOURCE_OPTIONS, horizontal=True)
    offer_data = show_offer_form(markets, source=source)
    if offer_data:
        save_offer_data(offer_data)
        st.success(OFFER_SAVED_SUCCESS)

    st.subheader(SECTION_OFFERS)
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

        selected_market = st.selectbox(LABEL_MARKET_FILTER, [ALL_MARKETS_OPTION] + markets)
        if selected_market != ALL_MARKETS_OPTION:
            offers_df = offers_df[offers_df["Marché"] == selected_market]

        st.dataframe(offers_df[display_columns])
    else:
        st.info(NO_OFFERS_DATA)
