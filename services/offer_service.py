import pandas as pd
from config.settings import MARKET_OFFERS_FILE

def load_offers():
    # Charger le fichier CSV des offres (y compris les marchés)
    if MARKET_OFFERS_FILE.exists():
        df = pd.read_csv(MARKET_OFFERS_FILE)

        # Filtrer uniquement les lignes de type "Offre"
        offer_data = df[df["Type"] == "Offre"]
        return offer_data
    else:
        # Retourner un DataFrame vide avec les colonnes du CSV complet
        return pd.DataFrame(columns=[
            "Date", "Type", "Marché", "Nombre d'annonces", "Tendance", "Titre",
            "Intitulé", "TJM", "Séniorité", "Technos principales", "Technos secondaires",
            "Compétences principales", "Compétences secondaires", "Secteur", "Localisation",
            "Rythme", "Entreprise", "Contact", "Lien"
        ])

def save_offer_data(df):
    # Sauvegarder les données dans le fichier CSV
    df.to_csv(MARKET_OFFERS_FILE, mode='a', header=not MARKET_OFFERS_FILE.exists(), index=False)

def get_existing_markets_from_offers():
    # Récupérer la liste des marchés existants
    df = load_offers()
    if "Marché" in df.columns:
        return sorted(df["Marché"].dropna().unique())
    return []
