import pandas as pd
from pathlib import Path

# Répertoire contenant les données
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OFFERS_FILE = DATA_DIR / "offers.csv"

def load_offers():
    # Charger le fichier CSV des offres (y compris les marchés)
    if OFFERS_FILE.exists():
        return pd.read_csv(OFFERS_FILE)
    return pd.DataFrame()  # Retourner un DataFrame vide si le fichier n'existe pas

def save_offer_data(df):
    # Sauvegarder les données dans le fichier CSV
    df.to_csv(OFFERS_FILE, mode='a', header=not OFFERS_FILE.exists(), index=False)

def get_existing_markets_from_offers():
    # Récupérer la liste des marchés existants
    df = load_offers()
    if "Marché" in df.columns:
        return sorted(df["Marché"].dropna().unique())
    return []
