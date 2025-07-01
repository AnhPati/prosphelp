import streamlit as st
import pandas as pd
from constants.alerts import WARNING_TITLE_LINK_REQUIRED, WARNING_CONTACT_NAME_REQUIRED
from constants.labels import SUBHEADER_NEW_ENTRY, BTN_SAVE_OFFER
from constants.schema.columns import COL_TYPE, COL_TITLE, COL_LINK, COL_CONTACT, COL_DATE, COL_MARKET
from components.forms.config.offer_inputs import BASE_FORM_INPUTS, OFFER_EXTRA_INPUTS, CONTACT_EXTRA_INPUTS

def offer_form(markets: list[str], source: str = "Offre"):
    st.subheader(SUBHEADER_NEW_ENTRY)

    if source.lower() == "offre":
        inputs = OFFER_EXTRA_INPUTS + BASE_FORM_INPUTS
    else:
        inputs = BASE_FORM_INPUTS + CONTACT_EXTRA_INPUTS

    form_data = {}
    with st.form("offer_form", clear_on_submit=True):
        market_field = next(field for field in BASE_FORM_INPUTS if field["key"] == COL_MARKET)
        form_data[COL_MARKET] = st.selectbox(market_field["label"], markets)
        
        for input in inputs:
            key = input["key"]
            if key == COL_MARKET:
                continue

            label = input["label"]
            ftype = input.get("type", "text")

            if ftype == "text":
                form_data[key] = st.text_input(label)
            elif ftype == "select":
                form_data[key] = st.selectbox(label, input.get("options", []))
            elif ftype == "slider":
                form_data[key] = st.slider(label, input.get("min", 1), input.get("max", 5), input.get("default", 3))

        submitted = st.form_submit_button(BTN_SAVE_OFFER)

    if submitted:
        if source == "offre" and (not form_data.get(COL_TITLE) or not form_data.get(COL_LINK)):
            st.error(WARNING_TITLE_LINK_REQUIRED)
            return None
        if source == "contact" and not form_data.get(COL_CONTACT):
            st.error(WARNING_CONTACT_NAME_REQUIRED)
            return None

        return {
            **form_data,
            COL_DATE: pd.to_datetime("today").strftime('%Y-%m-%d'),
            COL_TYPE: "Contact" if source == "contact" else "Offre",
        }

    return None