import streamlit as st
from services.offer_service import load_offers
from services.market_data import load_market_analysis
from components.charts import show_market_trend_chart, plot_skills_tech_chart

def show_compass():
    st.header("Boussole de l'Analyse du Marché")

    # Charger les données du marché et des offres
    df_market_analysis = load_market_analysis()
    df_offers = load_offers()

    # Vérification des colonnes nécessaires dans les données d'offres
    required_columns = ["Marché", "Compétences principales", "Compétences secondaires", "Technos principales", "Technos secondaires"]
    for col in required_columns:
        if col not in df_offers.columns:
            st.warning(f"⚠️ La colonne {col} est manquante dans les données.")
            return

    # Vérification de la présence de la colonne "Marché" dans l'analyse du marché
    if "Marché" not in df_market_analysis.columns:
        st.warning("⚠️ Aucune analyse de marché n'est disponible.")
        return

    # Fusionner tous les marchés présents dans les offres et les Notess
    markets_offers = df_offers["Marché"].dropna().unique()
    markets_trends = df_market_analysis["Marché"].dropna().unique()
    markets = sorted(set(markets_offers) | set(markets_trends))  # union des deux ensembles

    # Sélection du marché
    selected_market = st.selectbox("Sélectionner un marché", markets, index=0)

    # Notes des marchés (graphique global avec un marché mis en avant)
    st.subheader("📈 Notes des Marchés")
    if selected_market in df_market_analysis["Marché"].values:
        show_market_trend_chart(df_market_analysis, highlight_market=selected_market)
    else:
        st.info("ℹ️ Aucune donnée de Notes disponible pour ce marché.")

    # Compétences principales et secondaires
    st.subheader("💼 Compétences principales et secondaires")
    skills_df = df_offers[df_offers["Marché"] == selected_market]

    main_skills = skills_df["Compétences principales"].dropna().str.split(",").explode().str.strip()
    secondary_skills = skills_df["Compétences secondaires"].dropna().str.split(",").explode().str.strip()

    if not main_skills.empty:
        st.subheader("Compétences principales")
        plot_skills_tech_chart(main_skills, title="Compétences principales")
    else:
        st.warning("⚠️ Aucune compétence principale disponible pour ce marché.")

    if not secondary_skills.empty:
        st.subheader("Compétences secondaires")
        plot_skills_tech_chart(secondary_skills, title="Compétences secondaires")
    else:
        st.warning("⚠️ Aucune compétence secondaire disponible pour ce marché.")

    # Technologies principales et secondaires
    st.subheader("💻 Technologies principales et secondaires")
    main_techs = skills_df["Technos principales"].dropna().str.split(",").explode().str.strip()
    secondary_techs = skills_df["Technos secondaires"].dropna().str.split(",").explode().str.strip()

    if not main_techs.empty:
        st.subheader("Technologies principales")
        plot_skills_tech_chart(main_techs, title="Technologies principales")
    else:
        st.warning("⚠️ Aucune technologie principale disponible pour ce marché.")

    if not secondary_techs.empty:
        st.subheader("Technologies secondaires")
        plot_skills_tech_chart(secondary_techs, title="Technologies secondaires")
    else:
        st.warning("⚠️ Aucune technologie secondaire disponible pour ce marché.")
