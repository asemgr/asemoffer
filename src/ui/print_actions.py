import streamlit as st

def render_print_button():
    customer_name = st.session_state.get("cust_name", "").strip()
    if not customer_name:
        st.toast("Λείπει το όνομα πελάτη", icon="⚠️")
        return False

    # Το κουμπί επιστρέφει True αν πατηθεί
    if st.button("ΕΚΤΥΠΩΣΗ PDF", use_container_width=True):
        # Εδώ θα μπει αργότερα η κλήση για το PDF
        st.toast("Προετοιμασία PDF...", icon="📄")
        return True
    return False