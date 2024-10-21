import streamlit as st
from datalib.streamlitFunctions import center_h2, center_text
from data.uberdata.uberdatadescriptions import uberdata_description, dataset_overview_text
import pandas as pd
import plotly.express as px
from datalib.plots import histogram_with_stats
from config import UBERLOGO
import os
from st_aggrid import AgGrid

def get_data():
    data = pd.read_csv('data/uberdata/uberdata.csv')
    date_columns = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']
    for column in date_columns:
        data[column] = pd.to_datetime(data[column])
    data['hour'] = data['tpep_pickup_datetime'].dt.hour

    # Calculate the duration of each trip in minutes
    data['duration'] = (data['tpep_dropoff_datetime'] - data['tpep_pickup_datetime']).dt.total_seconds() / 60

    # Remove all trips with a duration of less then 1 minute
    data = data[data['duration'] >= 1]

    # Remove all trips with passenger count of 0
    data = data[data['passenger_count'] > 0]

    # Remove all trips with a fare amount <= 0
    data = data[data['fare_amount'] > 0]

    # Remove all trips with distance <= 0
    data = data[data['trip_distance'] > 0]

    # Remove all trips with duration > 244 minutes
    data = data[data['duration'] <= 244]

    # Remove lines with a duration smaller than 13 and a total amount higher that 90
    data = data[~((data['duration'] < 13) & (data['total_amount'] > 90))]

    # Remove trip distances == 99.9
    data = data[data['trip_distance'] != 99.9]

    # Save the data to an Excel file
        # convert to timezone unaware
    savetoexcel = False
    if savetoexcel:
        print("Saving data to Excel file...")
        data['tpep_pickup_datetime'] = data['tpep_pickup_datetime'].dt.tz_localize(None)
        data['tpep_dropoff_datetime'] = data['tpep_dropoff_datetime'].dt.tz_localize(None)
        data.to_excel('data/uberdata.xlsx', index=False)
        print("Data saved to Excel file.")

    
    return data

# 1. Title and Introduction
def title_and_intro(data):
    # Add a title and a brief introduction
    st.title('Uber Data Analysis Dashboard')
    st.markdown('---')
    center_text('In a late 2024 course, we were tasked with creating a Streamlit dashboard using Uber data.')
    st.markdown('---')

    # Dataset presentation
    center_h2('The Dataset Presentation')
    AgGrid(data.head(10), fit_columns_on_grid_load=True)  # Display the first 10 rows
    st.markdown('---')

    # Dataset description
    col1, col2 = st.columns(2)
    with col1:
        center_h2('The Dataset Description')

        st.markdown(uberdata_description)
    with col2:
        # show uber logo image
        absolute_path = os.path.abspath(UBERLOGO)
        st.image(absolute_path, use_column_width=True)
    st.markdown('---')

    # Problematic statement
    col1, col2 = st.columns(2)
    with col1:
        center_h2('The Problematic: How to become a successful Uber Driver ?')
        center_text('In order to answer this question, we need to define what success means in this case. In our analysis, we will consider the following metrics:')
        center_text('1. Maximizing total amount earned per ride')
        center_text('2. Reducing the time spent on each ride')
        center_text('3. Maximizing the number of rides')
        center_text('4. Increasing the amount of tips received')

    
    
    # Summary of what we will analyze
    with col2:
        center_h2('Summary of the Analysis')
        center_text('1. Dataset Overview')
        center_text('2. Exploring Trip Duration and Distance')
        center_text('3. Time and Location Analysis')
        center_text('4. Passenger Count and Earnings')
        center_text('5. Revenue Maximization Factors')
        center_text('6. Optimization Insights')
        center_text('7. Conclusion')  
    st.markdown('---')

