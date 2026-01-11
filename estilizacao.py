import streamlit as st

def estilizacao():
    st.markdown("""
    <style>
    .stApp {
        background-color: #E9ECEF;
    }
    
    [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 30px !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1) !important;
        border-top: 8px solid #2E7D32 !important;
    }

    h1, h2, h3, .stWidgetLabel p, .stMarkdown p {
        color: #000000 !important;
        font-weight: 800 !important;
    }

    div[data-testid="stSlider"] > div > div > div > div {
        background: linear-gradient(90deg, #2E7D32 0%, #FBC02D 50%, #D32F2F 100%) !important;
        height: 10px !important;
        border-radius: 5px;
    }
    
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #1A231E !important;
        border: 3px solid #FFFFFF !important;
        width: 25px !important;
        height: 25px !important;
    }

    input, textarea, div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #CED4DA !important;
        font-weight: 500 !important;
    }

    div.stButton > button:first-child {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none !important;
        padding: 15px !important;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)