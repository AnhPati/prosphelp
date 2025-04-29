import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/market_analysis.csv")

# Charger les données existantes ou créer un tableau vide
if DATA_PATH.exists() and DATA_PATH.stat().st_size > 0:
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame(columns=["Date", "Marché", "Nombre d'annonces"])

st.title("Analyse des marchés de l'emploi 📊")

# Formulaire pour ajouter un relevé
with st.form("add_market_data"):
    st.subheader("Ajouter un relevé quotidien")
    market = st.text_input("Nom du marché (ex: Développeur web)")
    date = st.date_input("Date du relevé")
    number = st.number_input("Nombre d'annonces trouvées", min_value=0, step=1)
    submitted = st.form_submit_button("Enregistrer")

    if submitted:
        new_entry = {"Date": date, "Marché": market, "Nombre d'annonces": number}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        st.success("Relevé enregistré avec succès !")

# Affichage des données
st.subheader("Historique des relevés")
st.dataframe(df)

# Visualisation
st.subheader("Tendances de tous les marchés 📈")

if not df.empty:
    # Pivot pour avoir une colonne par marché
    pivot_df = df.pivot(index="Date", columns="Marché", values="Nombre d'annonces")
    pivot_df = pivot_df.fillna(0)  # Remplir les jours manquants avec 0 (optionnel)

    st.line_chart(pivot_df)
else:
    st.info("Aucune donnée disponible pour l'instant.")