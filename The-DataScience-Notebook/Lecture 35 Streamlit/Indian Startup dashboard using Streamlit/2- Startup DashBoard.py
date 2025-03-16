import streamlit as st
import pandas as pd
import numpy as np

startup_data = pd.read_csv("startup_funding.csv")

# data cleaning in the invertor name
startup_data['Investors Name'].fillna('Undisclosed', inplace=True)

st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox("Select one", ["Overall Analysis", "Startup", "Investor"])

if option == "Overall Analysis":
    st.title("Overall Analysis")
    

elif option == "Startup":
    st.sidebar.selectbox("Select Startup", sorted(startup_data['Startup Name'].unique().tolist()))

    startup_button = st.sidebar.button("Find Startup Details")
    st.title("Startup Analysis")


else:
    st.sidebar.selectbox("Select Startup", sorted(startup_data['Investors Name'].unique().tolist()))

    investor_button = st.sidebar.button("Find Investor Details")
    st.title("Investor Analysis")