# 1. Dataset Overview
def dataset_overview(data):
    center_h2('1. Dataset Overview')
    cols = st.columns(2)

    with cols[0]:
        fig_fare = histogram_with_stats(data, 'fare_amount', 'Fare Amount Distribution')
        st.plotly_chart(fig_fare, use_container_width=True)

    with cols[1]:
        fig_tip = histogram_with_stats(data, 'tip_amount', 'Tip Amount Distribution')
        st.plotly_chart(fig_tip, use_container_width=True)

    center_text(dataset_overview_text)

    # analysis of scatter plots
    st.markdown('---')
    center_h2('Analysis of Scatter Plots')
    center_text("In this part, you can choose two columns to plot against each other. The scatter plot will show the relationship between the two columns.")
    col1, col2 = st.columns(2)
    with col1:
        column1 = st.selectbox('Select the first column', data.columns, index=data.columns.get_loc('fare_amount'))
    with col2:
        column2 = st.selectbox('Select the second column', data.columns, index=data.columns.get_loc('trip_distance'))
    

    fig = px.scatter(data, x=column1, y=column2, title=f'{column1} vs {column2}')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('---')

# 2. Exploring Trip Duration and Distance
def trip_duration_and_distance(data):
    # Title
    center_h2('2. Exploring Trip Duration and Distance')

    # Brief Introduction
    st.markdown("In this section, we explore how trip duration and distance vary across different trips, and the relationships between these variables over time.")

    # First row: Distribution of Trip Duration and Distance
    st.markdown('---')
    st.subheader("Distribution of Trip Duration and Distance")
    
    # Use two columns for histograms
    col1, col2 = st.columns(2)

    with col1:
        fig_duration = px.histogram(
            data, 
            x='duration', 
            nbins=50, 
            title='Distribution of Trip Duration',
            labels={'duration': 'Trip Duration (minutes)'},  # Updated axis label
            color_discrete_sequence=['#FF6F61']  # Changed color to a pleasant red-orange
        )
        st.plotly_chart(fig_duration, use_container_width=True)
        st.markdown('**Insight:** Most trips last between 5 and 10 minutes.')

    with col2:
        fig_distance = px.histogram(
            data, 
            x='trip_distance', 
            nbins=50, 
            title='Distribution of Trip Distance',
            labels={'trip_distance': 'Trip Distance (miles)'},  # Updated axis label
            color_discrete_sequence=['#6B5B95']  # Changed color to a soft purple
        )
        st.plotly_chart(fig_distance, use_container_width=True)
        st.markdown('**Insight:** The majority of trips are under 5 miles, with a few longer trips.')

    # Second row: Scatter Plot - Trip Duration vs Distance
    st.markdown('---')
    st.subheader("Trip Duration vs Distance")

    col1, col2 = st.columns([3, 1])

    with col1:
        fig_duration_distance = px.scatter(
            data, 
            x='trip_distance', 
            y='duration', 
            title='Relationship Between Trip Distance and Duration',
            labels={'trip_distance': 'Trip Distance (miles)', 'duration': 'Trip Duration (minutes)'},  # Updated axis labels
            color_discrete_sequence=['#88B04B']  # Changed color to a fresh green
        )
        st.plotly_chart(fig_duration_distance, use_container_width=True)

    with col2:
        st.markdown('''
        **Key Observations:**
        - Longer distances tend to result in longer durations, as expected.
        - However, some trips take unexpectedly longer times for shorter distances, which could be due to traffic conditions or inefficiencies.
        ''')

    # Third row: Line Plots for Average Duration and Distance by Hour
    st.markdown('---')
    st.subheader("Trip Duration and Distance by Time of Day")
    
    col1, col2 = st.columns(2)

    with col1:
        avg_duration_by_hour = data.groupby('hour')['duration'].mean().reset_index()
        fig_duration_by_hour = px.line(
            avg_duration_by_hour, 
            x='hour', 
            y='duration', 
            title='Average Trip Duration by Hour of the Day',
            labels={'hour': 'Hour of the Day', 'duration': 'Average Trip Duration (minutes)'},  # Updated axis labels
            line_shape='spline',  # Smooth the line for better aesthetics
            color_discrete_sequence=['#F7CAC9']  # Changed color to a light pink
        )
        st.plotly_chart(fig_duration_by_hour, use_container_width=True)
        st.markdown('**Insight:** Trips tend to take longer during the afternoon.')

    with col2:
        avg_distance_by_hour = data.groupby('hour')['trip_distance'].mean().reset_index()
        fig_distance_by_hour = px.line(
            avg_distance_by_hour, 
            x='hour', 
            y='trip_distance', 
            title='Average Trip Distance by Hour of the Day',
            labels={'hour': 'Hour of the Day', 'trip_distance': 'Average Trip Distance (miles)'},  # Updated axis labels
            line_shape='spline',  # Smooth the line
            color_discrete_sequence=['#92A8D1']  # Changed color to a light blue
        )
        st.plotly_chart(fig_distance_by_hour, use_container_width=True)
        st.markdown('**Insight:** The average trip distance increases around 4 AM.')

    st.markdown('---')

    # Add a conclusion at the end of the section
    st.subheader("Summary of Trip Duration and Distance Analysis")
    st.markdown('''
    - The majority of Uber trips are short, typically lasting between 5 to 10 minutes and covering less than 5 miles.
    - As expected, there is a positive correlation between trip distance and duration; longer trips tend to take more time.
    - However, there are some cases where shorter trips take unexpectedly long, which could be influenced by factors such as traffic or route inefficiencies.
    - The data suggests that trips generally take longer during the afternoon hours, indicating potential peak traffic times.
    - Interestingly, the average trip distance shows a slight increase around 4 AM, possibly linked to fewer drivers on the road and longer late-night journeys.
    ''')

    st.markdown('---')

