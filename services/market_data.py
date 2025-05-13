import pandas as pd
from config.settings import MARKET_OFFERS_FILE

def load_market_analysis():
    expected_columns = [
        "Date", "Type", "Marché", "Nombre d'annonces", "Tendance", "Titre",
        "Intitulé", "TJM", "Séniorité", "Technos principales", "Technos secondaires",
        "Compétences principales", "Compétences secondaires", "Secteur", "Localisation",
        "Rythme", "Entreprise", "Contact", "Lien"
    ]
    columns_sep = r'\|'
    
    if not MARKET_OFFERS_FILE.exists():
        return pd.DataFrame(columns=expected_columns)
    
    try:
        df = pd.read_csv(
            MARKET_OFFERS_FILE,
            sep=columns_sep,
            quotechar=None,
            encoding='utf-8',
            header=0,
            engine='python'
        )

        df = df.where(pd.notnull(df), None)
        market_data = df[df["Type"] == "Marché"].copy()

        return market_data
        
    except pd.errors.ParserError as e:
        print(f"Erreur de parsing détectée : {str(e)}")
        print("Veuillez vérifier le format du fichier CSV.")

        return pd.DataFrame(columns=expected_columns)
    
    except Exception as e:
        print(f"Erreur inattendue : {str(e)}")

        return pd.DataFrame(columns=expected_columns)

def save_market_analysis(market_data):
    expected_columns = [
        "Date", "Type", "Marché", "Nombre d'annonces", "Tendance", "Titre",
        "Intitulé", "TJM", "Séniorité", "Technos principales", "Technos secondaires",
        "Compétences principales", "Compétences secondaires", "Secteur", "Localisation",
        "Rythme", "Entreprise", "Contact", "Lien"
    ]
    columns_sep = "|"
    
    df = pd.DataFrame([market_data])
    
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    
    df = df[expected_columns]
    
    try:
        df.to_csv(
            MARKET_OFFERS_FILE,
            sep=columns_sep,
            mode="a" if MARKET_OFFERS_FILE.exists() else "w",
            header=not MARKET_OFFERS_FILE.exists(),
            index=False,
            encoding='utf-8',
            quoting=0
        )

        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {str(e)}")

        return False