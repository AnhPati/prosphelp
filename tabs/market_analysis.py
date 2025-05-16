import streamlit as st
from services.market_data import load_market_analysis, save_market_analysis
from components.charts import show_market_trend_chart

def show_market_analysis():
    st.header("Analyse des marchés")

    df = load_market_analysis()
    existing_markets = sorted(df["Marché"].dropna().unique()) if not df.empty else []

    # Checkbox, sa valeur est automatiquement stockée dans st.session_state
    use_existing = st.checkbox("Choisir un marché existant", value=True)

    with st.form("market_form"):
        if use_existing:
            market = st.selectbox("Marché existant", options=[""] + existing_markets)
            new_market = None
        else:
            market = None
            new_market = st.text_input("Nouveau marché")

        final_market = new_market.strip() if new_market else (market if market else "")

        date = st.date_input("Date")
        number = st.number_input("Nombre d'annonces", min_value=0, step=1)
        trend = st.text_input("Tendance (ex: en hausse, stable, en baisse)")

        submitted = st.form_submit_button("Ajouter")

        if submitted:
            if not final_market:
                st.warning("⚠️ Merci de spécifier un marché.")
            else:
                market_data = {
                    "Date": str(date),
                    "Type": "Marché",
                    "Marché": final_market,
                    "Nombre d'annonces": number,
                    "Tendance": trend
                }
                save_market_analysis(market_data)
                st.success("✅ Donnée ajoutée avec succès.")

    st.subheader("📊 Historique des marchés")
    if not df.empty:
        display_columns = ["Date", "Marché", "Nombre d'annonces", "Tendance"]
        st.dataframe(df[display_columns])
    else:
        st.info("Aucune donnée d'analyse de marché disponible.")

    st.subheader("📈 Tendances des marchés")
    show_market_trend_chart(df)
