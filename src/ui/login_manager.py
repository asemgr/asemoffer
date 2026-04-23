import streamlit as st
from src.utils.assets import LOGO_BASE64
from src.logic.users_data import USERS  # <--- ΠΡΟΣΘΗΚΗ ΓΙΑ ΤΗΝ ΕΠΑΛΗΘΕΥΣΗ

# Τα Base64 strings σου
USER_ICON_B64 = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAADsAAAA7AF5KHG9AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAmdJREFUWIW918tvDVEcB/BPSylajwQbKmkVO48gESFWCCtJiYW/QIKdWEm8QiJWIh5RdhaNlcfKYydSj4WyaSwIFcpCF1qt57WYczOn1d7OnXvbbzKZc2Z+3+/ve2bO+Z0ZykMNduI6utEfjm5cw44QMyFYgycojHN0YlVW0axud+EGZob+AO7hbei3YCtmRff34VZWI6WwEUOS0f3CMTSMEteAEyGmgEFsqDT5dMkoC8HEtgyc7fgROG+CRm4ckr7b/WXwDka8A5UYeBpEujGlDN5UvJZOylyYh79B5HgO/snA/YO5YwXVlhBokq6SFzkMdEU5FucxUB+1B3MY6I/aM8cKKmXgfdRelMNAU9R+l4OvBn2S99iRg38zcL+qoDxfDCI/0VoGb3ngFHAhb3KSmv4nCD2SrahMx+PA+Y2VlRiAM9Ki8gDzS8QuwMMo/nSlyWEa7keifZKav1ZS/xuwTrLu+6K4e6irhoGiiQ5jb8Ejj45qJm9Fu2SLzWpgIHCWjideannU45RkQ4pHMyTZI3rwJVxbiCVYb3gB+4nzOBp4mdGCV4aP6jbapB8do6EBu3FnBPdl0MyE1eiNyE+wqRz3AZulu2kBn2T4VGvF54h0SWWTqQ6XI71eJebFDMmjKgYfriDxSByJdLtCrv9wzvCRVxtXIv2zI2+ukNbuTlVcwxHq8Ey6tyyLb16L3OWZcFmxJcrTXrw4G9+lS22icVdarBpJfiCKrtomwcCeKN9euCr9kShVZKqFxpCrgCu10uLwVPJYJhrf8Dy0V9WiOXQ+TELyInrCubkWc0Ln4yQaKOaa8w8XCsN2TQjNFwAAAABJRU5ErkJggg=="
PASS_ICON_B64 = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAcVJREFUWIXF1ztrFUEUwPGfGnMlTSSFj0pttBGFiIK9CIJgJTYKsQs2+QB2Ipb5BoqgKNiLRO0FCSLY2ImFD/ARRYwmJtFizpKw3Ju7e3eue2A4szvn8d/dmTmztCxbBvAZxxTOYF/ce4tHuI3vOcB6yQV8xt9oP6IV159wfljJr2ANP3EN+zeMHcB1LIbNdO7kJ/AHXzC5id2xsFmOfjZ5Kr3isxVsz4Xt41zJ92IVz2v4zIfP7n6GWysEmwy7Ok80Fz59P0MVgF2h39cAeB16rJ/hSIVghc1qDYAH+IonOQAGkSU8rGJY5RMMVVoH6FULJnADp6RlOCbtcksD5CjmwtXo9wXoSOv4MBaiNZEJ7MQrHFfhIS5JO9kdeSbpCO5GzIvlwW5z4EjoW1jJALCCm9E/WgVgNPRyhuSFFLFGywOtr4ImAIekPX8OB9sAmMXpaLNtAPzq0f9vADPWz4QzgwZpss7fRXLqlepsAPBN2mAGlqYAVc6IQwV40xSg2yQsikWnafANsqMUe1OAl6GnM0F0rP+ovCgPdivH2/FMOtEu4mNDgD3SeWIeJ5UK3LYuDmu4L5GPa/4WPuAeLuN3w1j55R9kh1hzVYUyEwAAAABJRU5ErkJggg=="

