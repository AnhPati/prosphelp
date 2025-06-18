# tabs/offer_dissection.py

import streamlit as st
from config.settings import MARKET_OFFERS_FILE
from services.offer_service import load_offers, save_offer_data, get_existing_markets_from_offers
from components.forms.offer_form import offer_form
from constants.alerts import SUCCESS_OFFER_SAVED, INFO_NO_OFFERS_DATA
from constants.labels import HEADER_OFFER_DISSECTION, LABEL_DATA_SOURCE, SECTION_OFFERS, LABEL_MARKET_FILTER, ALL_MARKETS_OPTION, DATA_SOURCE_OPTIONS
from constants.schema.views import OFFER_DISPLAY_COLUMNS
from constants.schema.columns import COL_TYPE, COL_MARKET

def show_offer_dissection():
    st.header(HEADER_OFFER_DISSECTION)

    markets = get_existing_markets_from_offers()

    source = st.radio(LABEL_DATA_SOURCE, DATA_SOURCE_OPTIONS, horizontal=True)
    offer_data = offer_form(markets, source=source)
    if offer_data:
        save_offer_data(offer_data)
        st.success(SUCCESS_OFFER_SAVED)

    st.subheader(SECTION_OFFERS)
    if MARKET_OFFERS_FILE.exists():
        offers_df = load_offers()
        display_columns = OFFER_DISPLAY_COLUMNS

        if COL_TYPE in offers_df.columns:
            offers_df = offers_df[offers_df[COL_TYPE] == "Offre"]

        selected_market = st.selectbox(LABEL_MARKET_FILTER, [ALL_MARKETS_OPTION] + markets)
        if selected_market != ALL_MARKETS_OPTION:
            offers_df = offers_df[offers_df[COL_MARKET] == selected_market]

        st.dataframe(offers_df[display_columns])
    else:
        st.info(INFO_NO_OFFERS_DATA)
