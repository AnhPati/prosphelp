import requests
import time
import pandas as pd
import streamlit as st
from constants.alerts import ERROR_MISSING_LOCATION_COLUMN, INFO_GEOCODING_IN_PROGRESS, INFO_ALL_LOCATIONS_CACHED, SUCCESS_GEOCODING_DONE, PROGRESS_GEOCODING_TEXT

def _geocode_single_location(location_name: str) -> tuple[float | None, float | None]:
    if not isinstance(location_name, str) or not location_name.strip():
        return None, None

    if location_name in st.session_state.geocoded_locations_cache:
        return st.session_state.geocoded_locations_cache[location_name]['lat'], st.session_state.geocoded_locations_cache[location_name]['lon']

    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1,
        "addressdetails": 0
    }
    headers = {
        "User-Agent": "YourStreamlitApp/1.0 (anhpati@gmail.com)"
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            st.session_state.geocoded_locations_cache[location_name] = {'lat': lat, 'lon': lon}
            return lat, lon
        else:
            st.session_state.geocoded_locations_cache[location_name] = {'lat': None, 'lon': None}
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la géocodification de '{location_name}': {e}")
        st.session_state.geocoded_locations_cache[location_name] = {'lat': None, 'lon': None}
        return None, None
    finally:
        time.sleep(1)


def geocode_dataframe_locations_in_memory(df: pd.DataFrame, location_col: str) -> pd.DataFrame:
    if location_col not in df.columns:
        st.error(ERROR_MISSING_LOCATION_COLUMN.format(column=location_col))
        return df.copy()

    df_with_coords = df.copy()

    if 'latitude' not in df_with_coords.columns:
        df_with_coords['latitude'] = None
    if 'longitude' not in df_with_coords.columns:
        df_with_coords['longitude'] = None

    locations_to_process = df_with_coords[location_col].dropna().unique()

    locations_needing_geocoding = []
    for loc in locations_to_process:
        if loc in st.session_state.geocoded_locations_cache:
            lat_cached = st.session_state.geocoded_locations_cache[loc]['lat']
            lon_cached = st.session_state.geocoded_locations_cache[loc]['lon']
            df_with_coords.loc[df_with_coords[location_col] == loc, 'latitude'] = lat_cached
            df_with_coords.loc[df_with_coords[location_col] == loc, 'longitude'] = lon_cached
        elif (df_with_coords.loc[df_with_coords[location_col] == loc, 'latitude'].isnull().all() or
              df_with_coords.loc[df_with_coords[location_col] == loc, 'longitude'].isnull().all()):
            locations_needing_geocoding.append(loc)

    message_container = st.empty()
    progress_container = st.empty()

    if locations_needing_geocoding:
        message_container.info(
            INFO_GEOCODING_IN_PROGRESS.format(
                count=len(locations_needing_geocoding),
                s="s" if len(locations_needing_geocoding) > 1 else ""
            )
        )

        geocode_bar = progress_container.progress(0, text=PROGRESS_GEOCODING_TEXT)

        for i, loc in enumerate(locations_needing_geocoding):
            lat, lon = _geocode_single_location(str(loc))
            df_with_coords.loc[df_with_coords[location_col] == loc, 'latitude'] = lat
            df_with_coords.loc[df_with_coords[location_col] == loc, 'longitude'] = lon
            geocode_bar.progress((i + 1) / len(locations_needing_geocoding), text=PROGRESS_GEOCODING_TEXT)

        progress_container.empty()
        message_container.success(SUCCESS_GEOCODING_DONE)
        time.sleep(2)
        message_container.empty()
    else:
        message_container.info(INFO_ALL_LOCATIONS_CACHED)
        progress_container.empty()

    return df_with_coords