import streamlit as st
from pages.market_analysis import show_market_analysis
from pages.offer_dissection import show_offer_dissection
from pages.compass import show_compass  # Importer la fonction show_compass de la page compass

st.set_page_config(page_title="Prospection Tracker", layout="wide")
st.title("Prospection Tracker 🚀")

tab1, tab2, tab3 = st.tabs(["📈 Analyse des marchés", "📝 Dissection des offres", "🧭 Boussole"])

with tab1:
    show_market_analysis()

with tab2:
    show_offer_dissection()

with tab3:
    show_compass()  # Appeler la fonction show_compass pour afficher la page Boussole