def render_login():
    st.markdown(f"""
        <style>
        header, footer, [data-testid="stHeader"] {{
            display: none !important;
        }}
        
        .stApp, [data-testid="stForm"] {{
            background-color: #ffffff !important;
        }}

        /* ΕΙΚΟΝΙΔΙΟ ΓΙΑ ΤΟ ΟΝΟΜΑ ΧΡΗΣΤΗ */
        div[data-testid="stTextInput"]:first-of-type label::before {{
            content: "";
            display: inline-block;
            width: 22px;
            height: 22px;
            margin-right: 10px;
            vertical-align: middle;
            background-image: url('data:image/png;base64,{USER_ICON_B64}'); 
            background-size: contain;
            background-repeat: no-repeat;
        }}

        /* ΕΙΚΟΝΙΔΙΟ ΓΙΑ ΤΟΝ ΚΩΔΙΚΟ */
        div[data-testid="stTextInput"]:has(input[type="password"]) label::before {{
            content: "";
            display: inline-block;
            width: 22px;
            height: 22px;
            margin-right: 10px;
            vertical-align: middle;
            background-image: url('data:image/png;base64,{PASS_ICON_B64}');
            background-size: contain;
            background-repeat: no-repeat;
        }}

        /* Στυλ για τα inputs και τα labels */
        div[data-testid="stTextInput"] input {{
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #ced4da !important;
        }}
        
        div[data-testid="stTextInput"] label {{
            text-align: left !important;
            font-weight: bold !important;
            color: #000000 !important;
            display: flex !important;
            align-items: center !important;
        }}

        div[data-testid="stCheckbox"] label p {{
            color: #000000 !important;
            white-space: nowrap !important;
        }}

        /* Layout στήλες */
        [data-testid="column"] {{
            display: flex !important;
            align-items: center !important;
            width: auto !important;
        }}

        div[data-testid="stCheckbox"] {{
            margin-left: -5px !important; 
        }}

        /* Κουμπί */
        div.stButton > button {{
            background-color: #262730 !important;
            color: white !important;
            font-weight: bold !important;
            height: 2.5rem !important;
            border-radius: 4px !important;
            border: none !important;
            padding: 0 15px !important;
        }}

        .forgot-container {{
            margin-left: auto;
            margin-top: 10px;
        }}

        [data-testid="stForm"] {{
            border: none !important;
            padding: 0 !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1.5, 1.5, 1.5])

    with col_mid:
        l_space, logo_col, r_space = st.columns([.5, 8, .5])
        with logo_col:
            st.image(f"data:image/png;base64,{LOGO_BASE64}", width=750)
        
        st.markdown("<p style='text-align: center; color: #005aab; font-size: 30px; font-weight: bold; margin-left: 160px; margin-top: -40px;'>ΔΗΜΙΟΥΡΓΙΑ ΠΡΟΣΦΟΡΑΣ</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #71bf44; font-size: 20px; font-weight: bold; margin-left: 380px; margin-top: -30px;'>www.asem.gr</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #5c5c5c; font-size: 20px; margin-bottom: 10px; margin-top: 10px;'>Πληκτρολογήστε τα στοιχεία σας για είσοδο</p>", unsafe_allow_html=True)

        with st.form("login_box"):
            user_input = st.text_input("ΟΝΟΜΑ ΧΡΗΣΤΗ")
            pw_input = st.text_input("ΚΩΔΙΚΟΣ", type="password")
            
            c1, c2, c3 = st.columns([0.6, 0.1, 1])
            
            with c1:
                submit = st.form_submit_button("ΕΙΣΟΔΟΣ ΣΤΗΝ ΕΦΑΡΜΟΓΗ")
            with c2:
                remember = st.checkbox("Να με θυμάσαι")
            with c3:
                st.markdown("""
                    <div class="forgot-container" style="text-align: right; width: 100%;">
                        <a href="mailto:info@asem.gr" style="color: #005aab; text-decoration: none; font-size: 16px;">Ξέχασα τον κωδικό μου</a>
                    </div>
                """, unsafe_allow_html=True)
            
            if submit:
                # ΔΙΟΡΘΩΜΕΝΗ ΛΟΓΙΚΗ ΕΛΕΓΧΟΥ
                if user_input in USERS and USERS[user_input]["password"] == pw_input:
                    st.session_state["password_correct"] = True
                    st.session_state["active_user"] = user_input  # Για το header_manager
                    st.session_state["user_info"] = USERS[user_input]  # Για το app.py
                    st.session_state["user_catalog_type"] = USERS[user_input].get("catalog_type", "all")
                    st.rerun()
                else:
                    st.error("❌ Λάθος στοιχεία")