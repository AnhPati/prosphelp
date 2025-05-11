import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def show_market_trend_chart(df):
    if df.empty:
        st.info("Aucune donnée à afficher.")
        return

    # S'assurer que la colonne Date est bien en datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Filtrer les données de type "Marché"
    df_market = df[df["Type"] == "Marché"]

    if df_market.empty:
        st.warning("Aucune donnée de type 'Marché' à afficher.")
        return

    # Pivot et affichage
    pivot = df_market.pivot(index="Date", columns="Marché", values="Nombre d'annonces").fillna(0)
    st.line_chart(pivot)

def plot_skills_tech_chart(data, title=""):
    # Compter les occurrences des éléments
    counter = Counter(data)
    
    # Trier par fréquence
    sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    skills, counts = zip(*sorted_items)

    # Créer un graphique en bâtons
    plt.figure(figsize=(10, 6))
    plt.bar(skills, counts, color="skyblue")
    plt.xticks(rotation=45, ha='right')
    plt.title(title)
    plt.xlabel("Compétences / Technologies")
    plt.ylabel("Fréquence")
    plt.tight_layout()

    # Afficher le graphique
    st.pyplot(plt)

