import streamlit as st
from services.market_data import load_market_data, save_market_data
from components.charts import show_market_trend_chart

def show_market_analysis():
    st.header("Analyse des marchés")

    df = load_market_data()

    with st.form("market_form"):
        market = st.text_input("Marché (ex: Développeur React)")
        date = st.date_input("Date")
        number = st.number_input("Nombre d'annonces", min_value=0, step=1)
        submitted = st.form_submit_button("Ajouter")

        if submitted and market:
            df.loc[len(df)] = [str(date), market, number]
            save_market_data(df)
            st.success("Donnée ajoutée avec succès.")

    st.subheader("Historique")
    st.dataframe(df)

    st.subheader("Tendances")
    show_market_trend_chart(df)
