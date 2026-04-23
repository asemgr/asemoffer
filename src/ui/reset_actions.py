import streamlit as st

def render_reset_button():
    # Χρησιμοποιούμε το ίδιο κλειδί "btn_reset_v20" για να μη χαθεί το styling
    if st.button("ΚΑΘΑΡΙΣΜΟΣ", key="btn_reset_v20", icon=":material/delete:", use_container_width=True):
        # 1. Αδειάζουμε τη λίστα
        st.session_state.catalog_selection = []
        
        # 2. Αυξάνουμε τον μετρητή για να αλλάξουν τα keys στο sidebar
        if 'reset_counter' not in st.session_state:
            st.session_state.reset_counter = 0
        st.session_state.reset_counter += 1
        
        # 3. Καθαρίζουμε τα παλιά widget keys από τη μνήμη
        for key in list(st.session_state.keys()):
            if key.startswith("cb_"):
                del st.session_state[key]
        
        st.rerun()