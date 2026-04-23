import streamlit as st

def get_pricing_settings():
    # Διάταξη σε δύο στήλες μέσα στο navigator
    col_cat, col_disc = st.columns(2)
    
    with col_cat:
        catalog_choice = st.selectbox(
            "Τιμοκατάλογος",
            ["Κατάλογος Α", "Κατάλογος Β"],
            label_visibility="collapsed"
        )
    
    with col_disc:
        discount = st.number_input(
            "Έκπτωση (%)",
            min_value=0, max_value=100, value=0, step=1,
            label_visibility="collapsed"
        )
    
    # Αντιστοίχιση στηλών Excel
    column_map = {
        "Κατάλογος Α": {"single": "ΤΙΜΗ_Α", "box": "ΤΙΜΗ_Α_ΚΙΒΩΤΙΟ"},
        "Κατάλογος Β": {"single": "ΤΙΜΗ_Β", "box": "ΤΙΜΗ_Β_ΚΙΒΩΤΙΟ"}
    }
    
    selected_setup = column_map[catalog_choice]
    
    # Ενημέρωση session_state
    st.session_state['selected_price_col'] = selected_setup
    st.session_state['selected_discount'] = discount
    
    return selected_setup, discount