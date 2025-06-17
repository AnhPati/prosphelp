import streamlit as st
from services.offer_service import load_offers
from services.market_data import load_market_analysis
from services.geocoding_service import geocode_dataframe_locations_in_memory
from components.charts import show_market_trend_chart, plot_skills_tech_chart, pie_rythms_chart
from components.interactive_numeric_display import display_numeric_range_selector
from components.interactive_map import display_offers_map
from utils.filters import filter_dataframe_by_market
from constants.alerts import WARNING_MISSING_COLUMN, WARNING_NO_MARKET_ANALYSIS, INFO_NO_TREND_DATA, INFO_NO_RYTHM_DATA, INFO_NO_SECTOR_DATA, WARNING_NO_MAIN_SKILLS, WARNING_NO_SECONDARY_SKILLS, WARNING_NO_MAIN_TECH, WARNING_NO_SECONDARY_TECH
from constants.labels import HEADER_COMPASS, SECTION_MARKET_TRENDS, LABEL_TJM, LABEL_SENIORITY, LABEL_RHYTHM, LABEL_SECTOR, SECTION_SKILLS, SECTION_TECHS, LABEL_MAIN_SKILLS, LABEL_SECONDARY_SKILLS, LABEL_MAIN_TECHS, LABEL_SECONDARY_TECHS, LABEL_SELECT_MARKET
def show_compass():
    CONTEXT_ID = "compass"

    if 'geocoded_locations_cache' not in st.session_state:
        st.session_state.geocoded_locations_cache = {}
        st.session_state.geocoded_locations_cache = {} # Cette ligne est redondante si la précédente a déjà été exécutée, mais l'erreur était spécifique à l'absence de l'attribut.

    st.header(HEADER_COMPASS)

    # Chargement des données
    df_market_analysis = load_market_analysis()
    df_offers_original = load_offers()
    df_offers = geocode_dataframe_locations_in_memory(df_offers_original, "Localisation")

    # Vérification des colonnes nécessaires
    required_columns = [
        "Marché", "Compétences principales", "Compétences secondaires",
        "Technos principales", "Technos secondaires", "TJM", "Séniorité",
        "Secteur", "Rythme", "Localisation", "latitude", "longitude"
    ]
    for col in required_columns:
        if col not in df_offers.columns:
            st.warning(WARNING_MISSING_COLUMN.format(col=col))
            return

    if "Marché" not in df_market_analysis.columns:
        st.warning(WARNING_NO_MARKET_ANALYSIS)
        return

    # Fusionner les marchés disponibles dans les offres et dans les tendances
    markets_offers = df_offers["Marché"].dropna().unique()
    markets_trends = df_market_analysis["Marché"].dropna().unique()
    markets = sorted(set(markets_offers) | set(markets_trends))

    # Sélection du marché via fonction de filtre
    selected_market = filter_dataframe_by_market(df_offers, markets, label=LABEL_SELECT_MARKET)

    # Affichage de la tendance des marchés
    st.subheader(SECTION_MARKET_TRENDS)
    if selected_market in df_market_analysis["Marché"].values:
        show_market_trend_chart(df_market_analysis, highlight_market=selected_market, context_id=CONTEXT_ID)
    else:
        st.info(INFO_NO_TREND_DATA)

    # Filtrer les offres selon le marché sélectionné
    skills_df = df_offers[df_offers["Marché"] == selected_market]
    first_col, second_col, third_col, fourth_col = st.columns(4)

    with first_col:
        display_numeric_range_selector(skills_df, "TJM", LABEL_TJM, unit="€")
    with second_col:
        display_numeric_range_selector(skills_df, "Séniorité", LABEL_SENIORITY, unit="ans")
    with third_col:
        st.subheader(LABEL_RHYTHM)

        if "Rythme" in skills_df.columns:
            sectors = skills_df["Rythme"].dropna().str.strip()
            if not sectors.empty:
                pie_rythms_chart(sectors, title="⏳ Répartition des rythmes de travail", context_id=CONTEXT_ID)
            else:
                st.info(INFO_NO_RYTHM_DATA)
        else:
            st.warning(WARNING_MISSING_COLUMN.format(col="Rythme"))
    with fourth_col:
        st.subheader(LABEL_SECTOR)

        if "Secteur" in skills_df.columns:
            sectors = skills_df["Secteur"].dropna().str.strip()
            if not sectors.empty:
                pie_rythms_chart(sectors, title="💼 Secteurs du marché", context_id=CONTEXT_ID)
            else:
                st.info(INFO_NO_SECTOR_DATA)
        else:
            st.warning(WARNING_MISSING_COLUMN.format(col="Secteur"))

    display_offers_map(skills_df, selected_market)

    st.subheader(SECTION_SKILLS)

    # Compétences principales
    main_skills = skills_df["Compétences principales"].dropna().str.split(",").explode().str.strip()
    if not main_skills.empty:
        st.markdown(LABEL_MAIN_SKILLS)
        plot_skills_tech_chart(main_skills, title=LABEL_MAIN_SKILLS, context_id=CONTEXT_ID)
    else:
        st.warning(WARNING_NO_MAIN_SKILLS)

    # Compétences secondaires
    secondary_skills = skills_df["Compétences secondaires"].dropna().str.split(",").explode().str.strip()
    if not secondary_skills.empty:
        st.markdown(LABEL_SECONDARY_SKILLS)
        plot_skills_tech_chart(secondary_skills, title=LABEL_SECONDARY_SKILLS, context_id=CONTEXT_ID)
    else:
        st.warning(WARNING_NO_SECONDARY_SKILLS)

    st.subheader(SECTION_TECHS)

    # Technologies principales
    main_techs = skills_df["Technos principales"].dropna().str.split(",").explode().str.strip()
    if not main_techs.empty:
        st.markdown(LABEL_MAIN_TECHS)
        plot_skills_tech_chart(main_techs, title=LABEL_MAIN_TECHS, context_id=CONTEXT_ID)
    else:
        st.warning(WARNING_NO_MAIN_TECH)

    # Technologies secondaires
    secondary_techs = skills_df["Technos secondaires"].dropna().str.split(",").explode().str.strip()
    if not secondary_techs.empty:
        st.markdown(LABEL_SECONDARY_TECHS)
        plot_skills_tech_chart(secondary_techs, title=LABEL_SECONDARY_TECHS, context_id=CONTEXT_ID)
    else:
        st.warning(WARNING_NO_SECONDARY_TECH)
