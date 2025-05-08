# pages/offer_dissection.py

import streamlit as st

def show_offer_dissection():
    st.header("Dissection des offres")

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
        market = st.text_input("Marché concerné")

        submitted = st.form_submit_button("Enregistrer l'offre")

        if submitted:
            st.success("Offre enregistrée avec succès !")
            # Ici tu pourras ajouter la logique pour sauvegarder l'offre dans un fichier ou une base de données
