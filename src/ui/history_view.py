import streamlit as st
import pandas as pd
from pathlib import Path

def render_history_view():
    st.subheader("📂 Το Ιστορικό μου")
    
    file_path = Path(__file__).parent.parent.parent / "data" / "offers_history.xlsx"
    
    if not file_path.exists():
        st.warning("Δεν βρέθηκε αρχείο ιστορικού.")
        return

    try:
        df = pd.read_excel(file_path)
        active_user = st.session_state.get("active_user", "admin")
        user_role = st.session_state.get("user_info", {}).get("role", "GUEST")

        # Φιλτράρισμα: Οι πωλητές βλέπουν μόνο τα δικά τους, ο Admin όλα
        if user_role != "ADMIN":
            df = df[df["ΠΩΛΗΤΗΣ"] == active_user]

        if df.empty:
            st.info("Δεν υπάρχουν καταγεγραμμένες προσφορές.")
        else:
            st.dataframe(
                df, 
                use_container_width=True, 
                hide_index=True
            )
            
            # Κουμπί για κατέβασμα του Excel
            with open(file_path, "rb") as f:
                st.download_button(
                    "📥 Download Excel",
                    data=f,
                    file_name="my_offers_history.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    except Exception as e:
        st.error(f"Σφάλμα ανάγνωσης ιστορικού: {e}")