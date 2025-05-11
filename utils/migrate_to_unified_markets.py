import pandas as pd
import os

MARKET_ANALYSIS_FILE = "data/market_analysis.csv"
OFFERS_FILE = "data/offers.csv"
UNIFIED_FILE = "data/markets.csv"

def migrate():
    unified_rows = []

    # Charger les données de l'analyse des marchés
    if os.path.exists(MARKET_ANALYSIS_FILE):
        market_df = pd.read_csv(MARKET_ANALYSIS_FILE)
        for _, row in market_df.iterrows():
            unified_rows.append({
                "Date": row["Date"],
                "Marché": row["Marché"],
                "Nombre d'annonces": row["Nombre d'annonces"],
                "Tendance": row.get("Tendance", ""),
                # Offres
                "Titre": "",
                "Intitulé": "",
                "TJM": "",
                "Séniorité": "",
                "Technos principales": "",
                "Technos secondaires": "",
                "Compétences principales": "",
                "Compétences secondaires": "",
                "Secteur": "",
                "Localisation": "",
                "Rythme": "",
                "Entreprise": "",
                "Contact": "",
                "Lien": ""
            })

    # Charger les données des offres
    if os.path.exists(OFFERS_FILE):
        offers_df = pd.read_csv(OFFERS_FILE)
        for _, row in offers_df.iterrows():
            unified_rows.append({
                "Date": "",  # Inconnu pour une offre
                "Marché": row["Marché"],
                "Nombre d'annonces": "",
                "Tendance": "",
                "Titre": row.get("Titre", ""),
                "Intitulé": row.get("Intitulé", ""),
                "TJM": row.get("TJM", ""),
                "Séniorité": row.get("Séniorité", ""),
                "Technos principales": row.get("Technos principales", ""),
                "Technos secondaires": row.get("Technos secondaires", ""),
                "Compétences principales": row.get("Compétences principales", ""),
                "Compétences secondaires": row.get("Compétences secondaires", ""),
                "Secteur": row.get("Secteur", ""),
                "Localisation": row.get("Localisation", ""),
                "Rythme": row.get("Rythme", ""),
                "Entreprise": row.get("Entreprise", ""),
                "Contact": row.get("Contact", ""),
                "Lien": row.get("Lien", "")
            })

    # Sauvegarder dans le fichier unifié
    unified_df = pd.DataFrame(unified_rows)
    unified_df.to_csv(UNIFIED_FILE, index=False)
    print(f"✅ Migration terminée : {len(unified_df)} lignes écrites dans {UNIFIED_FILE}")

if __name__ == "__main__":
    migrate()
