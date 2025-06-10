# components/interactive_numeric_display.py

import streamlit as st
import pandas as pd
import numpy as np # Pour np.argmin

def display_numeric_range_selector(df: pd.DataFrame, column_name: str, title: str, unit: str = ""):
    """
    Affiche un sélecteur de plage interactif (slider) pour une colonne numérique,
    permettant de voir le nombre d'entrées correspondant à la valeur sélectionnée.

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données.
        column_name (str): Le nom de la colonne numérique à analyser.
        title (str): Le titre à afficher au-dessus du composant (ex: "TJM", "Niveau de Seniorité").
        unit (str): L'unité à afficher après la valeur (ex: "€", "ans", "jour(s)").
    """
    st.subheader(title)

    # Convertir la colonne en numérique, en gérant les erreurs
    numeric_values = pd.to_numeric(df[column_name], errors='coerce').dropna()

    if numeric_values.empty:
        st.info(f"ℹ️ Aucune donnée numérique valide disponible pour '{column_name}'.")
        return

    min_val = int(numeric_values.min())
    max_val = int(numeric_values.max())
    avg_val = numeric_values.mean()

    st.markdown(f"**Moyenne :** {avg_val:,.0f}{unit}")
    st.markdown(f"**Fourchette :** {min_val:,.0f}{unit} - {max_val:,.0f}{unit}")

    # Récupérer toutes les valeurs uniques et triées
    unique_vals = sorted(numeric_values.unique())

    if unique_vals:
        # Trouver l'index de la valeur la plus proche de la moyenne dans les valeurs uniques
        closest_avg_val_idx = (np.abs(np.array(unique_vals) - avg_val)).argmin()
        default_val = unique_vals[closest_avg_val_idx]

        # Créer le select_slider avec les valeurs uniques comme options
        selected_val = st.select_slider(
            f"Explorez les données par valeur :",
            options=unique_vals,
            value=default_val,
            format_func=lambda x: f"{x:,.0f}{unit}"
        )

        # Calcul du nombre d'entrées pour la valeur sélectionnée
        count_for_selected_val = numeric_values[numeric_values == selected_val].count()
        st.markdown(f"**Nombre d'entrées à {selected_val:,.0f}{unit} :** {count_for_selected_val}")
    else:
        st.info(f"ℹ️ Aucune valeur unique disponible pour l'exploration de '{column_name}'.")