def time_and_location_analysis(data):
    # Title
    center_h2('3. Time and Location Analysis')

    # Brief Introduction
    st.markdown("In this section, we analyze the impact of time and location on trip behavior, looking at patterns across hours of the day and trip start and end locations.")

    # First row: Trip Count by Hour
    st.markdown('---')
    st.subheader("Trip Count by Hour of the Day")
    
    trip_count_by_hour = data.groupby('hour')['duration'].count().reset_index()
    
    fig_trip_count_by_hour = px.bar(
        trip_count_by_hour, 
        x='hour', 
        y='duration', 
        title='Number of Trips by Hour of the Day',
        labels={'hour': 'Hour of the Day', 'duration': 'Number of Trips'},  # Updated axis labels
        color_discrete_sequence=['#FFB347']  # Warm orange tone
    )
    
    st.plotly_chart(fig_trip_count_by_hour, use_container_width=True)
    st.markdown('**Insight:** Most trips occur during the late afternoon and evening, indicating high activity during commute hours.')

    # Second row: Pickup Locations - Scatter Plot
    st.markdown('---')
    col1, col2 = st.columns(2)

    # Geographical Distribution of Pickup Locations
    with col1:
        st.subheader("Geographical Distribution of Pickup Locations")
        
        # Use latitude, longitude for scatter plot of pickup locations, and color based on the time of day (hour)
        fig_pickup_locations = px.scatter_mapbox(
            data, 
            lat="pickup_latitude", 
            lon="pickup_longitude", 
            color='hour',  # Color based on time of day
            color_continuous_scale='Sunsetdark',  # Use a color scale representing day-night cycle
            title="Geographical Distribution of Pickup Locations by Time of Day",
            labels={
                'pickup_latitude': 'Pickup Latitude', 
                'pickup_longitude': 'Pickup Longitude',
                'hour': 'Hour of the Day'
            },  # Updated axis labels
            mapbox_style="open-street-map",  # Use an open street map for a better visual
            zoom=10,
            height=500
        )
        
        st.plotly_chart(fig_pickup_locations, use_container_width=True)
        st.markdown('**Insight:** Pickup locations are colored based on the hour of the day, providing a temporal view of activity patterns across the city.')

    # Geographical Distribution of Dropoff Locations
    with col2:
        st.subheader("Geographical Distribution of Dropoff Locations")
        
        # Use latitude, longitude for scatter plot of dropoff locations, and color based on the time of day (hour)
        fig_dropoff_locations = px.scatter_mapbox(
            data, 
            lat="dropoff_latitude", 
            lon="dropoff_longitude", 
            color='hour',  # Color based on time of day
            color_continuous_scale='Sunsetdark',  # Another continuous color scale for contrast
            title="Geographical Distribution of Dropoff Locations by Time of Day",
            labels={
                'dropoff_latitude': 'Dropoff Latitude', 
                'dropoff_longitude': 'Dropoff Longitude',
                'hour': 'Hour of the Day'
            },  # Updated axis labels
            mapbox_style="open-street-map",  # Use the same open street map style
            zoom=10,
            height=500
        )
        
        st.plotly_chart(fig_dropoff_locations, use_container_width=True)
        st.markdown('**Insight:** Dropoff locations are colored by hour, revealing how dropoff patterns vary throughout the day, particularly in central and peripheral areas.')


    st.markdown('---')

    # Add a conclusion at the end of the section
    st.subheader("Summary of Time and Location Analysis")
    st.markdown('''
    - Uber trips are most frequent during the afternoon and early evening, coinciding with commute hours.
    - The majority of pickups and dropoffs occur in central locations, with a high density of trips in urban hubs.
    - There is a slight dispersal of dropoff locations, possibly reflecting longer trips from the central urban areas to peripheral regions.
    ''')

