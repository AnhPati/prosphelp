import streamlit as st
import pandas as pd
import io
from services.storage.save_manager import save_changes_if_any
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


def csv_uploader(filepath, uploader_key, title=None, expected_column=COL_TYPE,
                 firebase_path=None, inline=False, container=None):
    container = container or st

    # 👉 Titre uniquement si on est en layout vertical (sidebar)
    if not inline and title:
        container.markdown(f"### {LABEL_UPLOAD_SECTION.format(label=title)}")

    # ➕ Layout conditionnel
    if inline:
        col1, col2 = container.columns([1, 1])
        use_with = True
    else:
        col1, col2 = container, container
        use_with = False

    # 📤 Upload CSV avec label visible uniquement si non-inline
    file_uploader_kwargs = {
        "type": "csv",
        "key": f"{uploader_key}_upload"
    }
    if inline:
        file_uploader_kwargs["label"] = "Upload CSV"
        file_uploader_kwargs["label_visibility"] = "collapsed"
    else:
        file_uploader_kwargs["label"] = BTN_UPLOAD_CSV
        file_uploader_kwargs["label_visibility"] = "visible"

    if use_with:
        with col1:
            uploaded_file = container.file_uploader(**file_uploader_kwargs)
    else:
        uploaded_file = col1.file_uploader(**file_uploader_kwargs)

    if uploaded_file is not None:
        container.info(f"✅ File uploaded: {uploaded_file.name}, size: {uploaded_file.size} bytes")

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
        except Exception as e:
            container.error("❌ Error while reading CSV.")
            container.exception(e)
            return

        if df.shape[1] != len(EXPECTED_COLUMNS):
            container.error(ERROR_INVALID_COLUMN_COUNT.format(
                dectected=df.shape[1], expected=len(EXPECTED_COLUMNS)))
            return

        if expected_column not in df.columns:
            container.error(ERROR_MISSING_TYPE_COLUMN)
            return

        df.columns = df.columns.map(str).str.strip()
        df.to_csv(filepath, sep="|", index=False)

        if firebase_path:
            save_changes_if_any(local_path=filepath, remote_path=firebase_path)

        container.success(SUCCESS_FILE_IMPORTED)

    # 📥 Download CSV (Cloud-safe, évite CORS)
    if filepath.exists():
        try:
            df_download = pd.read_csv(filepath, sep="|")
            buffer = io.StringIO()
            df_download.to_csv(buffer, index=False, sep="|")
            buffer.seek(0)

            download_kwargs = {
                "label": f"📥 {BTN_DOWNLOAD_CSV}",
                "data": buffer.getvalue(),
                "file_name": filepath.name,
                "mime": "text/csv",
                "key": f"{uploader_key}_download"
            }

            if use_with:
                with col2:
                    st.markdown("<div style='margin-top: 0.85rem;'>", unsafe_allow_html=True)
                    container.download_button(**download_kwargs)
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                col2.download_button(**download_kwargs)

        except Exception as e:
            container.error("Error during file preparation for download.")
            container.exception(e)