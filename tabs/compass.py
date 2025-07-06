import streamlit as st
import pandas as pd
from services.offers.load_offers import load_offers
from services.market_analysis.load_markets_analysis import load_markets_analysis
from services.cache.geocoding_cache import save_cache
from components.maps.geocoding_feeback import geocode_with_feedback 
from components.charts.trend_chart import trend_chart
from components.charts.bar_chart import bar_chart
from components.charts.pie_chart import pie_chart
from components.numeric_range_slider import numeric_range_slider
from components.maps.offers_map import offers_map
from utils.filters import select_market_filter
from constants.alerts import (
    WARNING_MISSING_COLUMN, WARNING_NO_MARKET_ANALYSIS
)
from constants.labels import (
    HEADER_COMPASS, SECTION_MARKET_TRENDS, LABEL_TJM, LABEL_SENIORITY,
    LABEL_RHYTHM, LABEL_SECTOR, SECTION_POSITIONING, SECTION_MAP_OFFERS, SECTION_SKILLS, SECTION_TECHS,
    LABEL_MAIN_SKILLS, LABEL_SECONDARY_SKILLS, LABEL_MAIN_TECHS,
    LABEL_SECONDARY_TECHS, LABEL_SELECT_MARKET, TITLE_MARKET_TREND,
    X_AXIS_DATE, Y_AXIS_ADS, LEGEND_MARKET
)
from constants.schema.views import COMPASS_DISPLAY_COLUMNS
from constants.schema.columns import (
    COL_DATE, COL_MARKET, COL_SKILLS_MAIN, COL_SKILLS_SECONDARY,
    COL_TECHS_MAIN, COL_TECHS_SECONDARY, COL_TJM, COL_SENIORITY,
    COL_RHYTHM, COL_SECTOR, COL_NUMBER_OF_OFFERS, COL_LOCATION
)

def render_compass():
    CONTEXT_ID = "compass"
    st.header(HEADER_COMPASS)

    user_id = st.session_state.user["id"]

    df_market_analysis = load_markets_analysis(user_id)
    df_offers_original = load_offers(user_id)
    df_offers = geocode_with_feedback(df_offers_original, COL_LOCATION, st.session_state.geocoded_locations_cache)
    save_cache(st.session_state.geocoded_locations_cache)

    if df_offers.empty or any(col not in df_offers.columns for col in COMPASS_DISPLAY_COLUMNS):
        st.warning(WARNING_MISSING_COLUMN)
        return
    if COL_MARKET not in df_market_analysis.columns:
        st.warning(WARNING_NO_MARKET_ANALYSIS)
        return

    markets = sorted(set(df_offers[COL_MARKET].dropna()) | set(df_market_analysis[COL_MARKET].dropna()))
    selected_market = select_market_filter(markets, label=LABEL_SELECT_MARKET, key="compass_market_select")

    # 🔹 Tendance des marchés
    with st.expander(SECTION_MARKET_TRENDS, expanded=True, icon=":material/insights:"):
        trend_chart(
            df=df_market_analysis,
            index_col=COL_DATE,
            category_col=COL_MARKET,
            value_col=COL_NUMBER_OF_OFFERS,
            highlight=selected_market,
            title=TITLE_MARKET_TREND,
            x_axis_label=X_AXIS_DATE,
            y_axis_label=Y_AXIS_ADS,
            legend_title=LEGEND_MARKET,
            context_id=CONTEXT_ID
        )

    skills_df = df_offers[df_offers[COL_MARKET] == selected_market]

    # 🔹 Positionnement
    with st.expander(SECTION_POSITIONING, expanded=True, icon=":material/my_location:"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            numeric_range_slider(skills_df, COL_TJM, LABEL_TJM, unit="€")
        with col2:
            numeric_range_slider(skills_df, COL_SENIORITY, LABEL_SENIORITY, unit="ans")
        with col3:
            st.subheader(LABEL_RHYTHM)
            pie_chart(skills_df[COL_RHYTHM].dropna().astype(str).str.strip(), title=LABEL_RHYTHM, context_id=CONTEXT_ID)
        with col4:
            st.subheader(LABEL_SECTOR)
            pie_chart(skills_df[COL_SECTOR].dropna().astype(str).str.strip(), title=LABEL_SECTOR, context_id=CONTEXT_ID)

    # 🔹 Localisation
    with st.expander(SECTION_MAP_OFFERS, expanded=True, icon=":material/map:"):
        offers_map(skills_df, selected_market)

    # 🔹 Compétences
    with st.expander(SECTION_SKILLS, expanded=True, icon=":material/psychology:"):
        st.markdown(LABEL_MAIN_SKILLS)
        bar_chart(
            skills_df[COL_SKILLS_MAIN].dropna().astype(str).str.split(",").explode().str.strip(),
            title=LABEL_MAIN_SKILLS,
            context_id=CONTEXT_ID
        )
        st.markdown(LABEL_SECONDARY_SKILLS)
        bar_chart(
            skills_df[COL_SKILLS_SECONDARY].dropna().astype(str).str.split(",").explode().str.strip(),
            title=LABEL_SECONDARY_SKILLS,
            context_id=CONTEXT_ID
        )

    # 🔹 Technologies
    with st.expander(SECTION_TECHS, expanded=True, icon=":material/settings_input_component:"):
        st.markdown(LABEL_MAIN_TECHS)
        bar_chart(
            skills_df[COL_TECHS_MAIN].dropna().astype(str).str.split(",").explode().str.strip(),
            title=LABEL_MAIN_TECHS,
            context_id=CONTEXT_ID
        )
        st.markdown(LABEL_SECONDARY_TECHS)
        bar_chart(
            skills_df[COL_TECHS_SECONDARY].dropna().astype(str).str.split(",").explode().str.strip(),
            title=LABEL_SECONDARY_TECHS,
            context_id=CONTEXT_ID
        )