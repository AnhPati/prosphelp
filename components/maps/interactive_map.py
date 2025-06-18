import streamlit as st
import pandas as pd
import plotly.express as px
from constants.alerts import INFO_NO_COORDINATES_DATA, INFO_MAP_SUMMARY
from constants.labels import SECTION_MAP_OFFERS, LABEL_MAP_DETAIL

def display_offers_map(df_with_coords: pd.DataFrame, market_name: str):
    st.subheader(SECTION_MAP_OFFERS)

    df_with_coords['latitude'] = pd.to_numeric(df_with_coords['latitude'], errors='coerce')
    df_with_coords['longitude'] = pd.to_numeric(df_with_coords['longitude'], errors='coerce')

    map_data_aggregated = df_with_coords.groupby(['Localisation', 'latitude', 'longitude']).size().reset_index(name='Nombre_Offres')
    map_data_aggregated = map_data_aggregated.dropna(subset=['latitude', 'longitude'])

    if not map_data_aggregated.empty:
        fig = px.scatter_mapbox(
            map_data_aggregated,
            lat="latitude",
            lon="longitude",
            color="Nombre_Offres",
            size="Nombre_Offres",
            hover_name="Localisation",
            hover_data={"Nombre_Offres": True, "latitude": False, "longitude": False},
            zoom=3,
            height=500,
            title=f"Nombre d'offres par localisation pour le marché '{market_name}'",
            color_continuous_scale=px.colors.sequential.Plasma
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)

        st.info(INFO_MAP_SUMMARY.format(
            n=len(map_data_aggregated),
            s="s" if len(map_data_aggregated) > 1 else "",
            market_name=market_name
        ))

        st.markdown(LABEL_MAP_DETAIL)
        columns_to_exclude = ['latitude', 'longitude']
        df_locations = map_data_aggregated.drop(columns=columns_to_exclude)
        st.dataframe(df_locations.sort_values(by="Nombre_Offres", ascending=False).reset_index(drop=True))

    else:
        st.info(INFO_NO_COORDINATES_DATA)