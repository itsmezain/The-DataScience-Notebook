import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity


# Changing streamlit layout design 
st.set_page_config(layout = 'wide', initial_sidebar_state = 'expanded', page_title='Startup Analysis')


startup_data = pd.read_csv("startup_funding_clean_data.csv")

startup_data['date'] = pd.to_datetime(startup_data['date'], errors = 'coerce')

startup_data['month'] = startup_data['date'].dt.month

startup_data['year'] = startup_data['date'].dt.year



# function to fetch investor detail
#-------------------------------------------#

def load_investor_details(investor):
    st.title(investor)
    
    # load the recent 5 investment of the investor
    last_5_investment = startup_data[startup_data['Investors Name'].str.contains(investor)].head()[['date','Startup Name','Industry Vertical','city','round','amount' ]]

    st.subheader("Most Recent Investment : ")
    st.dataframe(last_5_investment)

    
    # biggest investment 
    col1, col2 = st.columns(2)
    with col1:
        big_inv_series = startup_data[startup_data['Investors Name'].str.contains(investor)].groupby(by= 'Startup Name')['amount'].sum().sort_values(ascending=False).head()
        
        st.subheader("Biggest Investment : ")
        st.dataframe(big_inv_series)
        
    with col2:
        st.subheader("Biggest Investment : ")
        fig, ax = plt.subplots()
        ax.bar(big_inv_series.index, big_inv_series.values)
        
        st.pyplot(fig)
        
    
    # biggest investment graph and generally invest in - graph
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Investment vertical : ")
        fig, ax = plt.subplots()
        investment_vertical_series = startup_data[startup_data['Investors Name'].str.contains(investor)].groupby('Industry Vertical')['amount'].sum()
        ax.pie(investment_vertical_series, labels=investment_vertical_series.index, autopct= "%0.01f")
        st.pyplot(fig)
    
    with col2:    
        
        st.subheader("Investment Round/Stage : ")
        fig, ax = plt.subplots()
        investment_sector_series = startup_data[startup_data['Investors Name'].str.contains(investor)].groupby('round')['amount'].sum()
        ax.pie(investment_sector_series, labels=investment_sector_series.index, autopct= "%0.01f")
        st.pyplot(fig)
        
    with col3:
        st.subheader("Investment City : ")
        fig, ax = plt.subplots()

        investment_city_series = startup_data[startup_data['Investors Name'].str.contains(investor)].groupby('city')['amount'].sum()
        
        ax.pie(investment_city_series, labels=investment_city_series.index, autopct= "%0.01f")
        st.pyplot(fig)

    # YoY investment
    st.subheader("Year over YearInvestment : ")
    
    year_series = startup_data[startup_data['Investors Name'].str.contains(investor)].groupby('year')['amount'].sum()
    
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values, marker='o')
    st.pyplot(fig2)


    ###  Similar Investors name based on the Sector they invest in

    def get_similar_investors(selected_investor, startup_data, top_n=5):
    
        # Create a pivot table: rows are investors and columns are Industry Vertical.
        # The values are the count of investments in that vertical.
        pivot = pd.crosstab(startup_data['Investors Name'], startup_data['Industry Vertical'])
    
        # Normalize each investor's row to sum to 1 (i.e. get a distribution).
        norm_pivot = pivot.div(pivot.sum(axis=1), axis=0)
    
        # Get the distribution vector for the selected investor.
        selected_vec = norm_pivot.loc[[selected_investor]]  # Keep it as a DataFrame
    
        # Compute cosine similarity between the selected investor and all investors.
        sim = cosine_similarity(norm_pivot, selected_vec).flatten()
    
        # Create a Series for similarities with investor names as index.
        sim_series = pd.Series(sim, index=norm_pivot.index)
    
        # Remove the selected investor from the list (similarity with itself).
        sim_series = sim_series.drop(selected_investor)
    
        # Get the top_n similar investors.
        top_similar = sim_series.sort_values(ascending=False).head(top_n)
    
        return top_similar.to_dict()

    similar_investors = get_similar_investors(investor, startup_data, top_n=5)
    st.subheader("Similar Investors:")
    sim_inv_df = pd.DataFrame.from_dict(similar_investors, orient='index', columns=['Similarity'])
    st.dataframe(sim_inv_df)

# Overall Analysis #
# -------------------------------------------------------#

def load_overall_analysis():
    st.title("Overall Analysis")

    col1,col2,col3,col4 = st.columns(4)
        
    with col1:
        # total invested amount
        total_invested_amount = round(startup_data['amount'].sum(), 2)
        st.metric(f"Total amount in INR CR", total_invested_amount )

    with col2:
        # max invested amount
        max_invested_amount = startup_data.groupby('Startup Name')['amount'].max().sort_values(ascending= False).head().values[0]
    
        st.metric(f"Total amount in INR CR", round(max_invested_amount,2))

    with col3:
        # Average investment amount
        average_investment = startup_data.groupby('Startup Name')['amount'].sum().mean()
        
        st.metric(f"Total amount in INR CR", round(average_investment,2))

    with col4:
        # Total funded Startup
        total_funded_startups = startup_data['Startup Name'].nunique()
        
        st.metric("Total funded startups", total_funded_startups) 

    ### MoM investment
    
    st.header('MoM Graph : ')
    
    selected_type_option = st.selectbox('Select type :', [ 'Total', 'Count'])
    
    if selected_type_option == 'Total':
    
        # Total amount invested Month over Month
        temp_df = startup_data.groupby(['year', 'month'])['amount'].sum().reset_index()
    
        temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    
        fig3, ax3 = plt.subplots()
        ax3.plot(temp_df['x-axis'], temp_df['amount'])
    
        st.pyplot(fig3)
    
    else:
        
        # Number of Funding Month over Month
        temp_df = startup_data.groupby(['year', 'month'])['amount'].count().reset_index()
    
        temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    
        fig3, ax3 = plt.subplots()
        ax3.plot(temp_df['x-axis'], temp_df['amount'])
    
        st.pyplot(fig3)
    

###      Web site part
#------------------------------#

st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox("Select one", ["Overall Analysis", "Startup", "Investor"])

if option == "Overall Analysis":
    # Calling the function to load overall analysis
    load_overall_analysis()
    
    
elif option == "Startup":
    st.sidebar.selectbox("Select Startup", sorted(startup_data['Startup Name'].unique().tolist()))

    startup_button = st.sidebar.button("Find Startup Details")
    
    if startup_button:
        startup_button = st.sidebar.button("Find Startup Details")
        st.title("Startup Analysis")


else:
    selected_investor = st.sidebar.selectbox("Select Investor", sorted(set(startup_data['Investors Name'].str.strip().str.split(',').explode().str.strip())))


    investor_button = st.sidebar.button("Find Investor Details")
    
    if investor_button:
        load_investor_details(selected_investor)
    
    

