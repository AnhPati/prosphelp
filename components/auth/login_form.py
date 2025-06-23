import streamlit as st
from config.settings import MARKET_OFFERS_FILE
from services.storage.firebase_storage_service import download_csv_from_storage

def simple_login_form():
    with st.form("login_form"):
        email = st.text_input("Email Google")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")

        if submitted:
            st.session_state.user = {
                "email": email,
                "id": "dev-user"  # ⚠️ Fake ID pour test
            }

def logout():
    with st.sidebar:
        if "user" in st.session_state:
            if st.button("🚪 Déconnexion"):
                # 🔽 Sauvegarde du CSV local avant de quitter
                user_id = st.session_state["user"]["id"]
                remote_path = f"users/user_{user_id}_markets.csv"
                download_csv_from_storage(remote_path, str(MARKET_OFFERS_FILE))

                # 🔚 Supprimer l'utilisateur et relancer l'app
                del st.session_state["user"]
                st.rerun()
