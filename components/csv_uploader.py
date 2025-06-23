import streamlit as st
import pandas as pd
from services.storage.firebase_storage_service import upload_csv_to_storage
from constants.alerts import (
    ERROR_MISSING_TYPE_COLUMN,
    SUCCESS_FILE_IMPORTED,
    ERROR_FILE_PROCESSING,
    ERROR_INVALID_COLUMN_COUNT
)
from constants.labels import (
    LABEL_UPLOAD_SECTION,
    BTN_UPLOAD_CSV,
    BTN_DOWNLOAD_CSV
)
from constants.schema.columns import COL_TYPE
from constants.schema.constants import COLUMNS_SEP, EXPECTED_COLUMNS


def csv_uploader(filepath, label, uploader_key, expected_column=COL_TYPE, firebase_path=None):
    st.sidebar.markdown(f"### {LABEL_UPLOAD_SECTION.format(label=label)}")

    # 📤 Upload CSV
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
                on_bad_lines="skip"
            )

            if df.shape[1] != len(EXPECTED_COLUMNS):
                st.sidebar.error(ERROR_INVALID_COLUMN_COUNT.format(
                    dectected=df.shape[1], expected=len(EXPECTED_COLUMNS)))
                return

            if expected_column not in df.columns:
                st.sidebar.error(ERROR_MISSING_TYPE_COLUMN)
                return

            df.columns = df.columns.str.strip()
            df.to_csv(filepath, sep="|", index=False)

            # 🔄 Synchronisation vers Firebase Storage si un chemin est fourni
            if firebase_path:
                upload_csv_to_storage(
                    local_path=filepath,
                    remote_path=firebase_path
                )

            st.sidebar.success(SUCCESS_FILE_IMPORTED)

        except Exception as e:
            st.sidebar.error(ERROR_FILE_PROCESSING.format(error=e))

    # 📥 Download CSV local existant
    if filepath.exists():
        with open(filepath, "rb") as f:
            st.sidebar.download_button(
                label=BTN_DOWNLOAD_CSV,
                data=f,
                file_name=filepath.name,
                mime="text/csv",
                key=f"{uploader_key}_download"
            )