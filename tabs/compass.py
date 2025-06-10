import streamlit as st
from services.offer_service import load_offers
from services.market_data import load_market_analysis
from services.geocoding_service import geocode_dataframe_locations_in_memory
from components.charts import show_market_trend_chart, plot_skills_tech_chart, pie_rythms_chart
from components.interactive_numeric_display import display_numeric_range_selector
from components.interactive_map import display_offers_map
from utils.filters import filter_dataframe_by_market

def show_compass():
    if 'geocoded_locations_cache' not in st.session_state:
        st.session_state.geocoded_locations_cache = {}
        st.session_state.geocoded_locations_cache = {} # Cette ligne est redondante si la précédente a déjà été exécutée, mais l'erreur était spécifique à l'absence de l'attribut.

    st.header("🧭 Boussole de l'Analyse du Marché")

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
            st.warning(f"⚠️ La colonne {col} est manquante dans les données.")
            return

    if "Marché" not in df_market_analysis.columns:
        st.warning("⚠️ Aucune analyse de marché n'est disponible.")
        return

    # Fusionner les marchés disponibles dans les offres et dans les tendances
    markets_offers = df_offers["Marché"].dropna().unique()
    markets_trends = df_market_analysis["Marché"].dropna().unique()
    markets = sorted(set(markets_offers) | set(markets_trends))

    # Sélection du marché via fonction de filtre
    selected_market = filter_dataframe_by_market(df_offers, markets, label="🎯 Sélectionner un marché")

    # Affichage de la tendance des marchés
    st.subheader("📈 Tendance des Marchés")
    if selected_market in df_market_analysis["Marché"].values:
        show_market_trend_chart(df_market_analysis, highlight_market=selected_market, context_id="compass")
    else:
        st.info("ℹ️ Aucune donnée de tendance disponible pour ce marché.")

    # Filtrer les offres selon le marché sélectionné
    skills_df = df_offers[df_offers["Marché"] == selected_market]
    first_col, second_col, third_col, fourth_col = st.columns(4)

    with first_col:
        display_numeric_range_selector(skills_df, "TJM", "💰 TJM (Taux Journalier Moyen)", unit="€")
    with second_col:
        display_numeric_range_selector(skills_df, "Séniorité", "📚 Séniorité", unit="ans")
    with third_col:
        st.subheader("⏳ Rythme de travail")

        if "Rythme" in skills_df.columns:
            sectors = skills_df["Rythme"].dropna().str.strip()
            if not sectors.empty:
                pie_rythms_chart(sectors, title="⏳ Répartition des rythmes de travail", context_id="compass")
            else:
                st.info("ℹ️ Aucune donnée sur le rythme de travail pour ce marché.")
        else:
            st.warning("⚠️ La colonne 'Rythme' est absente des données.")
    with fourth_col:
        st.subheader("💼 Secteurs")

        if "Secteur" in skills_df.columns:
            sectors = skills_df["Secteur"].dropna().str.strip()
            if not sectors.empty:
                pie_rythms_chart(sectors, title="💼 Secteurs du marché", context_id="compass")
            else:
                st.info("ℹ️ Aucune donnée sur le secteur de travail pour ce marché.")
        else:
            st.warning("⚠️ La colonne 'Secteur' est absente des données.")

    display_offers_map(skills_df, selected_market)

    st.subheader("🛠️ Compétences")

    # Compétences principales
    main_skills = skills_df["Compétences principales"].dropna().str.split(",").explode().str.strip()
    if not main_skills.empty:
        st.markdown("**Compétences principales**")
        plot_skills_tech_chart(main_skills, title="Compétences principales", context_id="compass")
    else:
        st.warning("⚠️ Aucune compétence principale disponible pour ce marché.")

    # Compétences secondaires
    secondary_skills = skills_df["Compétences secondaires"].dropna().str.split(",").explode().str.strip()
    if not secondary_skills.empty:
        st.markdown("**Compétences secondaires**")
        plot_skills_tech_chart(secondary_skills, title="Compétences secondaires", context_id="compass")
    else:
        st.warning("⚠️ Aucune compétence secondaire disponible pour ce marché.")

    st.subheader("💻 Technologies")

    # Technologies principales
    main_techs = skills_df["Technos principales"].dropna().str.split(",").explode().str.strip()
    if not main_techs.empty:
        st.markdown("**Technologies principales**")
        plot_skills_tech_chart(main_techs, title="Technologies principales", context_id="compass")
    else:
        st.warning("⚠️ Aucune technologie principale disponible pour ce marché.")

    # Technologies secondaires
    secondary_techs = skills_df["Technos secondaires"].dropna().str.split(",").explode().str.strip()
    if not secondary_techs.empty:
        st.markdown("**Technologies secondaires**")
        plot_skills_tech_chart(secondary_techs, title="Technologies secondaires", context_id="compass")
    else:
        st.warning("⚠️ Aucune technologie secondaire disponible pour ce marché.")
