from pathlib import Path

# Chemin vers le dossier "data" et le fichier unique pour les marchés et les offres
DATA_DIR = Path(__file__).parent.parent / "data"
MARKET_OFFERS_FILE = DATA_DIR / "markets.csv"
