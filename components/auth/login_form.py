import streamlit as st
import st_cookie
from config.settings import get_market_offers_file
from services.storage.firebase_storage_service import download_csv_from_storage
from components.auth.google_login import google_login

def simple_login_form():
    if st.secrets["fake"]["use_fake_auth"]:
        with st.form("login_form"):
            email = st.text_input("Fake Email")
            password = st.text_input("Fake Password", type="password")
            submitted = st.form_submit_button("Se connecter")
            if submitted:
                user_id = email.split("@")[0].replace(".", "_")

                st.session_state["user_email"] = email
                st.session_state["user_id"] = user_id
                st.session_state["user_token"] = "fake-token"

                st.session_state.user = {
                    "email": email, "id": user_id, "token": "fake-token"
                }
                st_cookie.update("user_email")
                st_cookie.update("user_id")
                st_cookie.update("user_token")
                st.rerun()
    else:
        google_login()

def logout():
    user_id = st.session_state.user["id"]
    local_csv_path = get_market_offers_file(user_id)
    remote_path = f"users/user_{user_id}_markets.csv"

    download_csv_from_storage(remote_path, str(local_csv_path))
    if local_csv_path.exists():
        local_csv_path.unlink()

    st_cookie.remove("user_email")
    st_cookie.remove("user_id")
    st_cookie.remove("user_token")
    st.session_state.clear()
    st.rerun()