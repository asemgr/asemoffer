import streamlit as st

def init_terms_state():
    if 'offer_terms' not in st.session_state:
        st.session_state.offer_terms = {}
    
    defaults = {
        "validity": "30",
        "payment": "Πίστωση 30 ημερών από την έκδοση του τιμολογίου",
        "delivery": "Παράδοση στην έδρα σας εντός 2-3 εργάσιμων ημερών απο την παραγγελία",
        "show_price_policy": True,
        "show_disclaimer": True,
        "price_policy_text": "",
        "disclaimer_text": ""
    }
    
    for key, value in defaults.items():
        if key not in st.session_state.offer_terms:
            st.session_state.offer_terms[key] = value

def render_terms_popover(global_discount=0):
    init_terms_state()
    
    with st.popover("Επιλογές", use_container_width=True):
        # Εφαρμογή του στυλ για το background και το πλάτος
        st.markdown("""
            <style>
            /* Στόχευση του σώματος του popover */
            div[data-testid="stPopoverContent"] {
                background-color: #065cab !important; /* Το μπλε της ASEM */
                border: 1px solid rgba(255,255,255,0.2) !important;
                border-radius: 12px !important;
                min-width: 480px !important; /* Για να μη σου κόβει το κείμενο */
                padding: 20px !important;
            }
            
            /* Λευκά γράμματα παντού */
            div[data-testid="stPopoverContent"] p, 
            div[data-testid="stPopoverContent"] label,
            div[data-testid="stPopoverContent"] span {
                color: white !important;
            }

            /* Styling για τα inputs για να φαίνονται καθαρά πάνω στο μπλε */
            div[data-testid="stPopoverContent"] div[data-baseweb="input"],
            div[data-testid="stPopoverContent"] div[data-baseweb="select"] > div {
                background-color: rgba(255, 255, 255, 0.1) !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                color: white !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<p style="font-weight:bold; font-size:18px; margin-bottom:10px;">Όροι & Προϋποθέσεις Προσφοράς:</p>', unsafe_allow_html=True)
        
        # 1. Ισχύς
        st.session_state.offer_terms["validity"] = st.text_input(
            "Ισχύς προσφοράς (ημέρες)",
            value=st.session_state.offer_terms["validity"]
        )
        
        # 2. Τρόπος Πληρωμής
        pay_options = [
            "Πίστωση 15 ημερών από την έκδοση του τιμολογίου",
            "Πίστωση 30 ημερών από την έκδοση του τιμολογίου",
            "Πίστωση 60 ημερών από την έκδοση του τιμολογίου",
            "Μετρητοίς κατά την παράδοση",
            "Προπληρωμή με τραπεζικό έμβασμα"
        ]
        curr_pay = st.session_state.offer_terms["payment"]
        pay_idx = pay_options.index(curr_pay) if curr_pay in pay_options else 1
        st.session_state.offer_terms["payment"] = st.selectbox(
            "Τρόπος πληρωμής", 
            pay_options, 
            index=pay_idx
        )
        
        # 3. Τρόπος Παράδοσης
        del_options = [
            "Παράδοση στην έδρα σας εντός 2-3 εργάσιμων ημερών απο την παραγγελία",
            "Παράδοση σε αποθήκη σας εντός 2-3 εργάσιμων ημερών απο την παραγγελία",
            "Παράδοση σε μεταφορική της επιλογής σας"
        ]
        curr_del = st.session_state.offer_terms["delivery"]
        del_idx = del_options.index(curr_del) if curr_del in del_options else 0
        st.session_state.offer_terms["delivery"] = st.selectbox(
            "Τρόπος παράδοσης", 
            del_options, 
            index=del_idx
        )
        
        st.write("---")
        
        # 4. Πολιτική Τιμών
        price_text = "Οι αναγραφόμενες τιμές είναι μετά έκπτωσης και προ Φ.Π.Α." if global_discount > 0 else "Οι αναγραφόμενες τιμές είναι προ Φ.Π.Α."
        st.session_state.offer_terms["price_policy_text"] = price_text
        st.session_state.offer_terms["show_price_policy"] = st.checkbox(
            f"Εμφάνιση: {price_text}", 
            value=st.session_state.offer_terms["show_price_policy"]
        )
        
        # 5. Disclaimer
        disclaimer_text = "Η ASEM διατηρεί το δικαίωμα να προβαίνει σε αλλαγές τιμών χωρίς προηγούμενη ειδοποίηση."
        st.session_state.offer_terms["disclaimer_text"] = disclaimer_text
        st.session_state.offer_terms["show_disclaimer"] = st.checkbox(
            "Εμφάνιση δήλωσης αλλαγής τιμών", 
            value=st.session_state.offer_terms["show_disclaimer"]
        )
    
    return st.session_state.offer_terms