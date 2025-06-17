import streamlit as st
import pandas as pd
from constants.alerts import ERROR_MISSING_TYPE_COLUMN, SUCCESS_FILE_IMPORTED, ERROR_FILE_PROCESSING
from constants.labels import LABEL_UPLOAD_SECTION, BTN_UPLOAD_CSV, BTN_DOWNLOAD_CSV

def files_controls(filepath, label, uploader_key):
    st.sidebar.markdown(f"### {LABEL_UPLOAD_SECTION.format(label=label)}")

    columns_sep = r'\|'

    # Bouton d'upload
    uploaded_file = st.sidebar.file_uploader(
        BTN_UPLOAD_CSV,
        type="csv",
        key=f"{uploader_key}_upload"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, sep=columns_sep, engine="python")
            df.columns = df.columns.str.strip()

            if "Type" not in df.columns:
                st.sidebar.error(ERROR_MISSING_TYPE_COLUMN)
                return

            df.to_csv(filepath, sep="|", index=False)
            st.sidebar.success(SUCCESS_FILE_IMPORTED)
        except Exception as e:
            st.sidebar.error(ERROR_FILE_PROCESSING.format(error=e))

    if filepath.exists():
        with open(filepath, "rb") as f:
            st.sidebar.download_button(
                label=BTN_DOWNLOAD_CSV,
                data=f,
                file_name=filepath.name,
                mime="text/csv",
                key=f"{uploader_key}_download"
            )