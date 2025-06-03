import streamlit as st
import pandas as pd
from services.offer_service import load_offers
from services.market_data import load_market_analysis
from components.charts import show_market_trend_chart, plot_skills_tech_chart
from utils.filters import filter_dataframe_by_market

def show_compass():
    st.header("🧭 Boussole de l'Analyse du Marché")

    # Chargement des données
    df_market_analysis = load_market_analysis()
    df_offers = load_offers()

    # Vérification des colonnes nécessaires
    required_columns = [
        "Marché", "Compétences principales", "Compétences secondaires",
        "Technos principales", "Technos secondaires"
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

    st.subheader("💼 Compétences")

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
