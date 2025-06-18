import streamlit as st
import pandas as pd
from constants.alerts import ERROR_MISSING_TYPE_COLUMN, SUCCESS_FILE_IMPORTED, ERROR_FILE_PROCESSING, ERROR_INVALID_COLUMN_COUNT
from constants.labels import LABEL_UPLOAD_SECTION, BTN_UPLOAD_CSV, BTN_DOWNLOAD_CSV
from constants.schema import COLUMNS_SEP, COL_TYPE, EXPECTED_COLUMNS


def csv_uploader(filepath, label, uploader_key, expected_column=COL_TYPE):
    st.sidebar.markdown(f"### {LABEL_UPLOAD_SECTION.format(label=label)}")

    # Upload CSV
    uploaded_file = st.sidebar.file_uploader(
        BTN_UPLOAD_CSV,
        type="csv",
        key=f"{uploader_key}_upload"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(
                uploaded_file,
                sep=COLUMNS_SEP,
                engine="python",
                quotechar='"',
                encoding="utf-8",
                header=0,
                on_bad_lines="skip"  # tolérant, mais...
            )

            expected_cols = len(EXPECTED_COLUMNS)
            if df.shape[1] != expected_cols:
                st.sidebar.error(ERROR_INVALID_COLUMN_COUNT.format(dectected=df.shape[1], expected=expected_cols))
                return

            if COL_TYPE not in df.columns:
                st.sidebar.error(ERROR_MISSING_TYPE_COLUMN)
                return

            df.columns = df.columns.str.strip()
            df.to_csv(filepath, sep="|", index=False)
            st.sidebar.success(SUCCESS_FILE_IMPORTED)

        except Exception as e:
            st.sidebar.error(ERROR_FILE_PROCESSING.format(error=e))

    # Download CSV (si présent)
    if filepath.exists():
        with open(filepath, "rb") as f:
            st.sidebar.download_button(
                label=BTN_DOWNLOAD_CSV,
                data=f,
                file_name=filepath.name,
                mime="text/csv",
                key=f"{uploader_key}_download"
            )