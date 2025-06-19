import streamlit as st
from config.settings import MARKET_OFFERS_FILE
from services.offers.get_existing_markets_from_offers import get_existing_markets_from_offers
from services.offers.save_offers import save_offer_data
from services.offers.load_offers import load_offers
from components.forms.offer_form import offer_form
from utils.filters import select_market_filter, filter_by_market_selection
from constants.alerts import SUCCESS_OFFER_SAVED, INFO_NO_OFFERS_DATA
from constants.labels import HEADER_OFFER_DISSECTION, LABEL_DATA_SOURCE, SECTION_OFFERS, LABEL_MARKET_FILTER, DATA_SOURCE_OPTIONS
from constants.schema.views import OFFER_DISPLAY_COLUMNS
from constants.schema.columns import COL_TYPE

def render_offer_dissection():
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

        if offers_df.empty:
            st.info(INFO_NO_OFFERS_DATA)
            return

        selected_market = select_market_filter(markets, LABEL_MARKET_FILTER)
        filtered_df = filter_by_market_selection(offers_df, selected_market)
        st.dataframe(filtered_df[OFFER_DISPLAY_COLUMNS])

    else:
        st.info(INFO_NO_OFFERS_DATA)