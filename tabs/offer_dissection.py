import streamlit as st
from services.offers.get_all_existing_markets import get_all_existing_markets
from services.offers.get_existing_markets_from_offers import get_existing_markets_from_offers
from services.offers.save_offers import save_offer_data
from services.offers.load_offers import load_offers
from components.forms.offer_form import offer_form
from utils.filters import select_market_filter, filter_by_market_selection
from constants.alerts import SUCCESS_OFFER_SAVED, INFO_NO_OFFERS_DATA
from constants.labels import HEADER_OFFER_DISSECTION, LABEL_DATA_SOURCE, SECTION_OFFERS, LABEL_MARKET_FILTER, DATA_SOURCE_OPTIONS
from constants.schema.views import OFFER_DISPLAY_COLUMNS
from constants.schema.columns import COL_TYPE
from config.settings import get_market_offers_file  # ✅ nouvelle méthode

def render_offer_dissection():
    st.header(HEADER_OFFER_DISSECTION)

    user_id = st.session_state.user["id"]
    markets = get_all_existing_markets(user_id)

    # ➕ Bloc collapsible pour l’ajout d’une offre/contact
    with st.expander("Ajouter une offre ou un contact", expanded=True, icon=":material/forms_add_on:"):
        source = st.radio(LABEL_DATA_SOURCE, DATA_SOURCE_OPTIONS, horizontal=True)
        offer_data = offer_form(markets, source=source)
        if offer_data:
            save_offer_data(offer_data, user_id)
            st.success(SUCCESS_OFFER_SAVED)

    # 📄 Bloc collapsible pour l’affichage des offres enregistrées
    with st.expander("Offres enregistrées", expanded=True, icon=":material/business_center:"):
        market_file = get_market_offers_file(user_id)
        if market_file.exists():
            offers_df = load_offers(user_id)

            if offers_df.empty:
                st.info(INFO_NO_OFFERS_DATA)
                return

            markets_from_offers = get_existing_markets_from_offers(user_id)
            selected_market = select_market_filter(markets_from_offers, LABEL_MARKET_FILTER, key="offer_dissection_market_select")
            filtered_df = filter_by_market_selection(offers_df, selected_market)
            st.dataframe(filtered_df[OFFER_DISPLAY_COLUMNS])
        else:
            st.info(INFO_NO_OFFERS_DATA)