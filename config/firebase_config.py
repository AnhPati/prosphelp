import streamlit as st

firebase_config = {
    "apiKey": st.secrets["firebase"]["firebase_api_key"],
    "authDomain": st.secrets["firebase"]["firebase_auth_domain"],
    "projectId": st.secrets["firebase"]["firebase_project_id"],
    "storageBucket": st.secrets["firebase"]["firebase_storage_bucket"],
    "messagingSenderId": "579820563933",
    "appId": st.secrets["firebase"]["firebase_app_id"],
    "databaseURL": st.secrets["firebase"]["firebase_database_url"]
}
