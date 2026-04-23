import streamlit as st
from src.logic.users_data import USERS

def render_top_bar():
    # --- ΛΟΓΙΚΗ ΑΝΑΓΝΩΡΙΣΗΣ ΧΡΗΣΤΗ ---
    url_user = st.query_params.get("user")
    session_user = st.session_state.get("active_user")
    # Προτεραιότητα στο URL user, μετά στο session, μετά admin
    user_key = url_user if url_user else (session_user if session_user else "admin")
    
    user_info = USERS.get(user_key, {})
    full_name = user_info.get("name", "ADMINISTRATOR")

    # Icons (Base64)
    USER_ICON = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAHYAAAB2AH6XKZyAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAABOZJREFUeJzdm91vVEUYxn9dI4iUimBJ/Ggh2kKFKoliVaLGr3jpR0yMkmgiRPgL1KR+RAWrF5p4qdEbIX7GeCVeqFHqBYmhGLWVFCoG0RSpQqtFabHsevGe1br7nLO7c87Mbv0lczN7zvs87+zsnDkzs02Eowu4DVgPrALagebosxPAYWAY2A18BOwP6M0b84HNwF6gUGMZAB4C5gV3nREbgJ+oPfHSchi4N7D3VLQCH5I+8dLyAXBewDyc6AZ+JPvki+UHYE2wbGrkSuA4yQl8A2wFbsIGwoVRWRXVbQMGK8Q4BlwRKKeq6QCOEm/6Y6yBqmUd8ElCvJ+BizPynpqzgK/QRseB21PEvgOYiIm9F3vK1J0X0AYPYF07LV1RLKXxfAbxU7EG+ItyY6PAhRnqXBTFLNU5hTVQ3XhHmPoT6PGgdQ1wUui96UGrKlYAM8LQ0x41twm9GWxaHZwnhJkxoMWj5iLsCVCq2+tRM5YBYeTxALpPCt0vAuj+h8Xo7h9ilnaZ0J0Bzgmg/Q/XCRPfBdQ/KPTXuwTKORroFHX7HGO5oLSUp4q4NsASUTfqGMsFpbXUJZBrAywQdccdY7lwTNSd7RLItQFOiDqnb8ARtS4w6RLItQEmRN35jrFcuEDUKU8VcW2AEVG32jGWC0rrQEB9moHTlD+KugNorxW6p/l3hbkm0owBX4r6uxzj1cKdom4APS55pZf6vAuolaeHPWrGsgK9FvCMR81nhd4poM2jZiJvCEMngas9aF0LTAm9HR60quZSYFqYGsVWcbKiDTgidKap84oQQB96vW4Ea6C0rI5iKY2tGcRPzQLi9/4mSPdkuBv4LSb2HmxFuiFYjj0BlNEC8ClwVQ3xeoDPEuIdpU7LYEmsBX4h3nQBGMJG8luw325zVLqiuj7g2woxxoDLA+VUM93A9yQnkKYcpIH3Bosswb7prJMfQq9DNAwt2GGIr/HXA4aBR2mwhmjG9gIm8Zd4aZkEnsLxBSgrzgC2oCcoocqRyIPrSx1NjvctB7YDN1RxbQHb8+/HRvj92LGXceCP6JqFWLduB1ZiA92N2KBajcd+4IEornc2EL9lXSx5YBewETsy40orsAlLMF9BcxzPZ4masO3oJBNTwCvAJR70O4BX0e8es0sf7j07ljOxLp/0je8g2y3xONqwHeGkRng98pwJ84CdCWIj2O81NDejd4iKZScZnDFswlozTuR9bJ+wXrQAbwtfxfIWKZ4QAC/FBM5jE5JGoZf4QfJF16D3xQScAR5M59cLm9A71gXgnlqDdaDfw/ORUKNyP7onTGLzi6rIYQcOVEs2UreP4zG0991UOR5siQnwrgezvngPncPGSjcuBX4VN47gd70/axaj1yXGgHOTbnxO3FTAnrlzjVvRucQupLZg8+nSG7b7duoRNUeYIOY80SPi4inCTG990Y5+d5BbacPiwpeD2PTLa5TnVbaV3iMuyuPnrS40nei5wbrZF6kp766QLj3zORWmyPvEBRWfmXOIzZTnN1j8cBnlXSRPupWcRiMux2U5bF2vdAVlENvl+b8whq1HzqYJuD6Hnb0tpd+7pfConLpz6LekIc9m6kFpDwDozKHP2AY9chYI9V/klTn0qctDfr3UhUOirjWHnbwq5Xe/XuqCymkR6LnynP3HdgLzKc9z+m/D0QfFcbkaEAAAAABJRU5ErkJggg=="
    LOGOUT_ICON = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAB2AAAAdgB+lymcgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAKPSURBVHic7du9jw1RHMbxz24kErEsIUI0XjrlrspGFBKJToFKhNhoROkPQPREwSKi9A8oxFuhIirRKYWC2MiyxEpWcXfZ3JwZd+15u9l9kl8zM5nzPN8758yZuWfoTYM4jAm8wSRmM9d3PMdoj56jaT9eLcF47PqEjUkTL9B5zCQO9D91NFbAVS37TuNqrIb6TXvxU/lfulgXeFY4ZKiyDYKjLSY+Y1zGQaiELgmHn8Lugr6y6YEwgAslTaXSYGDbtoZjH6Y0UkohAGsbjp1KaaSUQgCWlVYAlDZQWv0CYAPGsDVHY2+Fb4O7cjQe0Al8nfPwC1cwkLLBmgDswI+AlwmRINTeBfZhdWD7OG6KAKF2AO9b9kWD0K2ausAgnjb4id4d5lUTABjGiwZP83VHxKu5NgBkhlAjADJCqBUAvUG4bYkQagZABgi1AyAxhH4AQEII/QKARBD6CQAJIMQEsAbXdaa0bQZzVM/T5pgArlUQfGGd6TaY+mHoeOLzL1YnuzfU/jQYW7PdG1IDuJ/4/IvVvV4OWhkEIwLIoWG8VOltMLWih6d/ACQJT38ASBae+gEkDU/dAJb1C5Es4akTQLbw1Acga3jqArDs/xg50OAlWvjanwa3tOy7hbM6IKKqpitgO74FvES/7BeqJgBwDF/mPMzgsmW0QGJeQzoLuDfHPnHbcvmaNKUz/Y2u2gfB5FoBUNpAaYUANK0JHkpppJRCAD40HHswpZGadFH4NvgROwv6yqYRzXPvSZ3p56Zi7jLpifaHkBI1jcfYkzD3H42o97O5d1ifLvpfnSoQrtc6Eitk2zzgLs7prNCuTbM5Gxvz79fQubvAuqSJAxrAIdzAa50PKHMHn8YjkQfB3yvgfcyLwzefAAAAAElFTkSuQmCC"

    # Logout logic
    if st.query_params.get("action") == "logout":
        st.query_params.clear()
        st.session_state.clear()
        st.rerun()

    st.markdown(f"""
        <style>
        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 0rem !important;
        }}
        header[data-testid="stHeader"] {{
            background-color: rgba(0,0,0,0) !important;
            background: none !important;
            box-shadow: none !important;
        }}
        header[data-testid="stHeader"] svg {{
            fill: #000000 !important;
        }}
        header[data-testid="stHeader"] p, 
        header[data-testid="stHeader"] span {{
            color: #000000 !important;
        }}
        .top-bar-right {{
            position: fixed;
            top: 0px;
            right: 120px;
            height: 62px;
            display: flex;
            align-items: center;
            gap: 13px;
            z-index: 999999;
            background: transparent !important;
        }}
        .item-box {{
            display: flex;
            align-items: center;
            gap: 10px;
            color: #000000 !important;
            font-size: 12px;
            font-weight: 570;
            text-decoration: none !important;
        }}
        .user-link {{
            color: #000000 !important;
            cursor: pointer;
            transition: 0.2s;
        }}
        .user-link:hover {{
            text-decoration: underline !important;
            opacity: 0.7;
        }}
        .logout-link {{
            color: #000000 !important;
            opacity: 0.8;
            transition: 0.2s;
            cursor: pointer;
        }}
        .logout-link:hover {{
            opacity: 1;
            color: #be185d !important;
        }}
        .icon-img {{
            width: 18px;
            height: 18px;
            filter: brightness(0);
        }}
        .logout-link:hover .icon-img {{
            filter: invert(18%) sepia(88%) saturate(3475%) hue-rotate(326deg) brightness(84%) contrast(100%);
        }}
        </style>
        
        <div class="top-bar-right">
            <a class="item-box user-link" href="./?view=profile&auth=true&user={user_key}" target="_self">
                <img src="{USER_ICON}" class="icon-img">
                <span class="user-name-text">{full_name}</span>
            </a>
            <a class="item-box logout-link" href="./?action=logout" target="_self">
                <img src="{LOGOUT_ICON}" class="icon-img">
                <span>ΑΠΟΣΥΝΔΕΣΗ</span>
            </a>
        </div>
    """, unsafe_allow_html=True)