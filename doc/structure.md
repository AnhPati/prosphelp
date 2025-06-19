/job_compass
│
├── app.py                          # Point d’entrée de l’app
├── requirements.txt                # Dépendances du projet
│
├── config/
│   └── settings.py                 # Configs globales (chemins, constantes, etc.)
│
├── constants/
│   ├── alerts.py                   # Messages utilisateur : erreurs, infos, succès
│   ├── texts.py                    # Textes d’introduction et de documentation
│   ├── labels.py                   # Libellés pour l’UI : champs, boutons, sections
│   └── schema/
│       ├── __init__.py
│       ├── columns.py              # Alias et noms de colonnes utilisés en interne
│       ├── views.py                # Colonnes affichées par vue (offres, compass, etc.)
│       ├── constants.py            # Constantes techniques : séparateur CSV, etc.
│       └── forms.py                # Champs et configs dynamiques des formulaires
│
├── data/
│   └── markets.csv                 # Données locales de l’utilisateur
│
├── doc/
│   ├── design.svg                  # Palette de couleurs de l'application
│   ├── folders-roles.png           # @TODO : À supprimer si plus utilisé
│   └── structure.md                # Ce fichier décrivant l’architecture du projet
│
├── tabs/
│   ├── __init__.py
│   ├── compass.py                  # Logique + UI de l’onglet “Boussole”
│   ├── home.py                     # Logique + UI de l’onglet “Accueil”
│   ├── market_analysis.py          # Logique + UI de l’onglet “Analyse des marchés”
│   └── offer_dissection.py         # Logique + UI de l’onglet “Dissection des offres”
│
├── components/
│   ├── charts/
│   │   ├── pie_chart.py            # Diagrammes circulaires
│   │   ├── trend_chart.py          # Graphiques temporels
│   │   └── bar_chart.py            # Histogrammes
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── offer_form.py           # Formulaire pour offres ou contacts
│   │   ├── market_form.py          # Formulaire pour tendances de marché
│   │   └── config/
│   │       ├── offer_inputs.py     # Configuration dynamique du formulaire d'offre
│   │       └── market_inputs.py    # Configuration dynamique du formulaire de marché
│   ├── maps/
│   │   ├── map_from_dataframe.py   # Affichage générique d'une carte
│   │   ├── offers_map.py           # Carte dédiée aux offres géocodées
│   │   └── geocoding_feedback.py   # Composant UI de feedback pendant géocodage
│   ├── numeric_range_selector.py   # Composant pour explorer une valeur numérique
│   └── csv_uploader.py             # Composant pour uploader des fichiers CSV
│
├── services/
│   ├── storage/
│   │   ├── read_market_file.py             # Lecture du fichier `markets.csv`
│   │   └── append_to_market_file.py        # Ajout d’une ligne dans `markets.csv`
│   ├── markets_analysis/
│   │   ├── load_markets_analysis.py        # Chargement des tendances de marché
│   │   └── save_markets_analysis.py        # Sauvegarde des données de marché
│   ├── offers/
│   │   ├── load_offers.py                  # Chargement des offres
│   │   ├── save_offers.py                  # Sauvegarde d’une offre ou d’un contact
│   │   └── get_existing_markets_from_offers.py # Récupération des marchés existants
│   └── mapping/
│       ├── cache/
│       │   └── geocoding_cache.py          # Gestion du cache local de géocodage
│       ├── client.py                       # Appels à l’API Nominatim
│       └── processor.py                    # Enrichissement de DataFrame avec coordonnées
│
└── utils/
    ├── helpers.py                          # Fonctions utilitaires diverses
    ├── filters.py                          # Fonctions de filtrage et de sélection de marché
    ├── validation.py                       # Vérifications de règles métier (unicité, etc.)
    └── state/
        └── form_reset.py                   # Réinitialisation de formulaires dans session_state
