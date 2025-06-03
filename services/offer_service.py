import pandas as pd
from config.settings import MARKET_OFFERS_FILE

def load_offers():
    expected_columns = [
        "Date", "Type", "Marché", "Nombre d'annonces", "Tendance", "Titre",
        "Intitulé", "TJM", "Séniorité", "Technos principales", "Technos secondaires",
        "Compétences principales", "Compétences secondaires", "Secteur", "Localisation",
        "Rythme", "Entreprise", "Contact", "Lien", "Sophistication du marché", "Capitalisation de l'apprentissage", "Fiabilité"
    ]
    columns_sep = r'\|'
    
    if not MARKET_OFFERS_FILE.exists():
        return pd.DataFrame(columns=expected_columns)
    
    try:
        try:
            df = pd.read_csv(
                MARKET_OFFERS_FILE,
                sep=columns_sep,
                quotechar=None,
                encoding='utf-8',
                engine='python'
            )
        except pd.errors.ParserError:
            with open(MARKET_OFFERS_FILE, 'r', encoding='utf-8') as f:
                lines = [line.strip().split('|') for line in f.readlines()]
            
            cleaned_lines = []
            for line in lines:
                if len(line) == len(expected_columns):
                    cleaned_lines.append(line)

                elif len(line) > 0:
                    adjusted_line = line[:len(expected_columns)]
                    adjusted_line += [''] * (len(expected_columns) - len(adjusted_line))
                    cleaned_lines.append(adjusted_line)
            
            df = pd.DataFrame(cleaned_lines[1:], columns=cleaned_lines[0] if cleaned_lines else expected_columns)
        
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None
        
        offer_data = df[df["Type"] == "Offre"].copy()
        offer_data = offer_data.where(pd.notnull(offer_data), None)
        
        return offer_data
    
    except Exception as e:
        print(f"Erreur critique lors du chargement des offres : {str(e)}")
        
        return pd.DataFrame(columns=expected_columns)

def save_offer_data(offer_data):
    columns_sep = "|"
    expected_columns = [
        "Date", "Type", "Marché", "Nombre d'annonces", "Tendance", "Titre",
        "Intitulé", "TJM", "Séniorité", "Technos principales", "Technos secondaires",
        "Compétences principales", "Compétences secondaires", "Secteur", "Localisation",
        "Rythme", "Entreprise", "Contact", "Lien", "Sophistication du marché", "Capitalisation de l'apprentissage", "Fiabilité"
    ]
    
    if isinstance(offer_data, dict):
        df = pd.DataFrame([offer_data])
    else:
        df = offer_data.copy()
    
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    
    df = df[expected_columns]
    
    try:
        if MARKET_OFFERS_FILE.exists():
            existing_columns = pd.read_csv(MARKET_OFFERS_FILE, sep=columns_sep, nrows=0).columns
            if not set(df.columns).issubset(existing_columns):
                raise ValueError("Mismatch entre les colonnes du DataFrame et du fichier existant")
            
            df.to_csv(
                MARKET_OFFERS_FILE,
                sep=columns_sep,
                mode='a',
                header=False,
                index=False,
                quoting=0
            )
        else:
            df.to_csv(
                MARKET_OFFERS_FILE,
                sep=columns_sep,
                index=False,
                quoting=0
            )

        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {str(e)}")

        return False

def get_existing_markets_from_offers():
    try:
        df = load_offers()

        if not df.empty and "Marché" in df.columns:
            return sorted(df["Marché"].dropna().astype(str).unique())
        
        return []
    
    except Exception as e:
        print(f"Erreur lors de la récupération des marchés : {str(e)}")

        return []