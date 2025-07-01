import streamlit as st
import firebase_admin
from firebase_admin import credentials, storage
import json

from config.firebase_config import firebase_config

# 👉 Récupère les credentials depuis secrets.toml
if not firebase_admin._apps:
    firebase_creds = json.loads(json.dumps(dict(st.secrets["firebase_credentials"])))
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred, {
        "storageBucket": firebase_config["storageBucket"]
    })

bucket = storage.bucket()

def upload_csv_to_storage(local_path: str, remote_path: str) -> None:
    blob = bucket.blob(remote_path)
    blob.upload_from_filename(local_path)
    print(f"✅ Fichier '{local_path}' téléversé vers '{remote_path}'")

def download_csv_from_storage(remote_path: str, local_path: str) -> None:
    blob = bucket.blob(remote_path)
    if not blob.exists():
        print(f"⚠️ Fichier introuvable sur Firebase Storage: {remote_path}")
        return
    blob.download_to_filename(local_path)
    print(f"📥 Fichier '{remote_path}' téléchargé vers '{local_path}'")

def file_exists_in_storage(remote_path: str) -> bool:
    return bucket.blob(remote_path).exists()