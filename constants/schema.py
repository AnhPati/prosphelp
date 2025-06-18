# constants/schema.py

# Dictionnaire des noms de colonnes (FR par défaut)
COLUMN_NAMES = {
    "DATE": "Date",
    "TYPE": "Type",
    "MARKET": "Marché",
    "NUMBER_OF_OFFERS": "Nombre d'annonces",
    "NOTES": "Notes",
    "TITLE": "Titre",
    "JOB_TITLE": "Intitulé",
    "TJM": "TJM",
    "SENIORITY": "Séniorité",
    "TECH_MAIN": "Technos principales",
    "TECH_SECONDARY": "Technos secondaires",
    "SKILL_MAIN": "Compétences principales",
    "SKILL_SECONDARY": "Compétences secondaires",
    "SECTOR": "Secteur",
    "LOCATION": "Localisation",
    "RHYTHM": "Rythme",
    "COMPANY": "Entreprise",
    "CONTACT": "Contact",
    "LINK": "Lien",
    "SOPHISTICATION": "Sophistication du marché",
    "LEARNING": "Capitalisation de l'apprentissage",
    "RELIABILITY": "Fiabilité"
}

# Liste des colonnes attendues dans l'ordre
EXPECTED_COLUMNS = list(COLUMN_NAMES.values())

# Séparateur de colonnes dans les fichiers d'import/export
COLUMNS_SEP = r"\|"

# --- Colonnes à afficher pour l’analyse des marchés ---
MARKET_COLUMN_KEYS = [
    "DATE", "MARKET", "NUMBER_OF_OFFERS", "NOTES"
]

MARKET_DISPLAY_COLUMNS = [COLUMN_NAMES[key] for key in MARKET_COLUMN_KEYS]

OFFER_COLUMN_KEYS = [
    "DATE", "MARKET", "JOB_TITLE", "TJM", "SENIORITY",
    "TECH_MAIN", "TECH_SECONDARY",
    "SKILL_MAIN", "SKILL_SECONDARY",
    "SECTOR", "LOCATION", "RHYTHM",
    "COMPANY", "CONTACT", "LINK"
]

# Libellés des colonnes à afficher dans les DataFrames d'offres
OFFER_DISPLAY_COLUMNS = [COLUMN_NAMES[key] for key in OFFER_COLUMN_KEYS]

COMPASS_COLUMN_KEYS = [
    "MARKET",
    "SKILL_MAIN",
    "SKILL_SECONDARY",
    "TECH_MAIN",
    "TECH_SECONDARY",
    "TJM",
    "SENIORITY",
    "SECTOR",
    "RHYTHM",
    "LOCATION"
]

COMPASS_DISPLAY_COLUMNS = [COLUMN_NAMES[key] for key in COMPASS_COLUMN_KEYS] + ["latitude", "longitude"]

# (Optionnel) alias pour une utilisation plus explicite ailleurs dans le code
COL_TYPE = COLUMN_NAMES["TYPE"]
COL_DATE = COLUMN_NAMES["DATE"]
COL_MARKET = COLUMN_NAMES["MARKET"]
COL_TITLE = COLUMN_NAMES["TITLE"]
COL_TJM = COLUMN_NAMES["TJM"]
COL_CONTACT = COLUMN_NAMES["CONTACT"]
COL_JOB_TITLE = COLUMN_NAMES["JOB_TITLE"]
COL_TJM = COLUMN_NAMES["TJM"]
COL_SENIORITY = COLUMN_NAMES["SENIORITY"]
COL_TECHS_MAIN = COLUMN_NAMES["TECH_MAIN"]
COL_TECHS_SECONDARY = COLUMN_NAMES["TECH_SECONDARY"]
COL_SKILLS_MAIN = COLUMN_NAMES["SKILL_MAIN"]
COL_SKILLS_SECONDARY = COLUMN_NAMES["SKILL_SECONDARY"]
COL_SECTOR = COLUMN_NAMES["SECTOR"]
COL_LOCATION = COLUMN_NAMES["LOCATION"]
COL_RHYTHM = COLUMN_NAMES["RHYTHM"]
COL_COMPANY = COLUMN_NAMES["COMPANY"]
COL_CONTACT = COLUMN_NAMES["CONTACT"]
COL_LINK = COLUMN_NAMES["LINK"]
COL_SOPHISTICATION = COLUMN_NAMES["SOPHISTICATION"]
COL_RELIABILITY = COLUMN_NAMES["RELIABILITY"]