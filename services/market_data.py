import pandas as pd
from config.settings import MARKET_OFFERS_FILE

# Charger toutes les données depuis le fichier CSV
def load_market_analysis():
    if MARKET_OFFERS_FILE.exists():
        df = pd.read_csv(MARKET_OFFERS_FILE)

        # Filtrer uniquement les lignes de type "Marché"
        market_data = df[df["Type"] == "Marché"]
        return market_data
    else:
        # Retourner un DataFrame vide avec les colonnes du CSV complet
        return pd.DataFrame(columns=[
            "Date", "Type", "Marché", "Nombre d'annonces", "Tendance", "Titre",
            "Intitulé", "TJM", "Séniorité", "Technos principales", "Technos secondaires",
            "Compétences principales", "Compétences secondaires", "Secteur", "Localisation",
            "Rythme", "Entreprise", "Contact", "Lien"
        ])

# Sauvegarder une nouvelle entrée d'analyse de marché
def save_market_analysis(market_data):
    df = pd.DataFrame([market_data])

    if MARKET_OFFERS_FILE.exists():
        df.to_csv(MARKET_OFFERS_FILE, mode='a', header=False, index=False)
    else:
        # Écrire avec toutes les colonnes, même vides, pour assurer la structure
        full_columns = [
            "Date", "Type", "Marché", "Nombre d'annonces", "Tendance", "Titre",
            "Intitulé", "TJM", "Séniorité", "Technos principales", "Technos secondaires",
            "Compétences principales", "Compétences secondaires", "Secteur", "Localisation",
            "Rythme", "Entreprise", "Contact", "Lien"
        ]
        for col in full_columns:
            if col not in df.columns:
                df[col] = None
        df = df[full_columns]
        df.to_csv(MARKET_OFFERS_FILE, index=False)
