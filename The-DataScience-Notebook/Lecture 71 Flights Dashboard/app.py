import streamlit as st
from dbhelper import DB
import pandas as pd
import plotly.express as px

db = DB()

st.set_page_config(page_title="Flights Analytics", page_icon="✈️", layout="wide")

st.sidebar.title("✈️ Flights Analytics")
st.sidebar.markdown("---")
user_option = st.sidebar.selectbox("Menu", ["Check Flights", "Analytics"])


# ── ANALYTICS ─────────────────────────────────────────
if user_option == 'Analytics':
    st.title("📊 Flights Analytics Dashboard")
    st.markdown("Visual insights from the flights dataset.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    df = db.fetch_all()
    col1.metric("Total Flights", f"{df.shape[0]}")
    col2.metric("Airlines", df['Airline'].nunique())
    col3.metric("Router", df['Source'].nunique() * df['Destination'].nunique())
    col4.metric("Avg Price", f"₹{df['Price'].mean():,.0f}")
    
    st.markdown("---")
    
    # Row 1: Pie + Bar
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🥧 Flights by Airline")
        airline_count = db.fetch_airline_count()
        fig1 = px.pie(airline_count, 
                      values='Count', 
                      names='Airline', 
                      hole=0.5, 
                      color_discrete_sequence=px.colors.qualitative.Pastel
                      )
        
        fig1.update_traces(
            textposition="inside", 
            textinfo="percent+label"
            )
        
        fig1.update_layout(showlegend=False, margin=dict(t=10, b=10))
        st.plotly_chart(fig1, use_container_width=True)
    
        
    with col2:
        st.subheader("Count of Flights Per City")
        busy_airport = db.busy_airport()
        
        fig2 = px.bar(busy_airport, 
                      x="City", 
                      y="Count",
                      color="City", color_continuous_scale="Blues")
        
        fig2.update_layout(showlegend=False,xaxis_tickangle=-35, margin=dict(t=10, b=80), coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)
        
    
    # Row 2: Line + Bar
    col3, col4 = st.columns(2)   
    with col3:
        st.subheader("📅 Avg Price Over Time")
        price_by_date = df.groupby("Date_of_Journey")["Price"].mean().reset_index()
        
        fig3 = px.line(price_by_date, 
                       x="Date_of_Journey", 
                       y="Price", 
                       labels={"Price": "Avg Price (₹)", "Date_of_Journey": "Date"})
        fig3.update_traces(line_color="#636EFA")
        fig3.update_layout(margin=dict(t=10, b=10))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("🛑 Avg Price by Total Stops")
        stops_price = df.groupby("Total_Stops")["Price"].mean().sort_values().reset_index()
        
        fig4 = px.bar(stops_price, 
                      x="Total_Stops", 
                      y="Price",
                      color="Total_Stops", color_discrete_sequence=px.colors.qualitative.Set2,
                      labels={"Price": "Avg Price (₹)", "Total_Stops": "Stops"})
        
        fig4.update_layout(showlegend=False, margin=dict(t=10, b=10))
        st.plotly_chart(fig4, use_container_width=True)


    # Row 3: Source/Dest heatmap style
    st.subheader("🗺️ Avg Price: Source → Destination")
    pivot = df.groupby(["Source", "Destination"])["Price"].mean().reset_index()
    fig5 = px.density_heatmap(pivot, x="Source", y="Destination", z="Price",
                               color_continuous_scale="Viridis",
                               labels={"Price": "Avg Price (₹)"})
    fig5.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig5, use_container_width=True)


# ── CHECK FLIGHTS ────────────────────────────────────────
else:
    st.title("🔍 Check Flights")

    st.markdown("Filter and explore all available flights from the dataset.")
    col1, col2 = st.columns(2)

    city = db.fetch_city_name()
    city = sorted(city)
    
    with col1:
        source = st.selectbox('Source', city)
    with col2:
        destination = st.selectbox('Destination', [d for d in city if d != source] )

    if st.button('Search'):
        result_flight = db.fetch_all_flights(source,destination)
        
        col4, col5, col6 = st.columns(3)
        col4.metric("💰 Avg Price", f"₹{result_flight['Price'].mean():,.0f}")
        col5.metric("📉 Min Price", f"₹{result_flight['Price'].min():,.0f}")
        col6.metric("📈 Max Price", f"₹{result_flight['Price'].max():,.0f}")
        
        st.markdown(f"### Showing **{len(result_flight):,}** flights")
        st.dataframe(result_flight, use_container_width=True)

        