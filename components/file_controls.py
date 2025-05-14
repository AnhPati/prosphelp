import streamlit as st
import pandas as pd

def files_controls(filepath, label, uploader_key):
    st.sidebar.markdown(f"### 📁 {label}")

    columns_sep = r'\|'

    # Bouton d'upload
    uploaded_file = st.sidebar.file_uploader(
        "🔼 Charger un CSV",
        type="csv",
        key=f"{uploader_key}_upload"
    )

    if uploaded_file is not None:
        try:
            # Lecture du CSV avec séparateur pipe, moteur Python
            df = pd.read_csv(uploaded_file, sep=columns_sep, engine="python")

            # Nettoyage des noms de colonnes
            df.columns = df.columns.str.strip()

            # Vérification qu'une colonne clé existe (ex. "Type")
            if "Type" not in df.columns:
                st.sidebar.error("❌ Colonne 'Type' introuvable. Le fichier a-t-il bien le bon séparateur ?")
                return

            # Écriture du fichier sur disque
            df.to_csv(filepath, sep="|", index=False)
            st.sidebar.success("✅ Fichier importé avec succès.")
        except Exception as e:
            st.sidebar.error(f"❌ Erreur lors du traitement du fichier : {e}")

    # Bouton de téléchargement
    if filepath.exists():
        with open(filepath, "rb") as f:
            st.sidebar.download_button(
                label="💾 Télécharger le CSV",
                data=f,
                file_name=filepath.name,
                mime="text/csv",
                key=f"{uploader_key}_download"
            )
