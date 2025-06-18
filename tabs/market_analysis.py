import streamlit as st
import pandas as pd
from services.market_analysis.market_data import load_market_analysis, save_market_analysis
from components.charts.trend_chart import trend_chart
from utils.filters import filter_dataframe_by_market
from components.forms.market_form import market_form
from constants.alerts import WARNING_MISSING_MARKET, WARNING_MARKET_ALREADY_EXISTS, SUCCESS_DATA_SAVED, INFO_NO_MARKET_ANALYSIS_DATA
from constants.labels import HEADER_MARKET_ANALYSIS, SECTION_MARKET_TRENDS, SECTION_MARKET_HISTORY, LABEL_SELECT_MARKET, ALL_MARKETS_OPTION, TITLE_MARKET_TREND, X_AXIS_DATE, Y_AXIS_ADS, LEGEND_MARKET
from constants.schema.views import MARKET_DISPLAY_COLUMNS
from constants.schema.columns import COL_MARKET, COL_DATE, COL_TYPE, COL_NUMBER_OF_OFFERS, COL_NOTES
def is_new_entry_unique(df, market, date):
    existing = df[(df[COL_MARKET] == market) & (df[COL_DATE] == str(date))]
    return existing.empty

def show_market_analysis():
    CONTEXT_ID = "market_analysis"

    st.header(HEADER_MARKET_ANALYSIS)

    df_market_analysis = load_market_analysis()
    existing_markets = sorted(df_market_analysis[COL_MARKET].dropna().unique()) if not df_market_analysis.empty else []

    if "clear_form_market" in st.session_state and st.session_state.clear_form_market:
        st.session_state.selected_market = ""
        st.session_state.new_market = ""
        st.session_state.selected_number = 0
        st.session_state.selected_date = None
        st.session_state.notes = ""
        st.session_state.clear_form_market = False
        st.rerun()

    submitted, final_market, date, number, notes = market_form(existing_markets)
    
    if submitted:
        if not final_market:
            st.warning(WARNING_MISSING_MARKET)
        elif not is_new_entry_unique(df_market_analysis, final_market, date):
            st.warning(WARNING_MARKET_ALREADY_EXISTS)
        else:
            market_data = {
                COL_DATE: str(date),
                COL_TYPE: COL_MARKET,
                COL_MARKET: final_market,
                COL_NUMBER_OF_OFFERS: number,
                COL_NOTES: notes
            }
            save_market_analysis(market_data)
            st.success(SUCCESS_DATA_SAVED)
            st.session_state.clear_form_market = True
            st.rerun()

    st.subheader(SECTION_MARKET_TRENDS)
    markets_trends = [ALL_MARKETS_OPTION] + sorted(df_market_analysis[COL_MARKET].dropna().unique())
    selected_market = filter_dataframe_by_market(df_market_analysis, markets_trends, label=LABEL_SELECT_MARKET)
    trend_chart(
        df=df_market_analysis,
        index_col=COL_DATE,
        category_col=COL_MARKET,
        value_col=COL_NUMBER_OF_OFFERS,
        highlight=selected_market,
        title=TITLE_MARKET_TREND,
        x_axis_label=X_AXIS_DATE,
        y_axis_label=Y_AXIS_ADS,
        legend_title=LEGEND_MARKET,
        context_id=CONTEXT_ID
    )

    st.subheader(SECTION_MARKET_HISTORY)

    if not df_market_analysis.empty:
        if selected_market and selected_market != ALL_MARKETS_OPTION:
            df_market_analysis = df_market_analysis[df_market_analysis[COL_MARKET] == selected_market]
        
        display_columns = MARKET_DISPLAY_COLUMNS
        df_market_analysis[COL_DATE] = pd.to_datetime(df_market_analysis[COL_DATE]).dt.strftime("%d/%m/%Y")
        st.dataframe(df_market_analysis[display_columns])
    else:
        st.info(INFO_NO_MARKET_ANALYSIS_DATA)