def passenger_count_and_earnings(data):
    # Title
    center_h2('4. Passenger Count and Earnings')

    # Brief Introduction
    st.markdown("In this section, we explore how the number of passengers affects trip earnings, looking at the relationship between passenger count, total fare, and tips.")

    # First row: Distribution of Passenger Count
    st.markdown('---')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribution of Passenger Count")
        
        fig_passenger_count = px.histogram(
            data, 
            x='passenger_count', 
            nbins=6, 
            title='Distribution of Passenger Count per Trip',
            labels={'passenger_count': 'Number of Passengers'},  # Updated axis label
            color_discrete_sequence=['#4C9F70']  # Pleasant green color
        )
        st.plotly_chart(fig_passenger_count, use_container_width=True)
        st.markdown('**Insight:** Most trips have 1 or 2 passengers, with very few trips carrying 5 or more passengers.')

    with col2:
        st.subheader("Percentage of Rides with Tips by Passenger Count")

        # Calculate the percentage of rides with tips for each passenger count
        data['has_tip'] = data['tip_amount'] > 0  # Create a boolean column to indicate if a tip was given
        percentage_tips_by_passenger = data.groupby('passenger_count')['has_tip'].mean().reset_index()
        percentage_tips_by_passenger['has_tip'] *= 100  # Convert to percentage

        # Create a bar chart to show the percentage of rides with tips for each passenger count
        fig_percentage_tips = px.bar(
            percentage_tips_by_passenger,
            x='passenger_count',
            y='has_tip',
            title='Percentage of Rides with Tips by Passenger Count',
            labels={'passenger_count': 'Number of Passengers', 'has_tip': 'Percentage of Rides with Tips (%)'},  # Updated axis labels
            color_discrete_sequence=['#4C9F70'],  # Pleasant green color
            height=500
        )

        st.plotly_chart(fig_percentage_tips, use_container_width=True)
        st.markdown('**Insight:** In general about 60% of trips give a tip. Trips with 2, 3 and 4 passengers tend to give tips slightly less often.')

    # Second row: Box Plot for Total Fare by Passenger Count
    st.markdown('---')
    st.subheader("Total Fare by Passenger Count")
    
    fig_fare_by_passengers = px.box(
        data, 
        x='passenger_count', 
        y='total_amount', 
        title='Total Fare Distribution by Passenger Count',
        labels={'passenger_count': 'Number of Passengers', 'total_amount': 'Total Fare (USD)'},  # Updated axis labels
        color_discrete_sequence=['#FFA07A']  # Light salmon color
    )
    st.plotly_chart(fig_fare_by_passengers, use_container_width=True)
    st.markdown('**Insight:** While trips with more passengers tend to have higher fares, there are a few outliers with high fares even for trips with fewer passengers.')

    # Third row: Scatter Plot for Total Fare vs Tip Amount by Passenger Count
    st.markdown('---')
    st.subheader("Total Fare vs Tip Amount by Passenger Count")
    
    fig_fare_vs_tip = px.scatter(
        data, 
        x='total_amount', 
        y='tip_amount', 
        color='passenger_count', 
        title='Total Fare vs Tip Amount by Passenger Count',
        labels={'total_amount': 'Total Fare (USD)', 'tip_amount': 'Tip Amount (USD)', 'passenger_count': 'Number of Passengers'},  # Updated axis labels
        color_continuous_scale='Agsunset',  # Continuous color scale based on passenger count
        height=500
    )
    st.plotly_chart(fig_fare_vs_tip, use_container_width=True)
    st.markdown('''
    **Key Observations:**
    - Trips with higher fares tend to receive higher tips.
    - There’s a strong positive correlation between total fare and tip amount, regardless of passenger count.
    - Larger groups (3+ passengers) tend to have slightly higher fares and tips, but the relationship remains consistent across group sizes.
    ''')

    # Fourth row: Average Tip Amount by Passenger Count (Bar Plot)
    st.markdown('---')
    st.subheader("Average Tip Amount by Passenger Count")
    
    avg_tip_by_passenger = data.groupby('passenger_count')['tip_amount'].mean().reset_index()
    fig_avg_tip_by_passenger = px.bar(
        avg_tip_by_passenger, 
        x='passenger_count', 
        y='tip_amount', 
        title='Average Tip Amount by Passenger Count',
        labels={'passenger_count': 'Number of Passengers', 'tip_amount': 'Average Tip Amount (USD)'},  # Updated axis labels
        color_discrete_sequence=['#87CEEB'],  # Sky blue color for the bar chart
        height=500
    )
    st.plotly_chart(fig_avg_tip_by_passenger, use_container_width=True)
    st.markdown('**Insight:** Trips with 2 or more passengers generally yield higher tips compared to single-passenger trips.')

    st.markdown('---')

    # Add a conclusion at the end of the section
    st.subheader("Summary of Passenger Count and Earnings Analysis")
    st.markdown('''
    - Most Uber trips have 1 or 2 passengers, with very few trips involving larger groups.
    - While more passengers generally lead to higher total fares, the relationship between total fare and tip amount remains fairly consistent across passenger counts.
    - Trips with more passengers tend to receive higher tips, suggesting a correlation between group size and tipping behavior.
    ''')

