import streamlit as st
import st_cookie
from config.settings import MARKET_OFFERS_FILE
from services.storage.firebase_storage_service import download_csv_from_storage
from components.auth.google_login import google_login

def simple_login_form():
    if st.secrets["fake"]["use_fake_auth"]:
        with st.form("login_form"):
            email = st.text_input("Fake Email")
            password = st.text_input("Fake Password", type="password")
            submitted = st.form_submit_button("Se connecter")
            if submitted:
                st.session_state.user = {
                    "email": email, "id": "dev-user", "token": "fake-token"
                }
                # 🎯 Persistance cookies
                st_cookie.update("user_email")
                st_cookie.update("user_id")
                st_cookie.update("user_token")
                st.rerun()
    else:
        google_login()

def logout():
    with st.sidebar:
        if "user" in st.session_state and st.button("🚪 Déconnexion"):
            user_id = st.session_state.user["id"]
            remote_path = f"users/user_{user_id}_markets.csv"
            download_csv_from_storage(remote_path, str(MARKET_OFFERS_FILE))
            # 💥 Effacer cookies
            st_cookie.remove("user_email")
            st_cookie.remove("user_id")
            st_cookie.remove("user_token")

            st.session_state.clear()
            st.rerun()