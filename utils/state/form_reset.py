import streamlit as st

def reset_form_state(prefix: str) -> bool:
    clear_key = f"clear_form_{prefix}"
    if st.session_state.get(clear_key):
        keys_to_reset = [key for key in st.session_state.keys() if key.startswith(prefix)]
        for key in keys_to_reset:
            st.session_state[key] = None if "date" in key else ""
        st.session_state[clear_key] = False
        return True
    return False