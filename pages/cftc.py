import pandas as pd
import streamlit as st

from src import variable_com_disagg

dict_com_disagg = variable_com_disagg()
last_report_date = pd.to_datetime(dict_com_disagg['Report_Date'].max())

tab1, tab2, tab3 = st.tabs(['CFTC Market', 'CFTC Commodity', 'CFTC Classes'])

with tab1:
    st.write('')
    col1, col2, col3 = st.columns([0.70, 0.05, 0.25])

    sel_year = col3.multiselect(label='Year', options=dict_com_disagg['Cftc_year'])
    sel_class = col3.multiselect(label='Classes', options=dict_com_disagg['Argument'])
    sel_market = col3.multiselect(label='Market', options=dict_com_disagg['CFTC_Market_Code'])
    sel_date = col3.date_input(label='Report date', format='YYYY-MM-DD', value=last_report_date)