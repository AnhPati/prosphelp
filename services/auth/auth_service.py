import pyrebase
from config.firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def login_with_google(token_id):
    try:
        user = auth.sign_in_with_custom_token(token_id)
        return user
    except Exception as e:
        print(f"Login error: {e}")
        return None