import streamlit as st
import pandas as pd

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. Στοχεύουμε σε ΟΛΑ τα πιθανά containers του sidebar */
        [data-testid="stSidebar"], 
        [data-testid="stSidebar"] > div:first-child, 
        [data-testid="stSidebarNav"], 
        .st-emotion-cache-16ids9v, 
        .st-emotion-cache-6qob1r {
            background-color: #262626!important;
        }
        /* 2. Διορθώνουμε το φόντο των expanders που μπορεί να "φεγγίζει" */
        [data-testid="stSidebar"] [data-testid="stExpander"] {
            background-color: transparent !important;
        }
        
        /* ΚΥΡΙΟ BANNER */
        .custom-nav-header {
            background-color: #262626;
            color: white;
            align-items: center;
            padding: 12px 15px;
            margin-top: 8px;
            gap: 150px;
            transition: background-color 0.4s ease;
            position: relative;
            z-index: 1 !important;
            pointer-events: none;
        }
        
        .custom-nav-header img { width: 30px; height: auto; margin-right: 15px !important; }
        .custom-nav-header span { font-weight: bold; font-size: 1rem; text-transform: uppercase; }

        /* ΥΠΟΚΑΤΗΓΟΡΙΑ */
        .custom-sub-header {
            background-color: #1C1C1C;
            color: #eeeeee;
            padding: 12px 10px;
            font-size: .95rem;
            font-weight: 700;
            margin: 8px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        /* MOUSE OVER */
        [data-testid="stSidebar"] [data-testid="stExpander"]:hover + .custom-nav-header,
        .custom-nav-header:hover {
            background-color: #45ff29 !important;
        }

        /* ΕΞΑΦΑΝΙΣΗ DEFAULT EXPANDERS */
        [data-testid="stSidebar"] [data-testid="stExpander"] {
            background: #1C1C1C !important;
            margin-top: -42px !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stExpander"] summary {
            opacity: 0 !important;
            height: 45px !important;
        }

        /* ΔΙΟΡΘΩΣΗ ΓΙΑ NESTED */
        [data-testid="stSidebar"] [data-testid="stExpanderDetails"] [data-testid="stExpander"] {
            margin-top: -45px !important;
        }
        [data-testid="stSidebar"] [data-testid="stExpanderDetails"] [data-testid="stExpander"] summary {
            height: 40px !important;
        }
        
        /* CHECKBOXES */
        [data-testid="stSidebar"] [data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"] {
            background-color: #45ff29 !important;
            border-color: #45ff29 !important;
        }
        [data-testid="stSidebar"] [data-testid="stCheckbox"] div[role="checkbox"]:hover {
            border-color: #45ff29 !important;
        }
        [data-testid="stSidebar"] [data-testid="stCheckbox"] svg {
            fill: #000000 !important;
        }
        [data-testid="stSidebar"] [data-testid="stCheckbox"] {
            margin-bottom: -5px !important;
        }
        [data-testid="stSidebar"] [data-testid="stCheckbox"] label p {
            color: #e0e0e0 !important;
            font-size: 0.9rem !important;
        }
        [data-testid="stSidebar"] [data-testid="stExpanderDetails"] {
            padding-top: 0px !important;
            padding-bottom: 10px !important;
        }

        /* ΕΥΘΥΓΡΑΜΜΙΣΗ SIDEBAR TOP ELEMENTS */
        [data-testid="stSidebarContent"] > div > div:first-child {
            display: flex !important;
            align-items: center !important;
        }
        [data-testid="stSidebarContent"] > div > div:first-child > div[data-testid="column"] {
            display: flex !important;
            align-items: center !important;
        }
        [data-testid="stSidebarContent"] > div > div:first-child > div[data-testid="column"] > div {
            display: flex !important;
            align-items: center !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        [data-testid="stSidebarContent"] > div > div:first-child button {
            margin: 0 !important;
            vertical-align: middle !important;
        }
        [data-testid="stSidebarContent"] > div > div:first-child .user-text-sidebar {
            margin: 0 !important;
            line-height: 32px !important;
        }

        /* ΟΜΟΙΟΜΟΡΦΑ ΚΕΝΑ ΚΑΡΤΩΝ ΠΡΟΪΟΝΤΩΝ */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            margin-bottom: 16px !important;
        }
        </style>
    """, unsafe_allow_html=True)


def render_product_grid(name, desc, df_variants, border_color="#1e293b", price_setup=None, global_discount=0):
    import re
    
    col_single = price_setup['single'] if price_setup else "ΤΙΜΗ_Α"
    col_box = price_setup['box'] if price_setup else "ΤΙΜΗ_Α_ΚΙΒΩΤΙΟ"

    def safe_float(val):
        if pd.isna(val) or str(val).strip().lower() in ['', 'nan', 'none']:
            return 0.0
        try:
            clean_val = str(val).replace(',', '.')
            clean_val = re.sub(r'[^0-9.]', '', clean_val)
            return float(clean_val)
        except (ValueError, TypeError):
            return 0.0

    specific_discount = st.session_state.get("product_discounts", {}).get(name)
    if specific_discount is not None and specific_discount > 0:
        # Inline (ειδική) έκπτωση -> Πράσινο
        ui_price_color = "#28a745"
        ui_font_weight = "bold"
    elif global_discount > 0:
        # Γενική έκπτωση -> Μπλε
        ui_price_color = "#095DA9"
        ui_font_weight = "bold"
    else:
        # Καμία έκπτωση -> Default σκούρο
        ui_price_color = "#1e293b"
        ui_font_weight = "bold"

    table_rows = ""
    for _, row in df_variants.iterrows():
        raw_p_monados = safe_float(row.get(col_single, 0))
        raw_p_kivotiou = safe_float(row.get(col_box, 0))
        
        final_p_monados = raw_p_monados * (1 - global_discount / 100)
        final_p_kivotiou = raw_p_kivotiou * (1 - global_discount / 100) if raw_p_kivotiou != 0 else 0
        
        clean_code = str(row['ΚΩΔΙΚΟΣ']).replace('.0', '').strip()
        
        raw_sysk = str(row.get('ΣΥΣΚΕΥΑΣΙΑ', '1')).strip()
        clean_sysk = '-' if raw_sysk.lower() == 'nan' or raw_sysk == '' else raw_sysk

        p_monados_str = f"{final_p_monados:.2f}€"
        p_kivotiou_str = f"{final_p_kivotiou:.2f}€" if final_p_kivotiou != 0 else "-"

        table_rows += f"""
        <tr style="background: white;">
            <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center; color: #1e293b;">{clean_code}</td>
            <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center; color: #1e293b;">{row.get('ΛΙΤΡΑ', '')}</td>
            <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center; color: #1e293b;">{clean_sysk}</td>
            <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center; font-weight: {ui_font_weight}; color: {ui_price_color};">{p_monados_str}</td>
            <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center; font-weight: {ui_font_weight}; color: {ui_price_color};">{p_kivotiou_str}</td>
        </tr>"""

    full_html = f"""
    <div style="background: white; border-radius: 4px;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
        <thead>
            <tr style="background: black;">
                <th style="padding: 8px; color: white;">ΚΩΔΙΚΟΣ</th>
                <th style="padding: 8px; color: white;">LT/KG</th>
                <th style="padding: 8px; color: white;">ΣΥΣΚ.</th>
                <th style="padding: 8px; color: white;">ΤΙΜΗ Μ.</th>
                <th style="padding: 8px; color: white;">ΤΙΜΗ Κ.</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    </div>
    """
    st.html(full_html)