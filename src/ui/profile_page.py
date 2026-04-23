import streamlit as st
import pandas as pd
from src.logic.users_data import USERS
from src.utils.assets import (
    USER_ICON_BASE64_URL,
    ICON_USER_B64,
    ICON_EMPTY_BOX,
    ICON_NAME_B64,
    ICON_MAIL_B64,
    ICON_PHONE_B64,
    ICON_ROLE_B64,
    ICON_HISTORY_TAB_B64,
    ICON_STATS_TAB_B64,
    ICON_LINK_B64,
    ICON_CALENDAR,
    ICON_DISCOUNT,
    ICON_CLOCK
)
from src.ui.profile_tabs import render_profile_tabs


def show_profile():
    # --- 1. CSS STYLING (FIXED 2-ROW GRID) ---
    st.markdown(f"""
        <style>
        .stApp {{ background-color: #ffffff !important; }}
        
        button[data-baseweb="tab"]:nth-child(1)::before {{
            content: "";
            background-image: url("{ICON_HISTORY_TAB_B64}");
            background-size: contain;
            background-repeat: no-repeat;
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 10px;
            vertical-align: middle;
            opacity: 0.6;
        }}
        
        button[data-baseweb="tab"]:nth-child(2)::before {{
            content: "";
            background-image: url("{ICON_STATS_TAB_B64}");
            background-size: contain;
            background-repeat: no-repeat;
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 10px;
            vertical-align: middle;
            opacity: 0.6;
        }}

        button[data-baseweb="tab"]:nth-child(3)::before {{
            content: "";
            background-image: url("{ICON_LINK_B64}");
            background-size: contain;
            background-repeat: no-repeat;
            display: inline-block;
            width: 18px;
            height: 18px;
            margin-right: 10px;
            vertical-align: middle;
            opacity: 0.6;
        }}
        
        .profile-container {{
            display: flex;
            flex-direction: column;
            gap: 16px;
            width: 100%;
        }}
        .grid-row {{
            display: grid;
            gap: 16px;
            width: 100%;
            grid-template-columns: repeat(2, 1fr); 
        }}
        .info-item {{
            display: flex;
            align-items: center;
            padding: 15px;
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease;
        }}
        .info-item:hover {{
            border-color: #065cab;
            background: #ffffff;
            box-shadow: 0 4px 12px rgba(6, 92, 171, 0.1);
        }}
        .info-label {{
            font-weight: 600;
            color: #64748b;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
        }}
        .info-value {{
            color: #0f172a;
            font-weight: 500;
            font-size: 0.95rem;
            word-break: break-word;
        }}
        @media (max-width: 768px) {{
            .grid-row {{ grid-template-columns: 1fr !important; }}
        }}
        div[data-baseweb="tab-list"] {{
            gap: 6px;
            border-bottom: 2px solid #e2e8f0;
        }}
        button[data-baseweb="tab"] {{
            font-size: 15px !important;
            font-weight: 600 !important;
            color: #64748b !important;
            background-color: transparent !important;
            border: 2px solid transparent !important;
            border-bottom: none !important;
            border-radius: 8px 8px 0 0 !important;
            padding: 10px 20px !important;
            margin-bottom: -2px !important;
            transition: all 0.2s ease !important;
        }}
        button[data-baseweb="tab"]:hover {{
            color: #065cab !important;
            background-color: #fff !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: #065cab !important;
            background-color: #fff !important;
            border-color: #e2e8f0 !important;
            border-bottom-color: #f8fafc !important;
            box-shadow:  0 12px 12px rgba(0, 0, 0, 0.1);
        }}
        div[data-baseweb="tab-panel"] {{
            background-color: #fff;
            border: 2px solid #e2e8f0;
            border-top: none;
            border-radius: 0 4px 12px 12px;
            padding: 20px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            min-height: 400px;
            overflow-y: auto; 
            overflow-x: hidden;
            display: flex;
            flex-direction: column;
        }}
        div[data-baseweb="tab-panel"]::-webkit-scrollbar {{
            width: 8px;
        }}
        div[data-baseweb="tab-panel"]::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 10px;
        }}
        div[data-baseweb="tab-panel"]::-webkit-scrollbar-thumb:hover {{
            background: #065cab;
        }}
        </style>
    """, unsafe_allow_html=True)

    # --- 2. DATA LOGIC ---
    u_url = st.query_params.get("user")
    u_sess = st.session_state.get("active_user")
    active_user = u_url if u_url else (u_sess if u_sess else "admin")
    u_info = USERS.get(active_user, {})

    role_mapping = {
        "SALES_WHOLESALE": "Πωλητής",
        "ADMIN": "Διαχειριστής",
        "SALES": "Πωλητής"
    }
    friendly_role = role_mapping.get(u_info.get('role', 'SALES_WHOLESALE'), u_info.get('role', 'N/A'))

    # --- 3. HEADER ---
    col_logo, _, col_back = st.columns([1.5, 1, 1])
    with col_logo:
        st.image("assets/logo.png", width=340)
    with col_back:
        st.markdown(f'''
            <a href="./?auth=true&user={active_user}" target="_self" style="text-decoration:none;">
                <div style="color: #065cab; padding: 12px; text-align: right; margin-top: 5px; font-weight: bold;">
                    ⬅ Επιστροφή στην Αρχική
                </div>
            </a>
        ''', unsafe_allow_html=True)

    # --- 4. PROFILE CARD ---
    st.markdown("<br>", unsafe_allow_html=True)

    raw_name = u_info.get('name', 'N/A').lower().strip()
    raw_name = raw_name.replace('σ ', 'ς ')
    if raw_name.endswith('σ'):
        raw_name = raw_name[:-1] + 'ς'

    st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <img src="{USER_ICON_BASE64_URL}" width="32" style="margin-right:12px; opacity: 0.7;">
            <h3 style="color: #065cab; margin: 0; font-weight: 700;">Το Προφίλ μου</h3>
        </div>
        <div class="profile-container">
            <div class="grid-row">
                <div class="info-item">
                    <img src="{ICON_NAME_B64}" width="26" style="margin-right:15px; opacity: 0.6;">
                    <div>
                        <div class="info-label">Ονοματεπωνυμο</div>
                        <div class="info-value" style="text-transform: capitalize;">{raw_name}</div>
                    </div>
                </div>
                <div class="info-item">
                    <img src="{ICON_USER_B64}" width="26" style="margin-right:15px; opacity: 0.6;">
                    <div>
                        <div class="info-label">Username</div>
                        <div class="info-value">{active_user}</div>
                    </div>
                </div>
                <div class="info-item">
                    <img src="{ICON_PHONE_B64}" width="26" style="margin-right:15px; opacity: 0.6;">
                    <div>
                        <div class="info-label">Τηλεφωνο</div>
                        <div class="info-value">{u_info.get('phone', '-')}</div>
                    </div>
                </div>
                <div class="info-item">
                    <img src="{ICON_MAIL_B64}" width="26" style="margin-right:15px; opacity: 0.6;">
                    <div>
                        <div class="info-label">Email</div>
                        <div class="info-value">{u_info.get('email', 'N/A')}</div>
                    </div>
                </div>
                <div class="info-item">
                    <img src="{ICON_ROLE_B64}" width="26" style="margin-right:15px; opacity: 0.6;">
                    <div>
                        <div class="info-label">Ρολος</div>
                        <div class="info-value">{friendly_role}</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- 5. TABS ---
    render_profile_tabs(active_user, u_info)

if __name__ == "__main__":
    show_profile()