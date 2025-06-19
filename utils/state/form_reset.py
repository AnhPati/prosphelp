import streamlit as st

def reset_form_state(prefix: str) -> bool:
    clear_key = f"clear_form_{prefix}"
    if st.session_state.get(clear_key):
        keys_to_reset = [k for k in st.session_state.keys() if k.startswith(prefix)]
        for k in keys_to_reset:
            st.session_state[k] = None if "date" in k else ""
        st.session_state[clear_key] = False
        return True
    return False