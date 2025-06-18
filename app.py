import streamlit as st
from tabs.home import show_home
from tabs.market_analysis import show_market_analysis
from tabs.offer_dissection import show_offer_dissection
from tabs.compass import show_compass
from components.csv_uploader import csv_uploader
from config.settings import MARKET_OFFERS_FILE
from services.cache.geocoding_cache import load_cache

if 'geocoded_locations_cache' not in st.session_state:
    st.session_state.geocoded_locations_cache = load_cache()

st.set_page_config(page_title="JobCompass", layout="wide")
st.title("JobCompass")

csv_uploader(
    filepath=MARKET_OFFERS_FILE,
    label="Données Offres & Marché",
    uploader_key="global_data_controls"
)

tab0, tab1, tab2, tab3 = st.tabs([
    "🏠 Accueil",
    "📈 Analyse des marchés",
    "📝 Dissection des offres",
    "🧭 Boussole"
])

with tab0:
    show_home()
with tab1:
    show_market_analysis()
with tab2:
    show_offer_dissection()
with tab3:
    show_compass()
