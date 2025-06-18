import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from constants.alerts import INFO_NO_DATA_TO_DISPLAY, INFO_NO_MARKET_DATA_AVAILABLE
from constants.labels import TITLE_MARKET_TREND, X_AXIS_DATE, Y_AXIS_ADS, LEGEND_MARKET
from constants.schema import COL_MARKET, COL_DATE, COL_TYPE

def show_market_trend_chart(df, highlight_market=None, context_id="default"):
    if df.empty:
        st.info(INFO_NO_DATA_TO_DISPLAY)
        return

    df[COL_DATE] = pd.to_datetime(df[COL_DATE])
    df_market = df[df[COL_TYPE] == COL_MARKET]

    if df_market.empty:
        st.warning(INFO_NO_MARKET_DATA_AVAILABLE)
        return

    pivot = df_market.pivot(index=COL_DATE, columns=COL_MARKET, values="Nombre d'annonces").fillna(0)

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