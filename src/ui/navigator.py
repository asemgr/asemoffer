import streamlit as st
from src.logic.pdf_generator import generate_final_asem_pdf
from src.ui.terms_manager import render_terms_popover  
from datetime import datetime
from src.logic.users_data import USERS

def render_navigator():
    selected_prods = st.session_state.get('catalog_selection', [])
    count = len(selected_prods)

    current_user = st.session_state.get("user_info", {})
    user_role = current_user.get("role", "GUEST")
    max_disc = current_user.get("max_discount", 100) 

    st.markdown(f"""
        <style>
        div[data-testid="stVerticalBlockBorderWrapper"]:has(#nav-anchor) {{
            background-color: #262626 !important;
            border-radius: 12px !important;
            padding: 10px 20px !important;
            border: none !important;
        }}
        .nav-label {{ 
            color: #888 !important; 
            font-size: 11px !important; 
            font-weight: bold !important; 
            text-transform: uppercase; 
            margin-bottom: 8px !important; 
            display: block;
        }}
        .counter-container {{
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 70px; margin-top: -15px;
        }}
        .counter-num {{
            font-size: 2.5rem; font-weight: 900; color: rgba(255, 255, 255, 0.15);
            line-height: 0.2; font-family: 'Arial Black', sans-serif;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(#nav-anchor) div[data-baseweb="input"] > div,
        div[data-testid="stVerticalBlockBorderWrapper"]:has(#nav-anchor) div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
            background-color: #1C1C1C !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(#nav-anchor) input {{
            color: white !important; -webkit-text-fill-color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    column_map = {
        "ΧΟΝΔΡΙΚΗΣ": {"single": "ΤΙΜΗ_Α", "box": "ΤΙΜΗ_Α_ΚΙΒΩΤΙΟ"}, 
        "ΛΙΑΝΙΚΗΣ": {"single": "ΤΙΜΗ_Β", "box": "ΤΙΜΗ_Β_ΚΙΒΩΤΙΟ"}
    }

    with st.container(border=True):
        st.markdown('<div id="nav-anchor"></div>', unsafe_allow_html=True)
        
        cols = st.columns([1.5, 1.5, 0.8, 1.2, 1.2, 1.2, 0.8], vertical_alignment="bottom")

        with cols[0]:
            st.markdown('<p class="nav-label">ΣΤΟΙΧΕΙΑ ΠΕΛΑΤΗ <span style="color:red;">*</span>:</p>', unsafe_allow_html=True)
            customer_name = st.text_input("customer", placeholder="Υποχρεωτικό για συνέχεια...", key="cust_name", label_visibility="collapsed")

        with cols[1]:
            active_user = st.session_state.get("active_user", "guest")
            user_data = USERS.get(active_user, USERS.get("guest"))
            user_catalog_type = user_data.get("catalog_type", "all")
            
            if user_catalog_type == 'wholesale':
                available_options = ["ΧΟΝΔΡΙΚΗΣ"]
            elif user_catalog_type == 'retail':
                available_options = ["ΛΙΑΝΙΚΗΣ"]
            else:
                available_options = ["ΧΟΝΔΡΙΚΗΣ", "ΛΙΑΝΙΚΗΣ"]

            st.markdown('<p class="nav-label">ΕΠΙΛΟΓΗ ΤΙΜΟΚΑΤΑΛΟΓΟΥ:</p>', unsafe_allow_html=True)
            catalog_choice = st.selectbox("setup", options=available_options, key="sel_v20", label_visibility="collapsed")

        with cols[2]:
            st.markdown('<p class="nav-label">% ΕΚΠΤΩΣΗ: </p>', unsafe_allow_html=True)
            discount = st.number_input("num_v20", min_value=0.0, max_value=float(max_disc), value=0.0, step=5.0, key="num_v20_input", label_visibility="collapsed")

        selected_setup = column_map[catalog_choice]

        with cols[3]:
            st.markdown('<p class="nav-label">ΟΡΟΙ & ΠΡΟΥΠΟΘΕΣΕΙΣ: </p>', unsafe_allow_html=True)
            current_terms = render_terms_popover(global_discount=discount)

        with cols[4]:
            st.markdown('<p class="nav-label">ΕΝΕΡΓΕΙΕΣ</p>', unsafe_allow_html=True)
            
            is_disabled = count == 0 or not customer_name.strip()
            if is_disabled:
                st.button("ΕΚΤΥΠΩΣΗ", key="btn_print_off", icon=":material/print:", disabled=True, use_container_width=True) 
            else:
                # 1. Παραγωγή PDF
                pdf_data = generate_final_asem_pdf(
                    selected_prods, 
                    st.session_state.df_print, 
                    terms=current_terms, 
                    price_setup=selected_setup, 
                    global_discount=discount,
                    customer_name=customer_name,
                    product_discounts=st.session_state.get("product_discounts", {})
                )

                # 2. Καταγραφή Ιστορικού
                from src.logic.history_manager import save_offer
                active_user = st.session_state.get("active_user", "guest")
                
                validity_days = current_terms.get("validity", "30")
                validity_str = f"{validity_days} Ημέρες" # Δημιουργία της μεταβλητής για να μην πετάει NameError
                
                log_key = f"log_{customer_name}_{count}_{discount}_{validity_days}"
                if st.session_state.get("last_log") != log_key:
                    df_print = st.session_state.df_print
                    current_items = df_print[df_print['ΠΡΟΪΟΝ'].isin(selected_prods)].to_dict('records')
                    
                    # Κλήση με τη σωστή δομή παραμέτρων
                    save_offer(
                        username=active_user,
                        items=current_items,
                        customer_name=customer_name,
                        catalog=catalog_choice,
                        discount=discount,
                        duration=validity_str
                    )
                    st.session_state["last_log"] = log_key

                # 3. Διαμόρφωση ονόματος αρχείου και Download
                formatted_date = datetime.now().strftime("%d_%m_%Y")
                clean_name = customer_name.replace(" ", "_") if customer_name else "ΠΕΛΑΤΗ"
                file_name = f"ASEM_OFFER_{clean_name}_{formatted_date}.pdf"
                
                st.download_button(
                    "ΕΚΤΥΠΩΣΗ", 
                    data=pdf_data, 
                    icon=":material/print:", 
                    file_name=file_name, 
                    key="btn_print_active", 
                    use_container_width=True,
                    type="primary"
                )

        with cols[5]:
            st.markdown('<p class="nav-label"></p>', unsafe_allow_html=True)
            from src.ui.reset_actions import render_reset_button
            render_reset_button()

        with cols[6]:
            st.markdown('<p class="nav-label" style="text-align:center; margin-bottom:-10px !important;">PRODS:</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="counter-container"><div class="counter-num">{count}</div></div>', unsafe_allow_html=True)

    return selected_setup, discount