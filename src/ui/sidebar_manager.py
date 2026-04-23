import streamlit as st
import pandas as pd
import src.utils.assets as assets

def get_cat_icon(cat_name):
    mapping = {
        "ΥΓΙΕΙΝΗ ΚΟΥΖΙΝΑΣ": "ICON_1", "ΟΡΟΦΟΚΟΜΙΑ": "ICON_2",
        "ΧΩΡΟΣ ΥΓΙΕΙΝΗΣ": "ICON_3", "ECONOMY LINE": "ICON_4",
        "ΦΡΟΝΤΙΔΑ ΙΜΑΤΙΣΜΟΥ": "ICON_5",
        "ΦΡΟΝΤΙΔΑ ΧΑΛΙΩΝ": "ICON_6",
        "ΚΑΘΑΡΙΣΜΟΣ ΜΗΧΑΝΗΣ ESPRESSO": "ICON_7",
        "ΑΠΟΛΥΜΑΝΣΗ ΧΕΡΙΩΝ & ΕΠΙΦΑΝΕΙΩΝ": "ICON_8",
        "ΒΙΟΜΗΧΑΝΙΑ ΤΡΟΦΙΜΩΝ & ΠΟΤΩΝ": "ICON_9",
        "ΕΠΑΓΓΕΛΜΑΤΙΚΕΣ ΣΥΣΚΕΥΕΣ & ΑΞΕΣΟΥΑΡ": "ICON_10",
        "ΕΠΑΓΓΕΛΜΑΤΙΚΑ ΧΑΡΤΙΚΑ": "ICON_11"
    }
    var_name = mapping.get(cat_name.upper().strip())
    return getattr(assets, var_name, None) if var_name else None

def show_sidebar(df_struct):
    with st.sidebar:
        st.markdown("<h2 style='color:white; text-align:center; padding-bottom: 40px;'>Επιλογή Προϊόντων</h2>", unsafe_allow_html=True)
        
        # Αρχικοποίηση αν δεν υπάρχουν
        if 'catalog_selection' not in st.session_state:
            st.session_state.catalog_selection = []
        if 'reset_counter' not in st.session_state:
            st.session_state.reset_counter = 0

        categories = [c for c in df_struct['ΚΑΤΗΓΟΡΙΑ'].unique() if pd.notna(c)]

        for cat in categories:
            icon_data = get_cat_icon(cat)
            st.markdown(f'''
                <div class="custom-nav-header">
                    <img src="data:image/png;base64,{icon_data if icon_data else ''}">
                    <span>{cat}</span>
                </div>
            ''', unsafe_allow_html=True)

            with st.expander("", expanded=False):
                cat_df = df_struct[df_struct['ΚΑΤΗΓΟΡΙΑ'] == cat]
                subs = [s for s in cat_df['ΥΠΟΚΑΤΗΓΟΡΙΑ'].unique() if pd.notna(s) and str(s).strip() != ""]
                
                if not subs:
                    prods = cat_df['ΠΡΟΪΟΝ'].unique()
                    for p in prods:
                        render_product_checkbox(p, cat, "Γενικά")
                else:
                    for sub in subs:
                        st.markdown(f'<div class="custom-sub-header"><span>{sub.upper()}</span></div>', unsafe_allow_html=True)
                        with st.expander("", expanded=False):
                            prods = cat_df[cat_df['ΥΠΟΚΑΤΗΓΟΡΙΑ'] == sub]['ΠΡΟΪΟΝ'].unique()
                            for p in prods:
                                render_product_checkbox(p, cat, sub)

def render_product_checkbox(p, cat, sub):
    r_id = st.session_state.get('reset_counter', 0)
    clean_p = str(p).replace(" ", "_")
    clean_cat = str(cat).replace(" ", "_")
    # Προσθήκη κατηγορίας στο key για να είναι 100% μοναδικό
    u_key = f"cb_{r_id}_{clean_cat}_{clean_p}" 
    
    is_checked = p in st.session_state.catalog_selection
    
    if st.checkbox(p, key=u_key, value=is_checked):
        if p not in st.session_state.catalog_selection:
            st.session_state.catalog_selection.append(p)
            st.rerun()
    else:
        if p in st.session_state.catalog_selection:
            st.session_state.catalog_selection.remove(p)
            st.rerun()