def revenue_maximization_factors(data):
    # Title
    center_h2('5. Revenue Maximization Factors')

    # Brief Introduction
    st.markdown("In this section, we explore the key factors that influence revenue, focusing on the relationships between trip distance, duration, passenger count, and total fare.")

    # First row: Scatter Plot - Total Fare vs Trip Distance (colored by duration)
    st.markdown('---')
    st.subheader("Total Fare vs Trip Distance (Colored by Trip Duration)")
    
    fig_fare_vs_distance = px.scatter(
        data, 
        x='trip_distance', 
        y='total_amount', 
        color='duration', 
        title='Total Fare vs Trip Distance (Colored by Trip Duration)',
        labels={'trip_distance': 'Trip Distance (miles)', 'total_amount': 'Total Fare (USD)', 'duration': 'Trip Duration (minutes)'},  # Updated axis labels
        color_continuous_scale='Viridis',  # Color scale for duration
        height=500
    )
    st.plotly_chart(fig_fare_vs_distance, use_container_width=True)
    st.markdown('**Insight:** Longer trips tend to result in higher fares, but shorter trips with longer durations can also yield significant earnings.')

    # Second row: Average Total Fare by Hour of the Day
    st.markdown('---')
    st.subheader("Average Total Fare by Hour of the Day")
    
    avg_fare_by_hour = data.groupby('hour')['total_amount'].mean().reset_index()
    
    fig_avg_fare_by_hour = px.bar(
        avg_fare_by_hour, 
        x='hour', 
        y='total_amount', 
        title='Average Total Fare by Hour of the Day',
        labels={'hour': 'Hour of the Day', 'total_amount': 'Average Total Fare (USD)'},  # Updated axis labels
        color_discrete_sequence=['#FF6F61'],  # Pleasant red-orange color
        height=500
    )
    st.plotly_chart(fig_avg_fare_by_hour, use_container_width=True)
    st.markdown('**Insight:** Average fares are generally higher during late-night and early morning hours, suggesting that these times might yield higher earnings.')


    # Third row: Correlation Heatmap of Key Factors
    st.markdown('---')
    st.subheader("Correlation Heatmap of Key Factors Influencing Revenue")

    # Select relevant columns for correlation
    correlation_data = data[['total_amount', 'trip_distance', 'duration', 'passenger_count', 'fare_amount', 'tip_amount']]
    correlation_matrix = correlation_data.corr()

    fig_corr_heatmap = px.imshow(
        correlation_matrix, 
        title='Correlation Between Key Revenue Factors',
        labels={'color': 'Correlation'},
        color_continuous_scale='RdBu',  # Red-Blue color scale
        height=500
    )
    st.plotly_chart(fig_corr_heatmap, use_container_width=True)
    st.markdown('**Insight:** Total fare is strongly correlated with trip distance and duration, while passenger count has a weaker influence on overall earnings.')
    
    st.markdown('---')

    # Add a conclusion at the end of the section
    st.subheader("Summary of Revenue Maximization Factors")
    st.markdown('''
    - Longer trips and trips taken during late-night or early-morning hours generally yield higher fares.
    - Weekends, particularly Fridays and Saturdays, present peak opportunities for maximizing revenue.
    - Trip distance and duration are the strongest factors influencing total fare, while passenger count has a smaller impact.
    ''')

