import streamlit as st
from tabs.home import render_home
from tabs.market_analysis import render_market_analysis
from tabs.offer_dissection import render_offer_dissection
from tabs.compass import render_compass
from components.csv_uploader import csv_uploader
from config.settings import MARKET_OFFERS_FILE
from services.cache.geocoding_cache import load_cache
from design.inject_theme import inject_theme
from components.auth.login_form import simple_login_form, logout  # ✅ import logout

if 'geocoded_locations_cache' not in st.session_state:
    st.session_state.geocoded_locations_cache = load_cache()

st.set_page_config(page_title="JobCompass", layout="wide")

inject_theme()

# Interface d'authentification
if "user" not in st.session_state:
    simple_login_form()
    st.stop()
    
logout()  # ✅ appel propre

st.title("JobCompass")

# Upload des données CSV
csv_uploader(
    filepath=MARKET_OFFERS_FILE,
    label="Données Offres & Marché",
    uploader_key="global_data_controls"
)

# Navigation entre les onglets
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