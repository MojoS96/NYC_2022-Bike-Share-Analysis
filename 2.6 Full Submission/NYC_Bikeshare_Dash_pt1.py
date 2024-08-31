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
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'NYC CitiBike Strategy Dashboard', layout='wide')
st.title("NYC CitiBike Strategy Dashboard")

# Define side bar
st.sidebar.title("Chapter Selector")
page = st.sidebar.selectbox('Select a chapter of the analysis to navigate to',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot_7.csv', index_col = 0)
df2 = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)

######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems that CitiBikes currently faces in the New York City area.")
    st.markdown("Right now, Citi bikes runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 chapters:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Chapter Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("Citi_Bike_Ride_experience_Hero_3x.webp") #source: https://citibikenyc.com/how-it-works


    ### Create the dual axis line chart page ###
    
elif page == 'Weather component and bike usage':

   fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

	fig_2.add_trace(go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily'],'color': 'blue'}),secondary_y = False)

	fig_2.add_trace(go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'],'color': 'red'}),secondary_y=True)

	fig_2.update_layout(title = 'Daily bike trips and temperatures in NYC 2022',height = 600)

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("Based on how closely the two variables plotted mirror each other there is an easily identifiable correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. With this knowledge we can infer that the inventory shortage problem that is sometimes felt by the customers may be more widespread in the warmer months, approximately from May to October. This date range also aligns nicely with often held assumptions that late spring to early fall is the peak season for tourism (international, as opposed to domestic which also peaks during US Thanksgiving and Christmas) (Additional reading about Tourism seasonality: https://www.seathecity.com/when-is-the-best-time-to-visit-new-york-city/#:~:text=Peak%20Tourist%20Season,at%20all%20the%20wonderful%20attractions.)

### Most popular stations page

    # Create the season variable

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
    
    # Bar chart

    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in Ney York City',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("***As a disclaimer, for those that do not have an encyclopeadic knowledge of the street names and intersections it's understandably quite difficult to put the following station names into context. I'd recommend skipping to the next section containing map data to better understand how these trip volumes look in real life.***)
    st.markdown(" ")
    st.markdown("From the bar chart it is clear that there are some start stations that are more popular than others - in the top 3 we can see W 21 St & 6 Avenue (located in Midtown Manhattan), West St & Chambers St. (Found at the midway point of the Hudson Greenway Cycle Path) as Broadway & W 58 St. (Located on the Southwest corner of Central park). These 3 spots represent areas which combine a good mixture of popular tourist attractions as well as central locations which would be likely to have a good amount of usage by local residents going about their day to day commutes. There is a huge delta between the highest and lowest bars of the plot, which I believe is indicative of how interconnected the city is and how the main points of interest are fairly well spread out across multiple sections. This is a finding that we could cross reference with the interactive map that you can access through the side bar select box. In the meantime, please familiarize yourself with the google street map images of the popular stations to get an idea of the areas they serve")
    ### Images of the most popular station streets ###

    st.markdown(" ")
    st.markdown("1. W 21 St & 6 Avenue:")

    ### Image 1 ###

    myImage2 = Image.open("W21st_6thAve.PNG")

    st.markdown("2. West St & Chambers St:")

    ### Image 2 ###

    myImage3 = Image.open("ChambersSt_WestSt.PNG")

    st.markdown("3. Broadway & W 58 St:")

    ### Image 2 ###

    myImage4 = Image.open("Broadway_W58St.PNG")

elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over Ney York City")

    path_to_html = "nyc_bikesv2_kepler.gl.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in New York City")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown(""As you can see, usage within NYC is fairly spread out across different cultural centers throughout the city. There are arguably 3 primary hubs; The Hudson River Greenway, Central Park, and Midtown Manhattan (Which contains many tourist attractions such as the Empire State Building, MoMa, Times Square and many other PoIs)"")
    st.markdown("*** NEEDS EDITING*** The most common routes (>2,000) are between Theater on the Lake, Streeter Dr/Grand Avenue, Millenium Park, Columbus Dr/Randolph Street, Shedd Aquarium, Michigan Avenue/Oak Street, Canal Street/Adams Street, which are predominantly located along the water.")

else:
    
    st.header("Conclusions and recommendations")
    bikes = Image.open("recs_page.png")  #source: Midjourney
    st.image(bikes)
    st.markdown("### Our analysis has shown that Citi Bikes should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations around the water line, such as heater on the Lake, Streeter Dr/Grand Avenue, Millenium Park, Columbus Dr/Randolph Street, Shedd Aquarium, Michigan Avenue/Oak Street, Canal Street/Adams Street")
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand, but provide a lower supply in winter and late autumn to reduce logistics costs")