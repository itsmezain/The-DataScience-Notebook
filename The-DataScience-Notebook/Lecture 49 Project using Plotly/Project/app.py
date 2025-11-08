# Importing Libraries
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

st.set_page_config(page_title="India Census Visualization", layout="wide")

# Get current file directory
base_path = os.path.dirname(__file__)

# Construct path to CSV
csv_path = os.path.join(base_path,'india.csv')

india_census = pd.read_csv(csv_path)
 
# Extracting names of the states from the dataset
state = ["India"] + india_census['State'].unique().tolist()

# Extracting the columns on which data will be visualized
primary_parameter = india_census.columns[6:].tolist()


###      Web site part
#------------------------------#
st.sidebar.title('India Census Visualization')

selected_state = st.sidebar.selectbox("Select State", state)

primary = st.sidebar.selectbox("Select Primary Parameter", primary_parameter)

secondary = st.sidebar.selectbox("Select Secondary Parameter", primary_parameter)

plot_btn = st.sidebar.button("Plot Graph")

if plot_btn:
    if selected_state == 'India':
        # Plot for India
        fig = px.scatter_mapbox(
            india_census,
            lat="Latitude",
            lon="Longitude",
            size = primary,
            color = secondary,
            color_continuous_scale=px.colors.cyclical.IceFire,
            size_max=30,
            zoom=3.5,
            hover_name='District', # Shown on hover
            hover_data=['State', primary, secondary],
            title="India Census Visualization",
            width= 1400
        )

        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_center={"lat": 22.9734, "lon": 78.6569},
            margin={"r":0, "t":40, "l":0, "b":0},
            title_x=0.25,
            title_font=dict(size=22, color='Green'),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        # plot for state
        
        fig = px.scatter_mapbox(
            india_census[india_census['State'] == selected_state],
            lat="Latitude",
            lon="Longitude",
            size = primary,
            color = secondary,
            color_continuous_scale=px.colors.cyclical.IceFire,
            size_max=35,
            zoom=5,
            hover_name='District', # Shown on hover
            hover_data=['State', primary, secondary],
            title="India Census Visualization",
            width= 1400
        )

        fig.update_layout(
            mapbox_style="carto-positron",
            margin={"r":0, "t":40, "l":0, "b":0},
            title_x=0.25,
            title_font=dict(size=22, color='Green'),
        )
        
        st.plotly_chart(fig, use_container_width=True)