import streamlit as st
from collections import Counter
import plotly.express as px

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