import streamlit as st
from collections import Counter
import plotly.express as px
from constants.labels import X_AXIS_SKILLS_TECH, Y_AXIS_FREQUENCY

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