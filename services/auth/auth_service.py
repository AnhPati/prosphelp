import pyrebase
from config.firebase_config import firebase_config, USE_FAKE_AUTH

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def login_with_google(token_id: str):
    """
    Authentifie un utilisateur avec un token Google.
    Si le mode développeur est activé, retourne un utilisateur fictif.
    """
    if USE_FAKE_AUTH:
        print("⚠️ Mode développeur : authentification simulée.")
        return {
            "email": "dev@jobcompass.local",
            "id": "dev-user",
            "token": "fake-token"
        }

    try:
        user = auth.sign_in_with_custom_token(token_id)
        return {
            "email": user.get("email"),
            "id": user.get("localId"),
            "token": user.get("idToken")
        }
    except Exception as e:
        print(f"❌ Erreur de connexion Google : {e}")
        return None