# components/interactive_map.py

import streamlit as st
import pandas as pd
import plotly.express as px

def display_offers_map(df_with_coords: pd.DataFrame, market_name: str):
    st.subheader("📍 Localisation des Offres")

    df_with_coords['latitude'] = pd.to_numeric(df_with_coords['latitude'], errors='coerce')
    df_with_coords['longitude'] = pd.to_numeric(df_with_coords['longitude'], errors='coerce')

    map_data_aggregated = df_with_coords.groupby(['Localisation', 'latitude', 'longitude']).size().reset_index(name='Nombre_Offres')
    map_data_aggregated = map_data_aggregated.dropna(subset=['latitude', 'longitude'])

    if not map_data_aggregated.empty:
        fig = px.scatter_mapbox(map_data_aggregated,
                                lat="latitude",
                                lon="longitude",
                                color="Nombre_Offres",
                                size="Nombre_Offres",
                                hover_name="Localisation",
                                hover_data={"Nombre_Offres": True, "latitude": False, "longitude": False},
                                zoom=3, # Ajustez le zoom initial (ex: 3 pour la France)
                                height=500,
                                title=f"Nombre d'offres par localisation pour le marché '{market_name}'",
                                color_continuous_scale=px.colors.sequential.Plasma, # Palette de couleurs
                               )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

        st.info(f"Affichage de {len(map_data_aggregated)} localisations uniques sur la carte pour le marché '{market_name}'. La couleur et la taille des points indiquent le nombre d'offres.")

        st.markdown("**Détail par localisation :**")
        st.dataframe(map_data_aggregated.sort_values(by="Nombre_Offres", ascending=False).reset_index(drop=True))

    else:
        st.info("ℹ️ Aucune donnée de localisation valide avec des coordonnées géographiques disponible pour ce marché sélectionné.")