def optimization_insights(data):
    # Title
    center_h2('6. Optimization Insights')

    # Brief Introduction
    st.markdown("This section provides actionable insights based on our analysis to help Uber drivers optimize their operations for maximum revenue.")

    # First row: Optimal Times for Earnings
    st.markdown('---')
    st.subheader("Optimal Times for Earnings")

    avg_fare_by_hour = data.groupby('hour')['total_amount'].mean().reset_index()

    fig_optimal_times = px.bar(
        avg_fare_by_hour, 
        x='hour', 
        y='total_amount', 
        title='Average Earnings by Hour',
        labels={'hour': 'Hour of the Day', 'total_amount': 'Average Earnings (USD)'},
        color='total_amount',
        color_continuous_scale='Blues',
        height=500
    )
    st.plotly_chart(fig_optimal_times, use_container_width=True)
    st.markdown('**Insight:** Late-night and early morning hours typically yield the highest average earnings, suggesting these times as optimal for operation.')

        # Second row: Optimal Locations for Pickups and Dropoffs
    st.markdown('---')
    st.subheader("Optimal Locations for Pickups and Dropoffs")

    # Aggregate data to calculate average fare per pickup location
    avg_fare_by_location = data.groupby(['pickup_latitude', 'pickup_longitude'])['total_amount'].mean().reset_index()

    # Create a scatter mapbox plot for optimal pickup locations
    fig_optimal_locations = px.scatter_mapbox(
        avg_fare_by_location, 
        lat='pickup_latitude', 
        lon='pickup_longitude', 
        size='total_amount',  # Circle size represents the average fare
        color='total_amount',  # Color also represents average fare
        color_continuous_scale='Viridis',  # Color scale for visual differentiation
        mapbox_style="open-street-map",
        zoom=10,
        height=500,
        title='Optimal Pickup Locations for Maximizing Earnings'
    )
    st.plotly_chart(fig_optimal_locations, use_container_width=True)
    st.markdown('**Insight:** Certain locations consistently offer higher average fares, identifying them as strategic spots for pickups.')


    # Third row: Impact of Trip Distance on Earnings
    st.markdown('---')
    st.subheader("Impact of Trip Distance on Earnings")

    fig_distance_earnings = px.scatter(
        data,
        x='trip_distance',
        y='total_amount',
        title='Relationship Between Trip Distance and Earnings',
        labels={'trip_distance': 'Trip Distance (miles)', 'total_amount': 'Earnings (USD)'},
        height=500
    )
    st.plotly_chart(fig_distance_earnings, use_container_width=True)
    st.markdown('**Insight:** There is a positive correlation between trip distance and earnings, suggesting longer trips are generally more profitable.')

    # Fourth row: Advice on Passenger Count Management
    st.markdown('---')
    st.subheader("Advice on Passenger Count Management")

    avg_earnings_by_passenger = data.groupby('passenger_count')['total_amount'].mean().reset_index()

    fig_passenger_earnings = px.bar(
        avg_earnings_by_passenger,
        x='passenger_count',
        y='total_amount',
        title='Average Earnings by Passenger Count',
        labels={'passenger_count': 'Number of Passengers', 'total_amount': 'Average Earnings (USD)'},
        color='total_amount',
        color_continuous_scale='Reds',
        height=500
    )
    st.plotly_chart(fig_passenger_earnings, use_container_width=True)
    st.markdown('**Insight:** While earnings per trip increase with more passengers, strategies to attract groups of 2 could optimize earnings.')

    st.markdown('---')

    # Add a conclusion at the end of the section
    st.subheader("Summary of Optimization Insights")
    st.markdown('''
    - Operating during late-night and early morning hours can maximize earnings due to higher average fares.
    - Drivers should consider frequenting high-fare locations for pickups to increase earnings.
    - Longer trips tend to be more profitable, suggesting a focus on routes or areas that naturally lead to longer distances.
    - Managing passenger count by encouraging attract groups of 2 can potentially increase revenue.
    ''')

