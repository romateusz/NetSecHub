import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Styl dla st.link_button (np. "Otwórz") */
        div[data-testid="stLinkButton"] a {
            background-color: #e0f2f7 !important;
            color: #000000 !important;
            border: 1px solid #add8e6 !important;
            transition: all 0.3s ease-in-out;
            font-weight: bold;
            text-decoration: none;
        }

        /* Styl dla st.button (np. "Zapisz", "Dodaj") */
        button[data-testid^="stBaseButton"] {
            background-color: #f0f2f6 !important;
            color: #000000 !important;
            border: 1px solid #d1d1d1 !important;
            font-weight: bold;
            transition: all 0.3s ease-in-out;
        }

        /* Efekt Hover dla obu typów przycisków */
        div[data-testid="stLinkButton"] a:hover, 
        button[data-testid^="stBaseButton"]:hover {
            background-color: #0F2866 !important;
            color: #ffffff !important;
            transform: scale(1.02);
            border: 1.5px solid #0F2866 !important;
        }
        </style>
        """, unsafe_allow_html=True)