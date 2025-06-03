import streamlit as st
import pandas as pd
from services.market_data import load_market_analysis, save_market_analysis
from components.charts import show_market_trend_chart
from utils.filters import filter_dataframe_by_market

def show_market_analysis():
    st.header("Analyse des marchés")

    df_market_analysis = load_market_analysis()
    existing_markets = sorted(df_market_analysis["Marché"].dropna().unique()) if not df_market_analysis.empty else []

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
        notes = st.text_input("Notes")

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
                    "Notes": notes
                }
                save_market_analysis(market_data)
                st.success("✅ Donnée ajoutée avec succès.")
    
    st.subheader("📈 Tendance des marchés")
    markets_trends = df_market_analysis["Marché"].dropna().unique()
    selected_market = filter_dataframe_by_market(df_market_analysis, markets_trends, label="🎯 Sélectionner un marché")
    show_market_trend_chart(df_market_analysis, highlight_market=selected_market, context_id="market_analysis")
    
    st.subheader("📊 Historique des marchés")
    if not df_market_analysis.empty:
        display_columns = ["Date", "Marché", "Nombre d'annonces", "Notes"]
        df_market_analysis["Date"] = pd.to_datetime(df_market_analysis["Date"]).dt.strftime("%d/%m/%Y")
        st.dataframe(df_market_analysis[display_columns])
    else:
        st.info("Aucune donnée d'analyse de marché disponible.")
