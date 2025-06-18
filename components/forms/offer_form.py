import streamlit as st
import pandas as pd
from constants.alerts import WARNING_TITLE_LINK_REQUIRED, WARNING_CONTACT_NAME_REQUIRED
from constants.labels import SUBHEADER_NEW_ENTRY, FIELD_MARKET, FIELD_TITLE, FIELD_JOB_TITLE, FIELD_TJM, FIELD_SENIORITY, FIELD_TECH_MAIN, FIELD_TECH_SECONDARY, FIELD_SKILLS_MAIN, FIELD_SKILLS_SECONDARY, FIELD_SECTOR, FIELD_LOCATION, FIELD_RHYTHM, FIELD_COMPANY, FIELD_CONTACT, FIELD_LINK, FIELD_SOPHISTICATION, FIELD_RELIABILITY, BTN_SAVE_OFFER, RHYTHM_OPTIONS
from constants.schema.schema import COL_TYPE, COL_TITLE, COL_JOB_TITLE, COL_TJM, COL_SENIORITY, COL_MARKET, COL_DATE, COL_TECHS_MAIN, COL_TECHS_SECONDARY, COL_SKILLS_MAIN, COL_SKILLS_SECONDARY, COL_SECTOR, COL_LOCATION, COL_RHYTHM, COL_COMPANY, COL_CONTACT, COL_LINK, COL_SOPHISTICATION, COL_RELIABILITY
def show_offer_form(markets: list[str], source: str = "offre"):
    st.subheader(SUBHEADER_NEW_ENTRY)

    with st.form("data_entry_form"):
        title = job_title = offer_link = ""
        tjm = seniority = main_techs = secondary_techs = main_skills = secondary_skills = ""
        sector = location = work_mode = company = contact_name = ""
        sophistication = reliability = None

        if source == "offre":
            first_col, second_col = st.columns(2)
            with first_col:
                market = st.selectbox(FIELD_MARKET, markets)
            with second_col:
                title = st.text_input(FIELD_TITLE)
        else:
            market = st.selectbox(FIELD_MARKET, markets)

        if source == "offre":
            first_col, second_col, third_col = st.columns([3, 1, 1])
            with first_col:
                job_title = st.text_input(FIELD_JOB_TITLE)
            with second_col:
                tjm = st.text_input(FIELD_TJM)
            with third_col:
                seniority = st.text_input(FIELD_SENIORITY)
        else:
            first_col, second_col = st.columns(2)
            with first_col:
                tjm = st.text_input(FIELD_TJM)
            with second_col:
                seniority = st.text_input(FIELD_SENIORITY)

        first_col, second_col = st.columns(2)
        with first_col:
            main_techs = st.text_input(FIELD_TECH_MAIN)
        with second_col:
            secondary_techs = st.text_input(FIELD_TECH_SECONDARY)

        first_col, second_col = st.columns(2)
        with first_col:
            main_skills = st.text_input(FIELD_SKILLS_MAIN)
        with second_col:
            secondary_skills = st.text_input(FIELD_SKILLS_SECONDARY)

        first_col, second_col, third_col = st.columns(3)
        with first_col:
            sector = st.text_input(FIELD_SECTOR)
        with second_col:
            location = st.text_input(FIELD_LOCATION)
        with third_col:
            work_mode = st.selectbox(FIELD_RHYTHM, RHYTHM_OPTIONS)

        if source == "offre":
            first_col, second_col, third_col = st.columns(3)
            with first_col:
                company = st.text_input(FIELD_COMPANY)
            with second_col:
                contact_name = st.text_input(FIELD_CONTACT)
            with third_col:
                offer_link = st.text_input(FIELD_LINK)
        else:
            first_col, second_col = st.columns(2)
            with first_col:
                company = st.text_input(FIELD_COMPANY)
            with second_col:
                contact_name = st.text_input(FIELD_CONTACT)

        if source == "contact":
            first_col, second_col = st.columns(2)
            with first_col:
                sophistication = st.slider(FIELD_SOPHISTICATION, 1, 5, 3)
            with second_col:
                reliability = st.slider(FIELD_RELIABILITY, 1, 5, 3)

        submitted = st.form_submit_button(BTN_SAVE_OFFER)

        if submitted:
            if source == "offre" and not (title and offer_link):
                st.error(WARNING_TITLE_LINK_REQUIRED)
                return None
            if source == "contact" and not contact_name:
                st.error(WARNING_CONTACT_NAME_REQUIRED)
                return None

            return {
                COL_DATE: pd.to_datetime("today").strftime('%Y-%m-%d'),
                COL_TYPE: "Contact" if source == "contact" else "Offre",
                COL_MARKET: market,
                COL_TITLE: title,
                COL_JOB_TITLE: job_title,
                COL_TJM: tjm,
                COL_SENIORITY: seniority,
                COL_TECHS_MAIN: main_techs,
                COL_TECHS_SECONDARY: secondary_techs,
                COL_SKILLS_MAIN: main_skills,
                COL_SKILLS_SECONDARY: secondary_skills,
                COL_SECTOR: sector,
                COL_LOCATION: location,
                COL_RHYTHM: work_mode,
                COL_COMPANY: company,
                COL_CONTACT: contact_name,
                COL_LINK: offer_link,
                COL_SOPHISTICATION: sophistication,
                COL_RELIABILITY: reliability
            }

    return None