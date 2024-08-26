################################################ NYC BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'NYC CitiBike Strategy Dashboard', layout='wide')
st.title("NYC CitiBike Strategy Dashboard")
st.markdown("This dashboard aims to deliver a breakdown of some key metrics for New York City Bike share usage based on the data provided by CitiBike . (as well as weather data collected through the NOAA's API)")

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot_7.csv', index_col = 0)
df2 = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)

# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in New York City',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)


## Line chart 

fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily'],'color': 'blue'}),
secondary_y = False
)

fig_2.add_trace(
go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'],'color': 'red'}),
secondary_y=True
)

fig_2.update_layout(
    title = 'Daily bike trips and temperatures in NYC 2022',
    height = 600
)

st.plotly_chart(fig_2, use_container_width=True)


### Add the map ###

path_to_html = 'nyc_bikesv2_kepler.gl.html'


# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in NYC")
st.components.v1.html(html_data,height=1000)
st.markdown("As you can see, usage within NYC is fairly spread out across different cultural centers throughout the city. There are arguably 3 primary hubs; The Hudson River Greenway, Central Park, and Midtown Manhattan (Which contains many tourist attractions such as the Empire State Building, MoMa, Times Square and many other PoIs)")
