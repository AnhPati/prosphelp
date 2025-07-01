import streamlit as st
from urllib.parse import urlencode
import requests

def google_login():
    # 🔐 Paramètres OAuth2
    client_id = st.secrets["google"]["client_id"]
    client_secret = st.secrets["google"]["client_secret"]
    redirect_uri = st.secrets["auth"]["redirect_uri"]
    token_url = "https://oauth2.googleapis.com/token"
    userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"

    query_params = st.query_params

    # ✅ Si on a déjà un user : on nettoie le code et on sort
    if "user" in st.session_state:
        if "code" in query_params:
            st.query_params.clear()
        return

    # ✅ Si un code est présent : on tente de l’échanger une seule fois
    if "code" in query_params:
        code = query_params["code"]

        try:
            response = requests.post(token_url, data={
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            })

            token_data = response.json()
            access_token = token_data.get("access_token")

            if access_token:
                userinfo_response = requests.get(
                    userinfo_url,
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                userinfo = userinfo_response.json()

                st.session_state.user = {
                    "email": userinfo.get("email"),
                    "id": userinfo.get("sub"),
                    "token": access_token
                }

            else:
                st.error("❌ Erreur lors de la récupération du token Google.")

        except Exception as e:
            st.error(f"❌ Erreur OAuth : {e}")

        # 🧹 Nettoyage dans tous les cas (réussi ou échoué)
        st.query_params.clear()
        st.rerun()

    # 🟡 Pas encore connecté : afficher le bouton
    params = {
        "client_id": client_id,
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": redirect_uri,
        "prompt": "select_account"
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    st.link_button("🔐 Connexion avec Google", auth_url)