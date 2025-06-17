import streamlit as st
import pandas as pd
import numpy as np
from constants.alerts import INFO_NO_NUMERIC_DATA, INFO_NO_UNIQUE_VALUES
from constants.labels import SLIDER_EXPLORE_LABEL, LABEL_AVERAGE, LABEL_RANGE, LABEL_COUNT_FOR_SELECTED

def display_numeric_range_selector(df: pd.DataFrame, column_name: str, title: str, unit: str = ""):
    st.subheader(title)

    numeric_values = pd.to_numeric(df[column_name], errors='coerce').dropna()

    if numeric_values.empty:
        st.info(INFO_NO_NUMERIC_DATA.format(column_name=column_name))
        return

    min_val = int(numeric_values.min())
    max_val = int(numeric_values.max())
    avg_val = numeric_values.mean()

    st.markdown(LABEL_AVERAGE.format(avg=f"{avg_val:,.0f}", unit=unit))
    st.markdown(LABEL_RANGE.format(min=f"{min_val:,.0f}", max=f"{max_val:,.0f}", unit=unit))

    unique_vals = sorted(numeric_values.unique())

    if unique_vals:
        closest_avg_val_idx = (np.abs(np.array(unique_vals) - avg_val)).argmin()
        default_val = unique_vals[closest_avg_val_idx]

        selected_val = st.select_slider(
            SLIDER_EXPLORE_LABEL,
            options=unique_vals,
            value=default_val,
            format_func=lambda x: f"{x:,.0f}{unit}"
        )

        count_for_selected_val = numeric_values[numeric_values == selected_val].count()
        st.markdown(LABEL_COUNT_FOR_SELECTED.format(
            value=f"{selected_val:,.0f}",
            unit=unit,
            count=count_for_selected_val
        ))
    else:
        st.info(INFO_NO_UNIQUE_VALUES.format(column_name=column_name))
