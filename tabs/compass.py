import streamlit as st
from services.offer_service import load_offers
from services.market_data import load_market_analysis
from components.charts import show_market_trend_chart, plot_skills_tech_chart, pie_rythms_chart
from components.interactive_numeric_display import display_numeric_range_selector
from utils.filters import filter_dataframe_by_market
import requests
import time
import plotly.express as px #

# Exemple de fonction de géocodification (à déplacer idéalement dans services/offer_service.py ou utils/helpers.py)
def geocode_location(location_name):
    """
    Géocode un nom de lieu en utilisant l'API Nominatim d'OpenStreetMap.
    Attention : Nominatim a des limites de taux. Pour une utilisation en production,
    envisagez des services payants comme Google Geocoding API.
    """
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "YourStreamlitApp/1.0 (votre_email@example.com)"  # Indispensable pour Nominatim
    }
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la géocodification de {location_name}: {e}")
        return None, None
    finally:
        time.sleep(1)  # Respecter les limites de taux de Nominatim

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
    first_col, second_col, third_col, fourth_col = st.columns(4)

    with first_col:
        display_numeric_range_selector(skills_df, "TJM", "💰 TJM (Taux Journalier Moyen)", unit="€")
    with second_col:
        display_numeric_range_selector(skills_df, "Séniorité", "🎯 Séniorité", unit="ans")
    with third_col:
        st.subheader("🏠 Rythme de travail")

        if "Rythme" in skills_df.columns:
            sectors = skills_df["Rythme"].dropna().str.strip()
            if not sectors.empty:
                pie_rythms_chart(sectors, title="Répartition des rythmes de travail", context_id="compass")
            else:
                st.info("ℹ️ Aucune donnée sur le rythme de travail pour ce marché.")
        else:
            st.warning("⚠️ La colonne 'Rythme' est absente des données.")
    with fourth_col:
        st.subheader("🏠 Secteurs")

        if "Secteur" in skills_df.columns:
            sectors = skills_df["Secteur"].dropna().str.strip()
            if not sectors.empty:
                pie_rythms_chart(sectors, title="Secteurs du marché", context_id="compass")
            else:
                st.info("ℹ️ Aucune donnée sur le secteur de travail pour ce marché.")
        else:
            st.warning("⚠️ La colonne 'Secteur' est absente des données.")

    # --- Affichage de la localisation sur une carte avec coloration par nombre d'offres ---
    st.subheader("📍 Localisation des Offres")

    # Géocodage des localisations (si latitude/longitude ne sont pas déjà présentes)
    # Il est fortement recommandé de géocoder au chargement des données (offer_service.py)
    if 'latitude' not in skills_df.columns or 'longitude' not in skills_df.columns:
        st.info("Géocodage des localisations. Cela peut prendre un certain temps si c'est la première fois ou si de nouvelles localisations apparaissent.")
        # Utilise st.session_state pour cacher les résultats de géocodification
        if 'geocoded_cache' not in st.session_state:
            st.session_state.geocoded_cache = {}

        skills_df['latitude'] = None
        skills_df['longitude'] = None

        unique_locations_to_geocode = skills_df['Localisation'].dropna().unique()
        progress_text = "Opération de géocodification en cours. Veuillez patienter..."
        geocode_bar = st.progress(0, text=progress_text)
        total_locations = len(unique_locations_to_geocode)

        for i, loc in enumerate(unique_locations_to_geocode):
            if loc not in st.session_state.geocoded_cache:
                lat, lon = geocode_location(loc)
                st.session_state.geocoded_cache[loc] = {'lat': lat, 'lon': lon}
            skills_df.loc[skills_df['Localisation'] == loc, 'latitude'] = st.session_state.geocoded_cache[loc]['lat']
            skills_df.loc[skills_df['Localisation'] == loc, 'longitude'] = st.session_state.geocoded_cache[loc]['lon']
            geocode_bar.progress((i + 1) / total_locations, text=progress_text)
        geocode_bar.empty() # Supprime la barre de progression une fois terminé


    # Agrégation des données par localisation pour la coloration
    map_data_aggregated = skills_df.groupby(['Localisation', 'latitude', 'longitude']).size().reset_index(name='Nombre_Offres')
    map_data_aggregated = map_data_aggregated.dropna(subset=['latitude', 'longitude'])

    if not map_data_aggregated.empty:
        # Configuration de Mapbox (nécessite une clé d'accès Mapbox pour des fonds de carte avancés,
        # mais Plotly peut utiliser un fonds de carte par défaut sans clé)
        # st.secrets["mapbox_token"] si vous utilisez un secret
        # px.set_mapbox_access_token(st.secrets["mapbox_token"])

        fig = px.scatter_mapbox(map_data_aggregated,
                                lat="latitude",
                                lon="longitude",
                                color="Nombre_Offres", # Colorie en fonction du nombre d'offres
                                size="Nombre_Offres",  # La taille du point indique aussi le nombre d'offres
                                hover_name="Localisation",
                                hover_data={"Nombre_Offres": True, "latitude": False, "longitude": False},
                                zoom=3, # Zoom initial (ajustez selon la zone géographique)
                                height=500,
                                title=f"Nombre d'offres par localisation pour le marché '{selected_market}'",
                                color_continuous_scale=px.colors.sequential.Plasma, # Palette de couleurs
                                # mapbox_style="carto-positron" # Peut nécessiter une clé Mapbox pour d'autres styles
                               )
        fig.update_layout(mapbox_style="open-street-map") # Utilisation d'OpenStreetMap (gratuit)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

        st.info(f"Affichage de {len(map_data_aggregated)} localisations uniques sur la carte pour le marché '{selected_market}'. La couleur et la taille des points indiquent le nombre d'offres.")

        # Afficher le tableau agrégé
        st.markdown("**Détail par localisation :**")
        st.dataframe(map_data_aggregated.sort_values(by="Nombre_Offres", ascending=False).reset_index(drop=True))

    else:
        st.info("ℹ️ Aucune donnée de localisation valide avec des coordonnées géographiques disponible pour ce marché.")

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
