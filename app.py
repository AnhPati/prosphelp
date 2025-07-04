import os
import streamlit as st
import st_cookie
from pathlib import Path
from tabs.home import render_home
from tabs.market_analysis import render_market_analysis
from tabs.offer_dissection import render_offer_dissection
from tabs.compass import render_compass
from components.csv_uploader import csv_uploader
from config.settings import get_market_offers_file
from services.cache.geocoding_cache import load_cache
from services.storage.firebase_storage_service import download_csv_from_storage
from design.inject_theme import inject_theme
from components.auth.login_form import simple_login_form, logout

# 🔹 Config Streamlit
st.set_page_config(page_title="JobCompass", layout="wide")
inject_theme()

# 🔹 Restitution de session via cookies (st-cookie)
st_cookie.apply()

# 🔄 Restauration possible avant auth check
email = st.session_state.get("user_email")
user_id = st.session_state.get("user_id")
token = st.session_state.get("user_token")

if email and user_id and token and "user" not in st.session_state:
    st.session_state.user = {
        "email": email,
        "id": user_id,
        "token": token
    }

# 🔹 Authentification
if "user" not in st.session_state:
    simple_login_form()
    st.stop()

# 🔹 Déduire chemins CSV
user_id = st.session_state.user["id"]
remote_csv_path = f"users/user_{user_id}_markets.csv"
local_csv_path = get_market_offers_file(user_id)

# 🔹 Téléchargement CSV si absent
if not local_csv_path.exists():
    download_csv_from_storage(remote_path=remote_csv_path, local_path=str(local_csv_path))

# 🔹 Cache géocodage
if "geocoded_locations_cache" not in st.session_state:
    st.session_state.geocoded_locations_cache = load_cache()

# 🔹 Déconnexion + uploader dans header
col1, col2 = st.columns([6, 1])
with col1:
    csv_uploader(
        filepath=local_csv_path,
        uploader_key="header_csv_controls",
        firebase_path=remote_csv_path,
        inline=True
    )
with col2:
    st.markdown("<div style='text-align: right; margin-top: 0.5rem;'>", unsafe_allow_html=True)
    if st.button("🔓 Déconnexion", key="global_logout_btn"):
        if st.secrets["fake"]["use_fake_auth"]:
            st.switch_page("pages/logout_confirm.py")
        else:
            logout()
    st.markdown("</div>", unsafe_allow_html=True)

# 🔹 Interface principale
st.title("JobCompass")
with st.sidebar:
    if st.button("🔓 Déconnexion", key="sidebar_logout_btn"):
        if st.secrets["fake"]["use_fake_auth"]:
            st.switch_page("pages/logout_confirm.py")
        else:
            logout()

    csv_uploader(
        filepath=local_csv_path,
        title="Données Offres & Marché",
        uploader_key="sidebar_data_controls",
        firebase_path=remote_csv_path
    )

tabs = st.tabs(["🏠 Accueil", "📈 Analyse des marchés", "📝 Dissection des offres", "🧭 Boussole"])
with tabs[0]: render_home()
with tabs[1]: render_market_analysis()
with tabs[2]: render_offer_dissection()
with tabs[3]: render_compass()