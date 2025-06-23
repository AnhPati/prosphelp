import os
import streamlit as st
from tabs.home import render_home
from tabs.market_analysis import render_market_analysis
from tabs.offer_dissection import render_offer_dissection
from tabs.compass import render_compass
from components.csv_uploader import csv_uploader
from config.settings import MARKET_OFFERS_FILE
from services.cache.geocoding_cache import load_cache
from services.storage.firebase_storage_service import download_csv_from_storage
from design.inject_theme import inject_theme
from components.auth.login_form import simple_login_form, logout

# 🔹 Config Streamlit
st.set_page_config(page_title="JobCompass", layout="wide")
inject_theme()

# 🔹 Authentification
if "user" not in st.session_state:
    simple_login_form()
    st.stop()

# 🔹 Déduire le chemin utilisateur à partir de son ID
user_id = st.session_state.user["id"]
remote_csv_path = f"users/user_{user_id}_markets.csv"

# 🔹 Télécharger le CSV personnalisé s'il n'existe pas encore localement
if not os.path.exists(MARKET_OFFERS_FILE):
    download_csv_from_storage(
        remote_path=remote_csv_path,
        local_path=str(MARKET_OFFERS_FILE)
    )

# 🔹 Charger le cache de géocodage
if 'geocoded_locations_cache' not in st.session_state:
    st.session_state.geocoded_locations_cache = load_cache()

# 🔹 Afficher le bouton de déconnexion
logout()

# 🔹 Titre de l'application
st.title("JobCompass")

# 🔹 Upload CSV personnalisé
csv_uploader(
    filepath=MARKET_OFFERS_FILE,
    label="Données Offres & Marché",
    uploader_key="global_data_controls",
    firebase_path=remote_csv_path  # ✅ important : upload vers chemin utilisateur
)

# 🔹 Navigation par onglets
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