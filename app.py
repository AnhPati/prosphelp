import streamlit as st
from pages.market_analysis import show_market_analysis
from pages.offer_dissection import show_offer_dissection

st.set_page_config(page_title="Prospection Tracker", layout="wide")
st.title("Prospection Tracker 🚀")

tab1, tab2 = st.tabs(["📈 Analyse des marchés", "📝 Dissection des offres"])

with tab1:
    show_market_analysis()

with tab2:
    show_offer_dissection()