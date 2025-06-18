import streamlit as st
import pandas as pd
from services.offer_service import load_offers
from services.market_data import load_market_analysis
from services.geocoding_service import geocode_dataframe_locations_in_memory
from components.charts.trend_chart import trend_chart
from components.charts.bar_chart import bar_chart
from components.charts.pie_chart import pie_chart
from components.interactive_numeric_display import display_numeric_range_selector
from components.interactive_map import display_offers_map
from utils.filters import filter_dataframe_by_market
from constants.alerts import WARNING_MISSING_COLUMN, WARNING_NO_MARKET_ANALYSIS, INFO_NO_RYTHM_DATA, INFO_NO_SECTOR_DATA, WARNING_NO_MAIN_SKILLS, WARNING_NO_SECONDARY_SKILLS, WARNING_NO_MAIN_TECH, WARNING_NO_SECONDARY_TECH
from constants.labels import HEADER_COMPASS, SECTION_MARKET_TRENDS, LABEL_TJM, LABEL_SENIORITY, LABEL_RHYTHM, LABEL_SECTOR, SECTION_SKILLS, SECTION_TECHS, LABEL_MAIN_SKILLS, LABEL_SECONDARY_SKILLS, LABEL_MAIN_TECHS, LABEL_SECONDARY_TECHS, LABEL_SELECT_MARKET, TITLE_MARKET_TREND, X_AXIS_DATE, Y_AXIS_ADS, LEGEND_MARKET
from constants.schema.schema import COL_DATE,COL_MARKET, COMPASS_DISPLAY_COLUMNS, COL_SKILLS_MAIN, COL_SKILLS_SECONDARY, COL_TECHS_MAIN, COL_TECHS_SECONDARY, COL_TJM, COL_SENIORITY, COL_RHYTHM, COL_SECTOR, COL_NUMBER_OF_OFFERS, COL_LOCATION

def show_compass():
    CONTEXT_ID = "compass"

    if 'geocoded_locations_cache' not in st.session_state:
        st.session_state.geocoded_locations_cache = {}
        st.session_state.geocoded_locations_cache = {} # Cette ligne est redondante si la précédente a déjà été exécutée, mais l'erreur était spécifique à l'absence de l'attribut.

    st.header(HEADER_COMPASS)

    # Chargement des données
    df_market_analysis = load_market_analysis()
    df_offers_original = load_offers()
    df_offers = geocode_dataframe_locations_in_memory(df_offers_original, COL_LOCATION)

    # Vérification des colonnes nécessaires
    for col in COMPASS_DISPLAY_COLUMNS:
        if col not in df_offers.columns:
            st.warning(WARNING_MISSING_COLUMN.format(col=col))
            return

    if COL_MARKET not in df_market_analysis.columns:
        st.warning(WARNING_NO_MARKET_ANALYSIS)
        return

    # Fusionner les marchés disponibles dans les offres et dans les tendances
    markets_offers = df_offers[COL_MARKET].dropna().unique()
    markets_trends = df_market_analysis[COL_MARKET].dropna().unique()
    markets = sorted(set(markets_offers) | set(markets_trends))

    # Sélection du marché via fonction de filtre
    selected_market = filter_dataframe_by_market(df_offers, markets, label=LABEL_SELECT_MARKET)

    # Affichage de la tendance des marchés
    st.subheader(SECTION_MARKET_TRENDS)
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

    # Filtrer les offres selon le marché sélectionné
    skills_df = df_offers[df_offers[COL_MARKET] == selected_market]
    first_col, second_col, third_col, fourth_col = st.columns(4)

    with first_col:
        display_numeric_range_selector(skills_df, COL_TJM, LABEL_TJM, unit="€")
    with second_col:
        display_numeric_range_selector(skills_df, COL_SENIORITY, LABEL_SENIORITY, unit="ans")
    with third_col:
        st.subheader(LABEL_RHYTHM)
        rythm = skills_df.get(COL_RHYTHM, pd.Series()).dropna().str.strip()
        pie_chart(rythm, title=LABEL_RHYTHM, context_id=CONTEXT_ID)
    with fourth_col:
        st.subheader(LABEL_SECTOR)
        sectors = skills_df.get(COL_SECTOR, pd.Series()).dropna().str.strip()
        pie_chart(sectors, title=LABEL_SECTOR, context_id=CONTEXT_ID)

    display_offers_map(skills_df, selected_market)

    st.subheader(SECTION_SKILLS)

    st.markdown(LABEL_MAIN_SKILLS)
    main_skills = skills_df[COL_SKILLS_MAIN].dropna().str.split(",").explode().str.strip()
    bar_chart(main_skills, title=LABEL_MAIN_SKILLS, context_id=CONTEXT_ID)
    
    st.markdown(LABEL_SECONDARY_SKILLS)
    secondary_skills = skills_df[COL_SKILLS_SECONDARY].dropna().str.split(",").explode().str.strip()
    bar_chart(secondary_skills, title=LABEL_SECONDARY_SKILLS, context_id=CONTEXT_ID)
    
    st.subheader(SECTION_TECHS)

    st.markdown(LABEL_MAIN_TECHS)
    main_techs = skills_df[COL_TECHS_MAIN].dropna().str.split(",").explode().str.strip()
    bar_chart(main_techs, title=LABEL_MAIN_TECHS, context_id=CONTEXT_ID)

    st.markdown(LABEL_SECONDARY_TECHS)
    secondary_techs = skills_df[COL_TECHS_SECONDARY].dropna().str.split(",").explode().str.strip()
    bar_chart(secondary_techs, title=LABEL_SECONDARY_TECHS, context_id=CONTEXT_ID)