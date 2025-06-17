import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import Counter
import plotly.express as px

from constants.alerts import NO_DATA_AVAILABLE, NO_MARKET_DATA_AVAILABLE
from constants.labels import TITLE_MARKET_TREND, X_AXIS_DATE, Y_AXIS_ADS, LEGEND_MARKET, X_AXIS_SKILLS_TECH, Y_AXIS_FREQUENCY

def show_market_trend_chart(df, highlight_market=None, context_id="default"):
    if df.empty:
        st.info(NO_DATA_AVAILABLE)
        return

    df["Date"] = pd.to_datetime(df["Date"])
    df_market = df[df["Type"] == "Marché"]

    if df_market.empty:
        st.warning(NO_MARKET_DATA_AVAILABLE)
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
        title=TITLE_MARKET_TREND,
        xaxis_title=X_AXIS_DATE,
        yaxis_title=Y_AXIS_ADS,
        legend_title=LEGEND_MARKET,
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
        labels={'x': X_AXIS_SKILLS_TECH, 'y': Y_AXIS_FREQUENCY},
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