# components/offer_form.py

import streamlit as st
import pandas as pd

def show_offer_form(markets: list[str], source: str = "offre"):
    st.subheader("📝 Ajouter une nouvelle entrée")

    with st.form("data_entry_form"):
        market = st.selectbox("Marché concerné", markets)

        # Initialisation par défaut
        title = job_title = offer_link = ""
        tjm = seniority = main_techs = secondary_techs = main_skills = secondary_skills = ""
        sector = location = work_mode = company = contact_name = ""
        sophistication = reliability = None

        # Ordre imposé des champs

        # 1. Titre (offre uniquement)
        if source == "offre":
            title = st.text_input("Titre de l'offre")

        # 2. Intitulé (offre uniquement)
        if source == "offre":
            job_title = st.text_input("Intitulé du poste")

        # 3. TJM
        tjm = st.text_input("TJM (Tarif Journalier Moyen)")

        # 4. Séniorité
        seniority = st.text_input("Séniorité (années d'expérience)")

        # 5. Technos principales
        main_techs = st.text_input("Technologies principales (séparées par des virgules)")

        # 6. Technos secondaires
        secondary_techs = st.text_input("Technologies secondaires (séparées par des virgules)")

        # 7. Compétences principales
        main_skills = st.text_input("Compétences principales (séparées par des virgules)")

        # 8. Compétences secondaires
        secondary_skills = st.text_input("Compétences secondaires (séparées par des virgules)")

        # 9. Secteur
        sector = st.text_input("Secteur d'activité")

        # 10. Localisation
        location = st.text_input("Localisation")

        # 11. Rythme
        work_mode = st.selectbox("Rythme", ["Présentiel", "Distanciel", "Hybride"])

        # 12. Entreprise
        company = st.text_input("Nom de l'ESN")

        # 13. Contact
        contact_name = st.text_input("Nom du contact")

        # 14. Lien (offre uniquement)
        if source == "offre":
            offer_link = st.text_input("Lien vers l'offre")

        # 15. Sophistication (contact uniquement)
        if source == "contact":
            sophistication = st.slider("Sophistication du marché", 1, 5, 3)

        # 16. Fiabilité (contact uniquement)
        if source == "contact":
            reliability = st.slider("Fiabilité du contact", 1, 5, 3)

        # Validation
        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            if source == "offre" and not (title and offer_link):
                st.error("Le titre et le lien de l'offre sont obligatoires.")
                return None
            if source == "contact" and not contact_name:
                st.error("Le nom du contact est requis.")
                return None

            return {
                "Date": pd.to_datetime("today").strftime('%Y-%m-%d'),
                "Type": "Contact" if source == "contact" else "Offre",
                "Marché": market,
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
                "Sophistication": sophistication,
                "Fiabilité": reliability
            }

    return None

def show_market_form(existing_markets: list[str]):
    use_existing = st.checkbox("Choisir un marché existant", value=True)

    with st.form("market_form"):
        if use_existing:
            market = st.selectbox("Marché existant", options=[""] + existing_markets, key="selected_market")
            new_market = None
        else:
            market = None
            new_market = st.text_input("Nouveau marché", key="new_market")

        final_market = new_market.strip() if new_market else (market if market else "")
        first_col, second_col, third_col = st.columns(3)

        with first_col:
            date = st.date_input("Date", key="selected_date", format="DD/MM/YYYY")
        with second_col:
            number = st.number_input("Nombre d'annonces", min_value=0, step=1, key="selected_number")
        with third_col:
            notes = st.text_input("Notes", key="notes")

        submitted = st.form_submit_button("Ajouter")

        return submitted, final_market, date, number, notes