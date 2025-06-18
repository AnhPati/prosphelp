import streamlit as st
from constants.labels import  FIELD_MARKET_EXISTING, FIELD_MARKET_NEW, FIELD_DATE, FIELD_NUMBER_OF_OFFERS, FIELD_NOTES, BTN_SAVE_MARKET, CHECKBOX_USE_EXISTING_MARKET
def show_market_form(existing_markets: list[str]):
    use_existing = st.checkbox(CHECKBOX_USE_EXISTING_MARKET, value=True)

    with st.form("market_form"):
        if use_existing:
            market = st.selectbox(FIELD_MARKET_EXISTING, options=[""] + existing_markets, key="selected_market")
            new_market = None
        else:
            market = None
            new_market = st.text_input(FIELD_MARKET_NEW, key="new_market")

        final_market = new_market.strip() if new_market else (market if market else "")
        first_col, second_col, third_col = st.columns(3)

        with first_col:
            date = st.date_input(FIELD_DATE, key="selected_date", format="DD/MM/YYYY")
        with second_col:
            number = st.number_input(FIELD_NUMBER_OF_OFFERS, min_value=0, step=1, key="selected_number")
        with third_col:
            notes = st.text_input(FIELD_NOTES, key="notes")

        submitted = st.form_submit_button(BTN_SAVE_MARKET)

        return submitted, final_market, date, number, notes