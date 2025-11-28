import streamlit as st
import pandas as pd
from assignment2 import run

st.title('A3 Test Runner')
SAMPLE_RATIO = st.number_input('Sample Ratio', value=1e6)
START_DATE = st.text_input('Start Date', value='2021-04-01')
END_DATE = st.text_input('End Date', value='2022-04-30')
COUNTRIES_CSV_PATH = 'a2-countries.csv'
COUNTRIES_CSV = pd.read_csv(COUNTRIES_CSV_PATH)
COUNTRIES = st.multiselect('Select Countries', COUNTRIES_CSV["country"], default=['Afghanistan', 'Sweden', 'Japan'])
if st.button('Run Simulation'):
    run(countries_csv_name=COUNTRIES_CSV_PATH, countries=COUNTRIES, sample_ratio=SAMPLE_RATIO, start_date=START_DATE, end_date=END_DATE)
    st.success('Simulation completed and results saved to CSV files.')
    st.image('a2-covid-simulation.png', caption='COVID-19 Simulation Results')