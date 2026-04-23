import streamlit as st
import pandas as pd
from src.ui.style_manager import render_product_grid

@st.dialog("Ρύθμιση Έκπτωσης")
def edit_discount_modal(product_name):
    if "product_discounts" not in st.session_state:
        st.session_state.product_discounts = {}
    current_val = st.session_state.product_discounts.get(product_name, 0.0)
    new_val = st.number_input("Ποσοστό (%)", min_value=0.0, max_value=100.0, value=float(current_val), step=1.0)
    if st.button("Αποθήκευση"):
        st.session_state.product_discounts[product_name] = new_val
        st.rerun()

def render_product_card(name, data, global_discount):
    color_map = {
        "ΥΓΙΕΙΝΗ ΚΟΥΖΙΝΑΣ": "#095DA9", "ΟΡΟΦΟΚΟΜΙΑ": "#73BF44", "ΧΩΡΟΣ ΥΓΙΕΙΝΗΣ": "#7030A0",
        "ΦΡΟΝΤΙΔΑ ΙΜΑΤΙΣΜΟΥ": "#D66C6C", "ECONOMY LINE": "#002060", "ΦΡΟΝΤΙΔΑ ΧΑΛΙΩΝ": "#ED7D31",
        "ΚΑΘΑΡΙΣΜΟΣ ΜΗΧΑΝΗΣ ESPRESSO": "#582808", "ΑΠΟΛΥΜΑΝΣΗ ΧΕΡΙΩΝ & ΕΠΙΦΑΝΕΙΩΝ": "#5F0369",
        "ΒΙΟΜΗΧΑΝΙΑ ΤΡΟΦΙΜΩΝ & ΠΟΤΩΝ": "#C00000", "ΕΠΑΓΓΕΛΜΑΤΙΚΕΣ ΣΥΣΚΕΥΕΣ & ΑΞΕΣΟΥΑΡ": "#FFC000",
        "ΕΠΑΓΓΕΛΜΑΤΙΚΑ ΧΑΡΤΙΚΑ": "#A9D08E"
    }
    cat = data['ΚΑΤΗΓΟΡΙΑ'].iloc[0] if 'ΚΑΤΗΓΟΡΙΑ' in data.columns else ""
    cat_color = color_map.get(str(cat).strip(), "#1e293b")
    desc = data['ΠΕΡΙΓΡΑΦΗ'].iloc[0] if 'ΠΕΡΙΓΡΑΦΗ' in data.columns else ""

    sel = st.session_state.get("sel_v20", "ΧΟΝΔΡΙΚΗΣ")
    price_setup = {"single": "ΤΙΜΗ_Β", "box": "ΤΙΜΗ_Β_ΚΙΒΩΤΙΟ"} if sel == "ΛΙΑΝΙΚΗΣ" else {"single": "ΤΙΜΗ_Α", "box": "ΤΙΜΗ_Α_ΚΙΒΩΤΙΟ"}

    specific_discount = st.session_state.get("product_discounts", {}).get(name)
    effective_discount = specific_discount if specific_discount is not None else global_discount

    with st.container(border=True):
        # Χρωματιστή μπάρα πάνω — αξιόπιστα με st.html
        st.html(f'<div style="border-top: 5px solid {cat_color}; margin: -16px -16px 10px -16px; border-radius: 4px 4px 0 0;"></div>')

        col_title, col_btn = st.columns([8, 1])

        with col_title:
            # Τίτλος + περιγραφή μαζί σε st.html για να μην σπάει
            st.html(f'''
                <p style="font-size:1.25rem; font-weight:700; color:#1e293b; margin:0 0 3px 0; font-family:sans-serif;">{name}</p>
                <p style="font-size:0.82rem; color:#475569; margin:0; line-height:1.3; font-family:sans-serif;">{desc if desc else ""}</p>
            ''')

        with col_btn:
            if st.button("％", key=f"btn_disc_{name}", use_container_width=True):
                edit_discount_modal(name)

        render_product_grid(name, desc, data, cat_color, price_setup, effective_discount)