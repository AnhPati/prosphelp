/prospection_app
│
├── app.py                            # Point d’entrée de l’app
├── requirements.txt                 # Dépendances du projet
│
├── config/
│   └── settings.py                  # Configs globales (chemins, constantes, etc.)
│
├── data/
│   └── market_analysis.csv          # Données de suivi des marchés
│
├── pages/
│   ├── __init__.py
│   ├── market_analysis.py           # Logique + UI de l’onglet “Analyse des marchés”
│   └── offer_dissection.py          # Logique + UI de l’onglet “Dissection des offres”
│
├── components/
│   └── charts.py                    # Composants réutilisables (ex: graphiques)
│
├── services/
│   └── market_data.py               # Fonctions de lecture/écriture CSV
│
└── utils/
    └── helpers.py                   # Fonctions utilitaires diverses