import pandas as pd
from config.settings import MARKET_OFFERS_FILE
from utils.helpers import fallback_read_csv

EXPECTED_COLUMNS = [
    "Date", "Type", "Marché", "Nombre d'annonces", "Notes", "Titre",
    "Intitulé", "TJM", "Séniorité", "Technos principales", "Technos secondaires",
    "Compétences principales", "Compétences secondaires", "Secteur", "Localisation",
    "Rythme", "Entreprise", "Contact", "Lien", "Sophistication du marché", "Capitalisation de l'apprentissage", "Fiabilité"
]
COLUMNS_SEP = r'\|'


def load_market_analysis():
    if not MARKET_OFFERS_FILE.exists():
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    try:
        df = pd.read_csv(
            MARKET_OFFERS_FILE,
            sep=COLUMNS_SEP,
            quotechar=None,
            encoding='utf-8',
            header=0,
            engine='python'
        )
    except pd.errors.ParserError:
        df = fallback_read_csv(MARKET_OFFERS_FILE, EXPECTED_COLUMNS)

    except Exception as e:
        print(f"Erreur inattendue lors du chargement des données de marché : {str(e)}")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    return df[df["Type"] == "Marché"].copy()


def save_market_analysis(market_data):
    df = pd.DataFrame([market_data])
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    df = df[EXPECTED_COLUMNS]

    try:
        df.to_csv(
            MARKET_OFFERS_FILE,
            sep="|",
            mode='a' if MARKET_OFFERS_FILE.exists() else 'w',
            header=not MARKET_OFFERS_FILE.exists(),
            index=False,
            encoding='utf-8',
            quoting=0
        )
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données de marché : {str(e)}")
        return False