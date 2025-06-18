/prospection_app
│
├── app.py                          # Point d’entrée de l’app
├── requirements.txt                # Dépendances du projet
│
├── config/
│   └── settings.py             # Configs globales (chemins, constantes, etc.)
│
├── constants/
│   ├── alerts.py
│   ├── texts.py
│   ├── labels.py
│   schema/
|    ├── __init__.py
|    ├── columns.py         # Alias et noms de colonnes
|    ├── views.py           # Colonnes affichées selon les vues (offres, compass, etc.)
|    ├── constants.py       # Constantes techniques comme le séparateur
|    └── forms.py           # Champs pour les formulaires
|
├── data/
│   └── markets.csv             # Données de l'utilisateur
│
├── doc/
│   ├── design.svg                      # Palette de couleurs de l'application.
│   ├── folders-roles.png               # @TODO : A supprimer.
│   └── structure.md
│
├── tabs/
│   ├── __init__.py
│   ├── compass.py                   # Logique + UI de l’onglet “Boussole”
│   ├── home.py                      # Logique + UI de l’onglet “Accueil”
│   ├── market_analysis.py           # Logique + UI de l’onglet “Analyse des marchés”
│   └── offer_dissection.py          # Logique + UI de l’onglet “Dissection des offres”
│
├── components/
│   ├── charts/
│   |   ├── pie_chart.py
│   |   ├── trend_chart.py
│   |   └── bar_chart.py
|   ├── forms/
|   |   ├── __init__.py
|   |   ├── offer_form.py            # Formulaire d'ajout d'offre (offre/contact)
|   |   ├── market_form.py           # Formulaire d'ajout de tendance de marché
|   |   └── config/
|   |       ├── offer_inputs.py      # Configuration dynamique du formulaire d'offre
|   |       └── market_inputs.py     # Configuration dynamique du formulaire de marché
|   ├── maps/
|   |   ├── map_from_dataframe.py
│   |   └── offers_map.py
│   ├── numeric_range_selector.py               # @TODO : Renommer le composant.
|   └── csv_uploader.py
|
├── services/
|   ├── markets_analysis/
│   |   ├── load_markets_analysis.py             # @TODO : Extraire les alertes et les textes. Revoir l'implémentation.
│   |   └── save_markets_analysis.py             # @TODO : Extraire les alertes et les textes. Revoir l'implémentation.
|   ├── offers/
│   |   ├── load_offers.py                                  # @TODO : Extraire les alertes et les textes. Revoir l'implémentation.
│   |   ├── save_offers.py                                  # @TODO : Extraire les alertes et les textes. Revoir l'implémentation.
│   |   └── get_existing_markets_from_offers.py             # @TODO : Déplacer dans components/alerts/. Renommer le fichier.
│   └── mapping/
|       ├── client.py               # Appels à l'API Nominatim
|       └── processor.py            # Enrichit un DataFrame avec des coordonnées
│
└── utils/
    ├── filters/
    |   └── filter_dataframe_by_market.py               # @TODO : Extraire le contexte du filtre.
    └── helpers.py              # Fonctions utilitaires diverses