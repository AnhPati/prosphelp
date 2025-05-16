import streamlit as st
from pages.home import show_home
from pages.market_analysis import show_market_analysis
from pages.offer_dissection import show_offer_dissection
from pages.compass import show_compass
from components.file_controls import files_controls
from config.settings import MARKET_OFFERS_FILE

st.set_page_config(page_title="Prospection Tracker", layout="wide")
st.title("Prospection Tracker 🚀")

# ✅ Import/export unique dans la sidebar
files_controls(MARKET_OFFERS_FILE, "Données Offres & Marché", uploader_key="global_data_controls")

# 📑 Onglets de navigation avec accueil
tab0, tab1, tab2, tab3 = st.tabs([
    "🏠 Accueil",
    "📈 Analyse des marchés",
    "📝 Dissection des offres",
    "🧭 Boussole"
])

# 🏠 Accueil
with tab0:
    show_home()
# 📈 Analyse des marchés
with tab1:
    show_market_analysis()

# 📝 Dissection des offres
with tab2:
    show_offer_dissection()

# 🧭 Boussole
with tab3:
    show_compass()
