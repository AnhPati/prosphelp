# pages/offer_dissection.py

import streamlit as st
import pandas as pd
from pathlib import Path

# Répertoire contenant les données
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)  # Crée le dossier s'il n'existe pas

OFFERS_FILE = DATA_DIR / "offers.csv"
MARKETS_FILE = DATA_DIR / "market_analysis.csv"

def get_existing_markets():
    if MARKETS_FILE.exists():
        df = pd.read_csv(MARKETS_FILE)
        if "Marché" in df.columns:
            return sorted(df["Marché"].dropna().unique())
    return []

def save_offer(offer_data):
    df = pd.DataFrame([offer_data])
    if OFFERS_FILE.exists():
        df.to_csv(OFFERS_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(OFFERS_FILE, index=False)

def show_offer_dissection():
    st.header("Dissection des offres")

    markets = get_existing_markets()
    if not markets:
        st.warning("⚠️ Aucun marché détecté dans le fichier `market_analysis.csv`. Veuillez d'abord en créer via l'onglet Analyse des marchés.")
        return

    with st.form("offer_dissection_form"):
        title = st.text_input("Titre de l'offre")
        job_title = st.text_input("Intitulé du poste")
        tjm = st.text_input("TJM (Tarif Journalier Moyen)")
        seniority = st.text_input("Séniorité (années d'expérience)")
        main_techs = st.text_input("Technologies principales (séparées par des virgules)")
        secondary_techs = st.text_input("Technologies secondaires (séparées par des virgules)")
        main_skills = st.text_input("Compétences principales (séparées par des virgules)")
        secondary_skills = st.text_input("Compétences secondaires (séparées par des virgules)")
        sector = st.text_input("Secteur d'activité")
        location = st.text_input("Localisation")
        work_mode = st.selectbox("Rythme", ["Présentiel", "Distanciel", "Hybride"])
        company = st.text_input("Nom de l'entreprise")
        contact_name = st.text_input("Nom du contact")
        offer_link = st.text_input("Lien vers l'offre")
        market = st.selectbox("Marché concerné", markets)

        submitted = st.form_submit_button("Enregistrer l'offre")

        if submitted:
            offer_data = {
                "Titre": title,
                "Intitulé": job_title,
                "TJM": tjm,
                "Séniorité": seniority,
                "Technos principales": main_techs,
                "Technos secondaires": secondary_techs,
                "Compétences principales": main_skills,
                "Compétences secondaires": secondary_skills,
                "Secteur": sector,
                "Localisation": location,
                "Rythme": work_mode,
                "Entreprise": company,
                "Contact": contact_name,
                "Lien": offer_link,
                "Marché": market
            }
            save_offer(offer_data)
            st.success("✅ Offre enregistrée avec succès !")

    st.subheader("📄 Offres enregistrées")
    if OFFERS_FILE.exists():
        offers_df = pd.read_csv(OFFERS_FILE)
        st.dataframe(offers_df)
    else:
        st.info("Aucune offre enregistrée pour le moment.")
