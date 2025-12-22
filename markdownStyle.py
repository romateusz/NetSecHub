import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* PODSTAWOWE STYLE DLA WSZYSTKICH PRZYCISKÓW */
        button[data-testid^="stBaseButton"], div[data-testid="stLinkButton"] a {
            transition: all 0.3s ease-in-out !important;
            font-weight: bold !important;
            text-decoration: none !important;
        }

        /* STYLE DLA PRZYCISKÓW STANDARDOWYCH (Otwórz, Zapisz, Dodaj) */
        /* Link Button (Otwórz) */
        div[data-testid="stLinkButton"] a {
            background-color: #e0f2f7 !important;
            color: #000000 !important;
            border: 1px solid #add8e6 !important;
        }

        /* Standardowy Button */
        button[data-testid^="stBaseButton"] {
            background-color: #f0f2f6 !important;
            color: #000000 !important;
            border: 1px solid #d1d1d1 !important;
        }

        /* EFEKT HOVER DLA PRZYCISKÓW AKTYWNYCH (Niebieski + Powiększenie) */
        /* Wykluczamy przyciski z Popovera (usuwanie) za pomocą :not */
        div[data-testid="stLinkButton"] a:hover, 
        button[data-testid^="stBaseButton"]:not(:disabled):not(div[data-testid="stPopover"] button):hover {
            background-color: #0F2866 !important;
            color: #ffffff !important;
            transform: scale(1.02) !important;
            border: 1.5px solid #0F2866 !important;
        }

        /* STYLE DLA PRZYCISKÓW "USUŃ TRWALE" (Wewnątrz Popover) */
        div[data-testid="stPopover"] button {
            background-color: #ff4b4b !important; /* Czerwony */
            color: white !important;
            border: 1px solid #ff4b4b !important;
        }

        div[data-testid="stPopover"] button:hover {
            background-color: #b91d1d !important; /* Ciemniejszy czerwony */
            color: white !important;
            transform: none !important; /* WYŁĄCZENIE POWIĘKSZENIA */
            border: 1px solid #b91d1d !important;
        }

        /* PRZYCISK ZABLOKOWANY (Oczekiwanie...) */
        button[data-testid^="stBaseButton"]:disabled {
            cursor: not-allowed !important;
            opacity: 0.6 !important;
            filter: grayscale(1) !important;
            transform: none !important;
        }

        /* DODATKI DLA WYŚRODKOWANIA PIONOWEGO */
        [data-testid="stNotification"], .stCodeBlock {
            margin-bottom: 0px !important;
        }
                
        /* Ukrycie kursora wyszukiwania jeśli nie jest używany */
        div[data-baseweb="select"] > div {
            cursor: pointer !important;
        }

        /* Ukrycie migającego kursora w selectboxie, aby nie wyglądał jak pole tekstowe */
        div[data-baseweb="select"] input {
            caret-color: transparent !important;
        }

        /* Styl dla opcji wewnątrz listy rozwijanej */
        div[role="listbox"] ul {
            background-color: #ffffff !important;
        }

        /* Obramowanie selectboxa */
        div[data-baseweb="select"] {
            border: 1px solid #d1d1d1 !important;
            border-radius: 8px !important;
        }
                
        </style>
        """, unsafe_allow_html=True)