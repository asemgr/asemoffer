import streamlit as st

def apply_main_light_style():
    st.markdown("""
        <style>
        /* Φόντο κεντρικής οθόνης */
        div[data-testid="stAppViewContainer"] {
            background-color: #ffffff !important;
        }

        /* Container για το Logo και τον Τίτλο */
        .main-header-container {
            display: flex;
            align-items: center;      /* Κεντράρισμα καθ' ύψος */
            justify-content: space-between; /* Logo αριστερά - Τίτλος δεξιά */
            width: 100%;              /* Πλήρες πλάτος */
            margin-bottom: 30px;
            padding: 10px 0;
            border-bottom: 1px solid #f0f2f6; /* Προαιρετική λεπτή γραμμή διαχωρισμού */
        }

        /* Ρυθμίσεις για το Λογότυπο (ASEM) */
        .main-header-container img {
            height: 45px;             /* Ρύθμιση ύψους λογοτύπου */
            width: auto;
            object-fit: contain;
        }

        /* Ο Τίτλος τέρμα δεξιά */
        .main-header-text {
            color: #1e293b !important;
            font-size: 1.3rem !important; /* Κομψό μέγεθος */
            font-weight: 700 !important;
            margin: 0 !important;
            text-align: right;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)