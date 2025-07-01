import streamlit as st
import st_cookie
from urllib.parse import urlencode
import requests

def google_login():
    client_id = st.secrets["google"]["client_id"]
    client_secret = st.secrets["google"]["client_secret"]
    redirect_uri = st.secrets["auth"]["redirect_uri"]
    token_url = "https://oauth2.googleapis.com/token"
    userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"

    # ✅ Restaurer la session depuis les cookies (via session_state)
    if "user" not in st.session_state:
        email = st.session_state.get("user_email")
        user_id = st.session_state.get("user_id")
        token = st.session_state.get("user_token")

        if email and user_id and token:
            st.session_state.user = {
                "email": email,
                "id": user_id,
                "token": token
            }
            return  # Session restaurée

    # ✅ Si déjà connecté, on ne fait rien
    if "user" in st.session_state:
        return

    # ✅ Traitement du code OAuth
    qp = st.query_params
    if "code" in qp:
        code = qp.get("code")
        if isinstance(code, list):
            code = code[0]

        st.query_params.clear()

        resp = requests.post(token_url, data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        })
        token_data = resp.json()
        access_token = token_data.get("access_token")

        if not access_token:
            st.error(f"❌ Échec récupération du token Google : {token_data.get('error_description', token_data)}")
            return

        # ✅ Récupération des infos utilisateur
        ui = requests.get(userinfo_url, headers={"Authorization": f"Bearer {access_token}"}).json()
        st.session_state.user = {
            "email": ui.get("email"),
            "id": ui.get("sub"),
            "token": access_token
        }

        # ✅ Stockage dans session_state → persistance via st_cookie
        st.session_state["user_email"] = ui.get("email")
        st.session_state["user_id"] = ui.get("sub")
        st.session_state["user_token"] = access_token

        st_cookie.update("user_email")
        st_cookie.update("user_id")
        st_cookie.update("user_token")

        st.rerun()
        return

    # 🟡 Afficher le bouton si pas encore connecté
    st.link_button("🔐 Connexion avec Google", f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode({
        'client_id': client_id,
        'response_type': 'code',
        'scope': 'openid email profile',
        'redirect_uri': redirect_uri,
        'prompt': 'select_account'
    })}")