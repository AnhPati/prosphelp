import streamlit as st
from tabs.home import render_home
from tabs.market_analysis import render_market_analysis
from tabs.offer_dissection import render_offer_dissection
from tabs.compass import render_compass
from components.csv_uploader import csv_uploader
from config.settings import MARKET_OFFERS_FILE
from services.cache.geocoding_cache import load_cache

if 'geocoded_locations_cache' not in st.session_state:
    st.session_state.geocoded_locations_cache = load_cache()

st.set_page_config(page_title="JobCompass", layout="wide")

with open("design/theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("JobCompass")

csv_uploader(
    filepath=MARKET_OFFERS_FILE,
    label="Données Offres & Marché",
    uploader_key="global_data_controls"
)

tabs = st.tabs([
    "🏠 Accueil",
    "📈 Analyse des marchés",
    "📝 Dissection des offres",
    "🧭 Boussole"
])

with tabs[0]:
    render_home()
with tabs[1]:
    render_market_analysis()
with tabs[2]:
    render_offer_dissection()
with tabs[3]:
    render_compass()