def conclusion(data):
    # Title
    center_h2('7. Conclusion and Strategic Recommendations')

    # Introduction to the conclusion
    st.markdown("After a thorough analysis of the Uber data, here are the key insights and strategic recommendations that can help Uber drivers maximize their earnings and improve operational efficiency.")

    # Highlight key findings
    st.markdown('---')
    st.subheader("Key Findings:")
    st.markdown('''
    - **Time Optimization:** The data indicates that late-night and early-morning hours yield higher average fares, suggesting these times are optimal for operation due to less competition and higher demand for rides.
    - **Location Strategy:** Certain geographic locations consistently offer higher average fares, particularly in downtown areas and near major transit hubs. Drivers should target these areas for pickups, especially during peak demand times.
    - **Trip Dynamics:** Longer trips not only increase the total fare but also tend to have higher tips. Drivers should consider routes or strategies that encourage longer trips to maximize their earnings.
    - **Passenger Dynamics:** While more passengers generally do not significantly increase the fare, attracting groups (especially duos) can optimize tips and overall trip efficiency.
    - **Efficiency and Scaling:** Implementing findings from the correlation analysis, trips with optimal durations and distances should be prioritized to ensure the highest returns on time and resource investment.
    ''')

    # Strategic Recommendations
    st.markdown('---')
    st.subheader("Strategic Recommendations:")
    st.markdown('''
    - **Schedule Adjustment:** Drivers should adjust their schedules to capitalize on high-demand hours, which are typically outside of standard business hours.
    - **Strategic Positioning:** Utilize data-driven positioning to start shifts in or migrate towards high-fare zones, particularly during special events or in areas with nightlife.
    - **Route Planning:** Focus on accepting rides that lead to or pass through high-fare areas to increase chances of lucrative fares and tips.
    - **Promotions and Incentives:** Consider engaging in Uber promotions that target times of low demand to maintain a steady income throughout the day or opt for strategies that maximize participation in high-demand periods.
    - **Customer Service Excellence:** Maintaining a high level of customer service can encourage higher tips, especially on longer trips where driver-passenger interaction is prolonged.
    ''')

    # Final Thoughts
    st.markdown('---')
    st.subheader("Final Thoughts:")
    st.markdown('''
    The analyses provided in this dashboard offer a roadmap to optimizing performance as an Uber driver. By strategically targeting high-yield hours and locations, and focusing on service quality, drivers can significantly enhance their earning potential. Continuous analysis and adaptation to emerging trends and patterns will be crucial for sustained success.
    ''')

    st.markdown('---')
    st.markdown("This comprehensive analysis aims to empower Uber drivers with data-driven insights to make informed decisions that enhance their efficiency and profitability.")


parts_of_analysis = {
    '1. Dataset Overview': dataset_overview,
    '2. Exploring Trip Duration and Distance': trip_duration_and_distance,
    '3. Time and Location Analysis': time_and_location_analysis,
    "4. Passenger Count and Earnings": passenger_count_and_earnings,
    "5. Revenue Maximization Factors": revenue_maximization_factors,
    "6. Optimization Insights": optimization_insights,
    "Conclusion": conclusion,
}


# Main dashboard function
def uberdata():
    # get the data
    data = get_data()
    title_and_intro(data)
    # Call each function to render respective sections
    selected_parts = st.selectbox('Select a part of the analysis', list(parts_of_analysis.keys()))
    parts_of_analysis[selected_parts](data)
    
