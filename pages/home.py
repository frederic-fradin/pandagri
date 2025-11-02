import streamlit as st

st.set_page_config(
    page_title="MarketData",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Adjust top padding
st.markdown(
    """
            <style>
                    .block-container {
                        padding-top: 4rem;
                        padding-bottom: 4rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
            </style>
            """,
    unsafe_allow_html=True,
)

# Page header
col1, col2, col3 = st.columns([0.55, 0.10, 0.35])
col1.title("PandAgri - Analysis for agricultural traders")
