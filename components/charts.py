import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import Counter
import plotly.express as px

def show_market_trend_chart(df, highlight_market=None, context_id="default"):
    if df.empty:
        st.info("Aucune donnée à afficher.")
        return

    df["Date"] = pd.to_datetime(df["Date"])
    df_market = df[df["Type"] == "Marché"]

    if df_market.empty:
        st.warning("Aucune donnée de type 'Marché' à afficher.")
        return

    pivot = df_market.pivot(index="Date", columns="Marché", values="Nombre d'annonces").fillna(0)

    fig = go.Figure()

    for market in pivot.columns:
        is_highlighted = (market == highlight_market)
        fig.add_trace(go.Scatter(
            x=pivot.index,
            y=pivot[market],
            mode='lines',
            name=market,
            line=dict(
                width=4 if is_highlighted else 1,
                color='crimson' if is_highlighted else None,
                dash='solid' if is_highlighted else 'dot'
            ),
            opacity=1.0 if is_highlighted else 0.5
        ))

    fig.update_layout(
        title="Évolution des annonces par marché dans le temps",
        xaxis_title="Date",
        yaxis_title="Nombre d'annonces",
        legend_title="Marché",
        template="plotly_white",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True, key=f"trend_chart_{context_id}_{highlight_market or 'default'}")

def plot_skills_tech_chart(data, title="", context_id="default"):
    counter = Counter(data)
    sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    skills, counts = zip(*sorted_items)

    fig = px.bar(
        x=skills,
        y=counts,
        labels={'x': 'Compétences / Technologies', 'y': 'Fréquence'},
        title=title
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True, key=f"skills_chart_{context_id}_{title or 'no_title'}")

def pie_rythms_chart(data, title="", context_id="default"):
    counter = Counter(data)
    sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    rythms, counts = zip(*sorted_items)

    fig = px.pie(
        values=counts,
        names=rythms,
        title=title
    )
    st.plotly_chart(fig, use_container_width=True, key=f"pie_chart_{context_id}_{title or 'no_title'}")