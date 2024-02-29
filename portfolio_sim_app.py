import streamlit as st
from portfolio_calc import *
import plotly.express as px


# set layout to wide
st.set_page_config(layout="wide")


st.title("Example of modern portfolio theory")
st.write("This app takes a portfolio of stocks and investor risk tolerence and shows the theoretical optimal portfolio allocation.")

col1, col2, col3 = st.columns([1,1.5,1], gap = 'small')

items = ["Microsoft", "Apple", "Google", "Amazon", "Visa", "Nike", "Tesla","Southwest Airlines Co."]
selected_items = []  # Initialize an empty list to hold selected items


with col1:
    st.write("## Input Parameters")
    rf = st.number_input("Risk-free Rate %", value=0.05)
    num_simulations = st.number_input("Number of Simulations", value=1000)
    riskscalar = st.slider('Level of risk tolerence', min_value=0.0, max_value=1.0, value=0.8, step=0.01)

    st.write("Select your companies")    
    # Iterate over the items and create a checkbox for each
    for item in items:
        # Create a checkbox and if it's checked, add the item to the selected_items list
        if st.checkbox(item, key=item, value=True): 
            selected_items.append(item)


with col2:
    
    availableportfoliosdf , frontierdf , tangent , optimalportfolio , portfoliotabledf = portfoliocalc(selected_items , rf, num_simulations,riskscalar)
    st.write("## Output")

    fig = px.scatter(x = availableportfoliosdf['x']*100, y=availableportfoliosdf['y']*100, color_discrete_sequence=['red'])
    # Add a line for the standard deviations and returns
    fig.add_scatter(x = frontierdf['Standard Deviations']*100, y = frontierdf['Returns']*100, mode='lines', name='Efficent Frontier')
    # Add a line for the Capital Allocation Line (CAL)
    fig.add_scatter(x = [0, tangent[0]*100], y = [rf*100, tangent[1]*100], mode='lines', name='CAL', line=dict(color='black'))
    fig.add_scatter(x = [optimalportfolio[0]*100], y = [optimalportfolio[1]*100],  mode='markers', name='Optimal Risky Portfolio', marker=dict(size=10, color='blue'))
    # Set limits
    fig.update_layout(xaxis=dict(range=[0 , 60]), 
                      yaxis=dict(range=[-10,70]))
    # Label axes and add title
    fig.update_layout( xaxis_title='Standard Deviation (Risk)',
                       yaxis_title='Expected Return % Yearly',
                       title='Portfolio Optimization with Efficient Frontier')
    st.plotly_chart(fig)
    st.write(" Your optimal portfolio generates an expected return of "+ str(round(optimalportfolio[1]*100,1)) + "% with an expected volitility of " + str(round(optimalportfolio[0]*100,1))+"%")    

    
with col3:
    #create and plot table
    st.write("## Table Portfolio")
    st.write(portfoliotabledf, index=False)
    
    # Create a pie chart
    fig4 = px.pie(portfoliotabledf, values='Share of Portfolio', names='Companies')
    st.plotly_chart(fig4)
