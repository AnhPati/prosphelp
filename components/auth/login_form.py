import streamlit as st

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
    if "user" in st.session_state:
        del st.session_state["user"]