import streamlit as st
import pandas as pd
from services.market_analysis.load_markets_analysis import load_markets_analysis
from services.market_analysis.save_markets_analysis import save_markets_analysis
from components.charts.trend_chart import trend_chart
from utils.filters import select_market_filter, filter_by_market_selection
from utils.state.form_reset import reset_form_state
from utils.validation import is_entry_unique
from components.forms.market_form import market_form
from constants.alerts import WARNING_MISSING_MARKET, WARNING_MARKET_ALREADY_EXISTS, SUCCESS_DATA_SAVED, INFO_NO_MARKET_ANALYSIS_DATA
from constants.labels import HEADER_MARKET_ANALYSIS, SECTION_MARKET_TRENDS, SECTION_MARKET_HISTORY, LABEL_SELECT_MARKET, ALL_MARKETS_OPTION, TITLE_MARKET_TREND, X_AXIS_DATE, Y_AXIS_ADS, LEGEND_MARKET
from constants.schema.views import MARKET_DISPLAY_COLUMNS
from constants.schema.columns import COL_MARKET, COL_DATE, COL_TYPE, COL_NUMBER_OF_OFFERS, COL_NOTES

def render_market_analysis():
    CONTEXT_ID = "market_analysis"
    st.header(HEADER_MARKET_ANALYSIS)

    market_df = load_markets_analysis()
    existing_markets = sorted(market_df[COL_MARKET].dropna().unique()) if not market_df.empty else []

    reset_form_state("market")

    submitted, final_market, date, number, notes = market_form(existing_markets)

    if submitted:
        if not final_market:
            st.warning(WARNING_MISSING_MARKET)
        elif not is_entry_unique(market_df, COL_MARKET, final_market, COL_DATE, date):
            st.warning(WARNING_MARKET_ALREADY_EXISTS)
        else:
            new_data = {
                COL_DATE: str(date),
                COL_TYPE: COL_MARKET,
                COL_MARKET: final_market,
                COL_NUMBER_OF_OFFERS: number,
                COL_NOTES: notes,
            }
            save_markets_analysis(new_data)
            st.success(SUCCESS_DATA_SAVED)
            st.session_state.clear_form_market = True
            st.rerun()

    st.subheader(SECTION_MARKET_TRENDS)
    available_markets = [ALL_MARKETS_OPTION] + sorted(market_df[COL_MARKET].dropna().unique())
    selected_market = select_market_filter(market_df, available_markets, label=LABEL_SELECT_MARKET)
    filtered_market_df = filter_by_market_selection(market_df, selected_market)

    trend_chart(
        df=market_df,
        index_col=COL_DATE,
        category_col=COL_MARKET,
        value_col=COL_NUMBER_OF_OFFERS,
        highlight=selected_market,
        title=TITLE_MARKET_TREND,
        x_axis_label=X_AXIS_DATE,
        y_axis_label=Y_AXIS_ADS,
        legend_title=LEGEND_MARKET,
        context_id=CONTEXT_ID,
    )

    st.subheader(SECTION_MARKET_HISTORY)
    if not filtered_market_df.empty:
        filtered_market_df[COL_DATE] = pd.to_datetime(filtered_market_df[COL_DATE]).dt.strftime("%d/%m/%Y")
        st.dataframe(filtered_market_df[MARKET_DISPLAY_COLUMNS])
    else:
        st.info(INFO_NO_MARKET_ANALYSIS_DATA)