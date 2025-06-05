import streamlit as st
import pandas as pd
from services.market_data import load_market_analysis, save_market_analysis
from components.charts import show_market_trend_chart
from utils.filters import filter_dataframe_by_market

def is_new_entry_unique(df, market, date):
    existing = df[(df["Marché"] == market) & (df["Date"] == str(date))]
    return existing.empty

def show_market_analysis():
    st.header("Analyse des marchés")

    df_market_analysis = load_market_analysis()
    existing_markets = sorted(df_market_analysis["Marché"].dropna().unique()) if not df_market_analysis.empty else []

    # Nettoyer les champs du formulaire si nécessaire
    if "clear_form_market" in st.session_state and st.session_state.clear_form_market:
        st.session_state.selected_market = ""
        st.session_state.new_market = ""
        st.session_state.selected_number = 0
        st.session_state.selected_date = None
        st.session_state.notes = ""
        st.session_state.clear_form_market = False
        st.rerun()

    # Checkbox pour choisir un marché existant ou en saisir un nouveau
    use_existing = st.checkbox("Choisir un marché existant", value=True)

    with st.form("market_form"):
        if use_existing:
            market = st.selectbox("Marché existant", options=[""] + existing_markets, key="selected_market")
            new_market = None
        else:
            market = None
            new_market = st.text_input("Nouveau marché", key="new_market")

        final_market = new_market.strip() if new_market else (market if market else "")

        date = st.date_input("Date", key="selected_date", format="DD/MM/YYYY")
        number = st.number_input("Nombre d'annonces", min_value=0, step=1, key="selected_number")
        notes = st.text_input("Notes", key="notes")

        submitted = st.form_submit_button("Ajouter")

        if submitted:
            if not final_market:
                st.warning("⚠️ Merci de spécifier un marché.")
            elif not is_new_entry_unique(df_market_analysis, final_market, date):
                st.warning("⚠️ Une entrée pour ce marché à cette date existe déjà.")
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
                st.session_state.clear_form_market = True
                st.rerun()

    st.subheader("📈 Tendance des marchés")
    markets_trends = ["Tous"] + sorted(df_market_analysis["Marché"].dropna().unique())
    selected_market = filter_dataframe_by_market(df_market_analysis, markets_trends, label="🎯 Sélectionner un marché")
    show_market_trend_chart(df_market_analysis, highlight_market=selected_market, context_id="market_analysis")

    st.subheader("📊 Historique des marchés")

    if not df_market_analysis.empty:
        if selected_market and selected_market != "Tous":
            df_market_analysis = df_market_analysis[df_market_analysis["Marché"] == selected_market]
        
        display_columns = ["Date", "Marché", "Nombre d'annonces", "Notes"]
        df_market_analysis["Date"] = pd.to_datetime(df_market_analysis["Date"]).dt.strftime("%d/%m/%Y")
        st.dataframe(df_market_analysis[display_columns])
    else:
        st.info("Aucune donnée d'analyse de marché disponible.")