import streamlit as st
from datalib.streamlitFunctions import center_h2, center_text, center_h1, center_h3
import pandas as pd
import plotly.express as px
import math
from st_aggrid import AgGrid

# Load Data Functions
def get_accidents_caracteristiques():
	caracteristiques = pd.read_parquet('data/accidents/caracteristiques_cleaned.parquet')
	return caracteristiques

def get_accidents_usagers():
	usagers = pd.read_parquet('data/accidents/usagers_cleaned.parquet')
	return usagers

def intro(caracteristiques, usagers):
	# Title and Subtitle with Styling
	center_h1('🚧 How to Avoid Road Accidents 🛑')
	center_text("An Analysis of Road Accidents Data in France (2005-2022)")
	
	# Adding a link with markdown for the dataset
	st.markdown(
		"""
		<div style='text-align: center'>
			<a href="https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2022/#/resources" target="_blank">🔗 Link to the dataset</a>
		</div>
		""", 
		unsafe_allow_html=True
	)

	# Overview Section with Columns for Layout
	st.markdown('---')

	center_h2("Dataset Overview")
	col1, col2, col3 = st.columns(3)
	
	with col1:
		center_h3("Accident Data Files:")
		center_text("1. The characteristics of the accidents")
		center_text("2. The users involved in the accidents")

	with col3:
		center_h3("Data Format:")
		center_text("The data is available in CSV format, divided by year.")
		center_text("We'll be using data from 2005 to 2020, concatenating the years into a single dataframe.")

	with col2:
		center_h3("Data Cleaning Steps 🧹")
		center_text("To ensure the data is consistent across all years, we will perform the following cleaning steps:")

		st.markdown(
			"""
			<div style='text-align: center'>
				<ul style='list-style-type: none; padding: 0;'>
					<li>📅 <strong>Date formats</strong>: Normalize date formats across different years.</li>
					<li>🏷️ <strong>Column renaming</strong>: Standardize column names across different files.</li>
					<li>🌍 <strong>Geographical data</strong>: Standardize latitude and longitude formats (decimal degrees).</li>
					<li>🗑️ <strong>Remove irrelevant columns</strong>.</li>
				</ul>
			</div>
			""", 
			unsafe_allow_html=True
		)
	st.markdown('---')


	col1, col2 = st.columns(2)
	# Displaying accident characteristics data
	with col1:
		center_h3("Sample Data from 'Accident Characteristics' 📊")
		AgGrid(caracteristiques.head(10), fit_columns_on_grid_load=True)
		st.markdown(
			"""
			<div style='text-align: left'>
				- <strong>num_acc</strong>: Unique accident identifier.<br>
				- <strong>mois</strong>: Month of the accident.<br>
				- <strong>jour</strong>: Day of the accident.<br>
				- <strong>hrmn</strong>: Time of the accident.<br>
				- <strong>lum</strong>: Lighting conditions (1: Daylight, 5: Night with lit public lighting).<br>
				- <strong>agg</strong>: Urban area classification (1: Rural, 9: Urban area with >300,000 inhabitants).<br>
				- <strong>int</strong>: Type of intersection (e.g., X-intersection, roundabout).<br>
				- <strong>atm</strong>: Weather conditions (1: Normal, 5: Fog/Smoke).<br>
				- <strong>col</strong>: Type of collision (1: Head-on, 7: No collision).<br>
				- <strong>lat/long</strong>: Geographical coordinates.<br>
				- <strong>dep</strong>: Department code (INSEE).<br>
				- <strong>annee</strong>: Year of the accident.
			</div>
			""", 
			unsafe_allow_html=True
		)

	# Displaying user data from accidents
	with col2:
		center_h3("Sample Data from 'Accident Users' 🧑‍🤝‍🧑")
		AgGrid(usagers.head(10), fit_columns_on_grid_load=True)

		st.markdown(
			"""
			<div style='text-align: left'>
				- <strong>num_acc</strong>: Accident identifier (matches the characteristics data).<br>
				- <strong>place</strong>: Position in the vehicle (driver, passenger).<br>
				- <strong>catu</strong>: User category (1: Driver, 2: Passenger, 3: Pedestrian).<br>
				- <strong>grav</strong>: Severity of injury (1: Unharmed, 2: Killed, 3: Hospitalized).<br>
				- <strong>sexe</strong>: Gender (1: Male, 2: Female).<br>
				- <strong>trajet</strong>: Purpose of trip (1: Home to work, 5: Leisure).<br>
				- <strong>an_nais</strong>: Year of birth.<br>
				- <strong>annee</strong>: Year of the accident.
			</div>
			""", 
			unsafe_allow_html=True
		)


	# Number of accidents per month-year
	st.markdown('---')

	center_h3(" 📊🚦 Number of Accidents Per Month-Year")
	# set date column
	caracteristiques['date'] = pd.to_datetime(caracteristiques['annee'].astype(str) + '-' + caracteristiques['mois'].astype(str) + '-' + caracteristiques['jour'].astype(str))

	# Extract month and year
	caracteristiques['month_year'] = caracteristiques['date'].dt.to_period('M')
	caracteristiques['month_year'] = caracteristiques['month_year'].astype(str)

	# Group data by month-year
	accidents_per_month_year = caracteristiques.groupby('month_year').size().reset_index(name='count')
	fig_bar = px.bar(
		accidents_per_month_year,
		x='month_year',
		y='count',
		title="",
		labels={'month_year': 'Month-Year', 'count': 'Number of Accidents'},
		template="plotly_dark",
		color='count',
		color_continuous_scale='Viridis'  # Color gradient based on count
	)

	# Customize the layout
	fig_bar.update_layout(
		title_font_size=24,
		title_x=0.5,
		xaxis_tickangle=-45,
		xaxis_title="Month-Year",
		yaxis_title="Number of Accidents",
		yaxis=dict(showgrid=False)      # Remove horizontal gridlines
	)

	# Show the plot
	st.plotly_chart(fig_bar, use_container_width=True)

	center_text("We can see that the number of accidents has increased over the years. It is interesting to see a current patern through the year, with more accidents happening right before the summer, and many right after the summer.")

def Summary_and_outline():
	st.markdown('---')
	center_h2("🚗 Accident Data Analysis Project Outline 🛑")

	center_text("""
	This project aims to explore trends, patterns, and risk factors related to road accidents. 
	The analysis is based on various dimensions such as time, location, weather conditions, and demographics.
	""")

	# Create columns for each part of the analysis
	columns = st.columns(7)

	# Time Frame Analysis
	with columns[0]:
		center_h3("🕒 1. Time Frame Analysis")
		st.markdown("""
		- 📅 Explore trends in accidents over months, days, and times of day.
		- ⏰ Identify peak accident times (e.g., weekends, holidays).
		""")

	# Location-Based Analysis
	with columns[1]:
		center_h3("📍 2. Location-Based Analysis")
		st.markdown("""
		- 🗺️ Analyze accidents across regions (departments).
		- 🏙️ Study the impact of lighting, urban vs. rural areas, and intersections.
		""")

	# Weather Conditions
	with columns[2]:
		center_h3("☔ 3. Weather Conditions")
		st.markdown("""
		- 🌧️ Analyze the effect of weather conditions (rain, fog, etc.) on accidents.
		- 🌦️ Cross-reference weather with time of day and location for insights.
		""")

	# Collision Analysis
	with columns[3]:
		center_h3("💥 4. Collision Analysis")
		st.markdown("""
		- 🚗💨 Study different types of collisions (head-on, rear-end, etc.).
		- ⚠️ Assess the impact of collisions on fatality rates.
		""")

	# Demographic Analysis
	with columns[4]:
		center_h3("👥 5. Demographic Analysis")
		st.markdown("""
		- 🚹🚺 Analyze how gender influences accident rates and injury severity.
		- 🌍 Cross-analyze with time, location, and weather conditions.
		""")

	# Vehicle and Occupant Positioning
	with columns[5]:
		center_h3("🛑 6. Vehicle and Occupant Positioning")
		st.markdown("""
		- 🪑 Study how the position of individuals in the vehicle affects injury severity.
		""")

	# Trip Purpose
	with columns[6]:
		center_h3("🚗 7. Trip Purpose")
		st.markdown("""
		- 🛣️ Explore how the purpose of the trip (commuting, leisure, etc.) correlates with accidents.
		""")


	# Ending call to action
	center_h2("🚦 Let's get started! 🚀")

def time_frame_analysis(caracteristiques, usagers):
	st.markdown("""
	This section explores accident trends over various time dimensions—months, days of the week, and hours of the day. Understanding these patterns can help in pinpointing high-risk periods and improving safety measures.
	""")

	# Extract additional time information (hour, day of the week)
	caracteristiques['hour'] = caracteristiques['hrmn'].astype(str).str[:2].astype(float)  # Extract hour
	caracteristiques['day_of_week'] = caracteristiques['date'].dt.dayofweek  # Monday=0, Sunday=6

	# Create 3 columns layout
	col1, col2, col3 = st.columns(3)

	# Number of accidents per month
	with col1:
		accidents_per_month = caracteristiques.groupby('mois').size().reset_index(name='count')
		# Mapping month numbers to names
		month_mapping = {
			1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
			7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
		}
		accidents_per_month['mois'] = accidents_per_month['mois'].map(month_mapping)

		center_h3("📅 Number of Accidents Per Month")

		fig_bar_month = px.bar(
			accidents_per_month,
			x='mois',
			y='count',
			title=" ",
			labels={'mois': 'Month', 'count': 'Number of Accidents'},
			template="plotly_dark",
			color='count',
			color_continuous_scale='Viridis'  # Color gradient based on count
		)

		# Customize the layout
		fig_bar_month.update_layout(
			title_font_size=24,
			title_x=0.5,
			xaxis_tickangle=-45,
			xaxis_title="Month",
			yaxis_title="Number of Accidents",
			yaxis=dict(showgrid=False)  # Remove horizontal gridlines
		)

		# Show the plot
		st.plotly_chart(fig_bar_month, use_container_width=True)
		st.markdown("""
		**Analysis:** The chart shows a fairly consistent number of accidents across months, with a slight increase in June/July and September/October. This could indicate seasonal variations possibly linked to weather changes or increased travel during holiday seasons.
		""")

	# Number of accidents per day of the week
	with col2:
		accidents_per_day = caracteristiques.groupby('day_of_week').size().reset_index(name='count')
		
		# Mapping days of the week for better readability
		day_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
		accidents_per_day['day_of_week'] = accidents_per_day['day_of_week'].map(day_mapping)
		center_h3("📅 Number of Accidents Per Day of the Week")
		fig_bar_day = px.bar(
			accidents_per_day,
			x='day_of_week',
			y='count',
			title=" ",
			labels={'day_of_week': 'Day of Week', 'count': 'Number of Accidents'},
			template="plotly_dark",
			color='count',
			color_continuous_scale='Bluered'  # Color gradient based on count
		)

		# Customize the layout
		fig_bar_day.update_layout(
			title_font_size=24,
			title_x=0.5,
			xaxis_tickangle=-45,
			xaxis_title="Day of the Week",
			yaxis_title="Number of Accidents",
			yaxis=dict(showgrid=False)  # Remove horizontal gridlines
		)

		# Show the plot
		st.plotly_chart(fig_bar_day, use_container_width=True)
		st.markdown("""
		**Analysis:** There is a clear peak in accidents on Fridays, suggesting increased activity and mobility as the week ends. The lower accident rates on weekends could reflect less commuter traffic and potentially more cautious driving habits.
		""")

	# Accidents per hour of the day
	with col3:
		accidents_per_hour = caracteristiques.groupby('hour').size().reset_index(name='count')
		center_h3("🕒 Number of Accidents Per Hour of the Day")
		fig_bar_hour = px.bar(
			accidents_per_hour,
			x='hour',
			title=" ",
			y='count',
			labels={'hour': 'Hour of Day', 'count': 'Number of Accidents'},
			template="plotly_dark",
			color='count',
			color_continuous_scale='Turbo'  # Color gradient based on count
		)

		# Customize the layout
		fig_bar_hour.update_layout(
			title_font_size=24,
			title_x=0.5,
			xaxis_tickangle=-45,
			xaxis_title="Hour",
			yaxis_title="Number of Accidents",
			yaxis=dict(showgrid=False)  # Remove horizontal gridlines
		)

		# Show the plot
		st.plotly_chart(fig_bar_hour, use_container_width=True)
		st.markdown("""
		**Analysis:** The hourly data shows significant peaks during evening rush hours, with the highest peak around 5 PM. This indicates that the majority of accidents occur when traffic density is highest, suggesting a need for increased traffic management during these times. We will further this analysis when checking the types of commutings that are more prone to accidents.
		""")

def location_based_analysis(caracteristiques, usagers):
	center_text("""
	This section focuses on understanding the geographic distribution of road accidents. We'll explore how different factors like urbanization, lighting conditions, and intersection types contribute to accident rates.
	""")

	# Create columns layout for different analyses
	col1, col2 = st.columns(2)

	# Analysis by Department
	with col1:
		center_h3("Accidents by Department")
		accidents_by_dept = caracteristiques.groupby('dep').size().reset_index(name='count').sort_values('count', ascending=False)
		fig_dept = px.bar(
			accidents_by_dept, 
			x='dep', 
			y='count', 
			title="",
			labels={'dep': 'Department', 'count': 'Number of Accidents'},
			template="plotly_dark",
			color='count',
			color_continuous_scale='Turbo'  # Color gradient based on count
		)

		st.plotly_chart(fig_dept, use_container_width=True)
		st.markdown("""
		**Analysis:** This chart ranks departments by the number of accidents, highlighting regions with higher accident frequencies. Departments with major urban centers or high traffic volumes often show more accidents.
		""")

	# Analysis by Urbanization
	with col2:
		center_h3("Accidents in Urban vs. Rural Areas")
		accidents_by_area = caracteristiques.groupby('agg').size().reset_index(name='count')
		area_mapping = {1: 'Rural', 2: 'Urban'}
		accidents_by_area['agg'] = accidents_by_area['agg'].map(area_mapping)
		fig_area = px.pie(
			accidents_by_area, 
			names='agg', 
			values='count', 
			title="",
			color_discrete_sequence=px.colors.sequential.RdBu,
			
		)
		st.plotly_chart(fig_area, use_container_width=True)
		st.markdown("""
		**Analysis:** The pie chart shows the distribution of accidents between urban and rural areas, providing insights into where interventions may be most needed.
		""")

	# Lighting Conditions Analysis
	
	col1, col2 = st.columns(2)
	with col1:
		center_h3("Impact of Lighting Conditions on Accidents")
		
		# Group data by lighting conditions and count the occurrences
		lighting_conditions = caracteristiques.groupby('lum').size().reset_index(name='count').sort_values('count', ascending=False)
		
		# Mapping numerical codes to descriptive labels
		light_mapping = {1: 'Daylight',2: 'Dusk or dawn',3: 'Night without public lighting',4: 'Night with public lighting not lit',5: 'Night with public lighting lit'}
		
		# Apply the mapping to the 'lum' column
		lighting_conditions['lum'] = lighting_conditions['lum'].map(light_mapping)

		# Handle missing values (if any exist outside the defined mapping)
		lighting_conditions = lighting_conditions.dropna(subset=['lum'])

		# Create bar plot with Plotly
		fig_light = px.bar(
			lighting_conditions,
			x='lum',
			y='count',
			title="",
			labels={'lum': 'Lighting Condition', 'count': 'Number of Accidents'},
			template="plotly_dark",
			color='count',
			color_continuous_scale='Viridis'  # Color gradient based on count
		)

		# Show the plot
		st.plotly_chart(fig_light, use_container_width=True)

		# Add analysis commentary
		st.markdown("""
		**Analysis:** This analysis highlights how different lighting conditions affect the frequency of accidents. Accidents under poor lighting conditions might suggest a need for better street lighting or reflective signage.
		""")

	# Intersection Type Analysis
	with col2:
		center_h3("Accidents by Type of Intersection")
		intersection_types = caracteristiques.groupby('int').size().reset_index(name='count').sort_values('count', ascending=False)
		int_mapping = {1: 'No Intersection', 2: 'X Intersection', 3: 'T Intersection', 4: 'Y Intersection', 5: 'Intersection with more than 4 branches',
				   6: 'Roundabout', 7: 'Square', 8: 'Railway crossing', 9: 'Other Intersection'}
		intersection_types['int'] = intersection_types['int'].map(int_mapping)
		fig_intersection = px.bar(
			intersection_types, 
			x='int', 
			y='count', 
			title="",
			labels={'int': 'Type of Intersection', 'count': 'Number of Accidents'},
			template="plotly_dark",
			color='count',
			color_continuous_scale='Viridis'  # Color gradient based on count
		)
		st.plotly_chart(fig_intersection, use_container_width=True)
		st.markdown("""
		**Analysis:** The bar chart provides insights into which types of intersections are most prone to accidents. This information can guide traffic flow improvements and signage enhancements.
		""")

	# Map Plot using lat/long
	center_h3("Geographical Distribution of Accidents")
	
	# Filter the data for non-null lat and long, and valid coordinates
	accidents_map = caracteristiques.dropna(subset=['lat', 'long'])
	accidents_map = accidents_map[(accidents_map['lat'] > -90) & (accidents_map['lat'] < 90) & 
								  (accidents_map['long'] > -180) & (accidents_map['long'] < 180)]
	
	accidents_map = accidents_map[
		(accidents_map['lat'].between(41, 51)) & 
		(accidents_map['long'].between(-5, 10))
	]
	
	sample_size = 5000
	# Sampling the data to reduce the number of points plotted
	if len(accidents_map) > sample_size:
		accidents_map = accidents_map.sample(n=sample_size)

		# Mapping from 'lum' codes to descriptive names (make sure these are correct)
	light_mapping = {
		1: 'Daylight',
		2: 'Dusk or dawn',
		3: 'Night without public lighting',
		4: 'Night with public lighting not lit',
		5: 'Night with public lighting lit'
	}
	accidents_map['light_condition'] = accidents_map['lum'].map(light_mapping)

	# Plot the map using open-street-map style (no token required)
	fig_map = px.scatter_mapbox(
			accidents_map,
			lat="lat",
			lon="long",
			color="light_condition",  # Use lighting condition as color
			color_discrete_sequence=px.colors.qualitative.Light24,  # A color palette that is easy to distinguish
			hover_name="num_acc",
			hover_data={"lat": False, "long": False, "light_condition": True},  # Customize hover data
			zoom=5,
			height=600,
			title="Map of Accident Locations by Lighting Condition"
		)
	fig_map.update_layout(
		mapbox_style="open-street-map",
		mapbox_zoom=5,
		mapbox_center={"lat": 46, "lon": 2.5},  # Centered on France
		margin={"r":0, "t":0, "l":0, "b":0}
	)
	st.plotly_chart(fig_map, use_container_width=True)
	
	col1, col2 = st.columns(2)
	with col1:
		center_h3("Analysis Overview:")
		st.markdown(
			"""
			<div style='text-align: center'>
				<ul style='list-style-type: none; padding: 0;'>
					<li>🌍 <strong>High Density Across France</strong>: Dense scatter of accidents indicating widespread traffic safety issues.</li>
					<li>🌙 <strong>Night-Time Insights</strong>: Significant accidents in areas with insufficient public lighting.</li>
					<li>🌆 <strong>Urban Concentration</strong>: High accident frequencies in major urban centers.</li>
				</ul>
			</div>
			""",
			unsafe_allow_html=True
		)

	with col2:
		center_h3("Key Insights and Recommendations:")
		st.markdown(
			"""
			<div style='text-align: center'>
				<ul style='list-style-type: none; padding: 0;'>
					<li>🔦 <strong>Enhance Lighting</strong>: Improve street lighting in poorly lit areas to reduce night-time accidents.</li>
					<li>🚦 <strong>Urban Safety Measures</strong>: Implement traffic management solutions in urban areas to mitigate risks.</li>
					<li>📊 <strong>Policy Implications</strong>: Use insights to develop targeted road safety strategies.</li>
				</ul>
			</div>
			""",
			unsafe_allow_html=True
		)

	center_h2("Key Takeaways and Recommendations:")
	st.markdown(
		"""
		<div style='text-align: center'>
			<ul style='list-style-type: none; padding: 0;'>
				<li>🏙️ <strong>Target High Accident Departments:</strong> Direct resources to departments with the highest numbers of accidents, focusing on the most affected areas like the 75 and the 13 to reduce rates effectively.</li>
				<li>🌃 <strong>Enhance Lighting in Critical Areas:</strong> Significantly increase street lighting in regions where accidents frequently occur at night without public lighting, notably in rural and suburban settings.</li>
				<li>🛣️ <strong>Redesign Hazardous Intersections:</strong> Prioritize the redesign of intersections where the majority of accidents occur, especially non-intersection areas and T-intersections, to facilitate safer traffic flow.</li>
				<li>🌆 <strong>Urban vs. Rural Safety Strategies:</strong> Develop differentiated safety strategies for urban (with a slight majority of accidents) and rural areas, addressing specific needs such as pedestrian safety in cities and road maintenance in the countryside.</li>
				<li>🔆 <strong>Focus on Dusk and Dawn:</strong> Implement targeted measures during dusk and dawn when visibility issues significantly increase accident risks, as shown by the spike in accidents during these times.</li>
				<li>🗺️ <strong>Utilize Geographical Data for Planning:</strong> Leverage detailed geographical distribution insights from the maps to plan interventions more effectively, ensuring resources are allocated where they are most needed.</li>
			</ul>
		</div>
		""",
		unsafe_allow_html=True
	)

def weather_conditions_analysis(caracteristiques, usagers):
	# Merge the dataframes on the accident identifier
	merged_data = pd.merge(caracteristiques, usagers.drop(columns=["annee"]), on='num_acc', how='right')

	center_text("The two following plots contain the same data. The first one is grouped by severity, while the second one is grouped by weather condition. This highlights the impact of weather conditions on accident severity.")

	col1, col2 = st.columns(2)

	weather_map = {1: 'Normal', 2: 'Light Rain', 3: 'Heavy Rain', 4: 'Snow/Hail', 5: 'Fog/Smoke', 6: 'Strong Wind/Storm', 7: 'Dazzling', 8: 'Cloudy', 9: 'Other'}
	severity_map = {1: 'Unharmed', 2: 'Killed', 3: 'Hospitalized', 4: 'Light Injury'}
	
	merged_data['Weather Condition'] = merged_data['atm'].map(weather_map)
	merged_data['Severity'] = merged_data['grav'].map(severity_map)

	# Severity distribution by Weather Condition
	severity_distribution = pd.crosstab(merged_data['Weather Condition'], merged_data['Severity'])

	# Create a crosstab of weather condition vs severity
	severity_distribution = pd.crosstab(merged_data['Weather Condition'], merged_data['Severity'])

	# Normalize the data to get percentages
	severity_distribution_percentage = severity_distribution.div(severity_distribution.sum(axis=1), axis=0) * 100

	# Reset the index to get the weather conditions as a column
	severity_distribution_percentage = severity_distribution_percentage.reset_index()

	# Convert from wide to long format for easier plotting
	severity_distribution_melted = severity_distribution_percentage.melt(id_vars='Weather Condition', 
																			var_name='Severity', 
																			value_name='Percentage')

	# Create the bar chart grouped by severity
	fig_severity = px.bar(
		severity_distribution_melted,
		x='Severity',
		y='Percentage',
		color='Weather Condition',
		title='',
		barmode='group',
		labels={'Percentage': 'Percentage of Accidents', 'Severity': 'Severity'},
		color_discrete_sequence=px.colors.qualitative.Set2
	)

	# Update layout
	fig_severity.update_layout(
		xaxis_title='Severity',
		yaxis_title='Percentage of Accidents',
		yaxis=dict(ticksuffix='%'),
		legend_title='Weather Condition'
	)

	with col1:
		center_h3("Percentage of Accident Severity by Weather Condition (Grouped by Severity)")
		st.plotly_chart(fig_severity, use_container_width=True)

	# Second plot: Grouped by Weather Condition
	fig_weather = px.bar(
		severity_distribution_melted,
		x='Weather Condition',
		y='Percentage',
		color='Severity',
		title='',
		barmode='group',
		labels={'Percentage': 'Percentage of Accidents', 'Weather Condition': 'Weather Condition'},
		color_discrete_sequence=px.colors.qualitative.Pastel
	)

	# Update layout
	fig_weather.update_layout(
		xaxis_title='Weather Condition',
		yaxis_title='Percentage of Accidents',
		yaxis=dict(ticksuffix='%'),
		legend_title='Severity'
	)
	with col2:
		center_h3("Percentage of Accident Severity by Weather Condition (Grouped by Weather)")
		st.plotly_chart(fig_weather, use_container_width=True)

	# Yearly analysis using 'annee'
	yearly_weather = pd.crosstab(merged_data['annee'], merged_data['Weather Condition'])
	fig_yearly = px.line(yearly_weather, title='')
	fig_yearly.update_layout(xaxis_title='Year', yaxis_title='Number of Accidents')
	with col1:
		center_h3("Yearly Analysis of Accidents by Weather Condition")
		st.plotly_chart(fig_yearly, use_container_width=True)

	for col in yearly_weather.columns:
		yearly_weather[col] = yearly_weather[col] / yearly_weather[col].iloc[0] * 100

	
	fig_yearly = px.line(yearly_weather, title='')
	fig_yearly.update_layout(xaxis_title='Year', yaxis_title='Number of Accidents')
	with col2:
		center_h3("Yearly Analysis of Accidents by Weather Condition (rebased)")
		st.plotly_chart(fig_yearly, use_container_width=True)

	st.markdown(
		"""
		<div style='text-align: center'>
			<ul style='list-style-type: none; padding: 0;'>
				<li>🌞 <strong>Clear Weather:</strong> Most accidents occur under normal weather conditions, highlighting everyday driving risks.</li>
				<li>🌧️ <strong>Adverse Weather:</strong> Heavy rain and fog significantly increase the risk of severe accidents, suggesting the need for enhanced weather-adaptive traffic management systems.</li>
				<li>🌬️ <strong>Wind and Storm:</strong> While less common, strong wind conditions pose serious risks, especially on open roads and highways.</li>
			</ul>
		</div>
		""",
		unsafe_allow_html=True
	)

def collision_analysis(caracteristiques, usagers):
	# Merge the dataframes on the accident identifier
	merged_data = pd.merge(caracteristiques, usagers.drop(columns=["annee"]), on='num_acc', how='right')

	# Map for collision types (col)
	collision_map = {
		1: 'Two vehicles - head-on', 
		2: 'Two vehicles - rear-end', 
		3: 'Two vehicles - side impact', 
		4: 'Chain collision (3+ vehicles)', 
		5: 'Multiple collisions (3+ vehicles)', 
		6: 'Other collision', 
		7: 'No collision'
	}

	# Map for weather conditions (atm)
	weather_map = {
		1: 'Normal', 
		2: 'Light Rain', 
		3: 'Heavy Rain', 
		4: 'Snow/Hail',
		5: 'Fog/Smoke',
		6: 'Strong Wind/Storm',
		7: 'Dazzling',
		8: 'Cloudy',
		9: 'Other'
	}

	# Map for severity (grav)
	severity_map = {1: 'Unharmed', 2: 'Killed', 3: 'Hospitalized', 4: 'Light Injury'}

	merged_data['Collision Type'] = merged_data['col'].map(collision_map)
	merged_data['Weather Condition'] = merged_data['atm'].map(weather_map)
	merged_data['Severity'] = merged_data['grav'].map(severity_map)

	col1, col2 = st.columns(2)

	# 1. Distribution of Collision Types
	with col1:
		center_h3("Distribution of Collision Types")
		collision_distribution = merged_data['Collision Type'].value_counts(normalize=True) * 100
		
		# Reset the index to convert the index into a column
		collision_distribution = collision_distribution.reset_index()
		collision_distribution.columns = ['Collision Type', 'Percentage']  # Renaming columns
		
		fig_collision = px.bar(collision_distribution, 
							   x='Collision Type', 
							   y='Percentage', 
							   labels={'Collision Type': 'Collision Type', 'Percentage': 'Percentage of Accidents'},
							   title='',
							   template='plotly_dark')
		fig_collision.update_layout(xaxis_tickangle=-45)
		st.plotly_chart(fig_collision, use_container_width=True)

	# 2. Severity of Accidents by Collision Type
	with col2:
		center_h3("Severity of Accidents by Collision Type")
		severity_collision_distribution = pd.crosstab(merged_data['Collision Type'], merged_data['Severity'])
		severity_collision_percentage = severity_collision_distribution.div(severity_collision_distribution.sum(axis=1), axis=0) * 100
		
		# Reset index and convert wide to long format
		severity_collision_melted = severity_collision_percentage.reset_index().melt(id_vars='Collision Type', 
																					 var_name='Severity', 
																					 value_name='Percentage')
		fig_severity = px.bar(severity_collision_melted, 
							  x='Collision Type', 
							  y='Percentage', 
							  color='Severity',
							  title='',
							  barmode='group', 
							  labels={'Percentage': 'Percentage of Accidents', 'Collision Type': 'Collision Type'},
							  template='plotly_dark')
		fig_severity.update_layout(xaxis_tickangle=-45)
		st.plotly_chart(fig_severity, use_container_width=True)



	# Yearly Trends of Collision Types
	with col1:
		center_h3("Yearly Trends of Collision Types")
		yearly_collision = pd.crosstab(merged_data['annee'], merged_data['Collision Type'])
		yearly_collision_percentage = yearly_collision.div(yearly_collision.sum(axis=1), axis=0) * 100
		yearly_collision_melted = yearly_collision_percentage.reset_index().melt(id_vars='annee', 
																				var_name='Collision Type', 
																				value_name='Percentage')
		fig_yearly_collision = px.line(yearly_collision_melted, 
									x='annee', 
									y='Percentage', 
									color='Collision Type', 
									title='',
									labels={'Percentage': 'Percentage of Accidents', 'annee': 'Year'},
									template='plotly_dark')
		st.plotly_chart(fig_yearly_collision, use_container_width=True)

	# Create a crosstab of Collision Type vs Weather Condition
	heatmap_data = pd.crosstab(merged_data['Collision Type'], merged_data['Weather Condition'])

	# Normalize the data by columns to see the proportion of each collision type per weather condition
	heatmap_data = heatmap_data.div(heatmap_data.sum(axis=0), axis=1)

	# Generate the heatmap
	fig = px.imshow(heatmap_data, 
					labels=dict(x="Weather Condition", y="Collision Type", color="Proportion"),
					x=heatmap_data.columns, 
					y=heatmap_data.index,
					aspect="auto",
					title="")
	fig.update_xaxes(side="bottom")

	fig.update_layout(
		xaxis_title='Weather Condition',
		yaxis_title='Collision Type',
		coloraxis_colorbar={
			'title': 'Proportion'
		}
	)
	with col2:
		center_h3("Proportion of Collision Types by Weather Conditions")
		# Display the heatmap in the Streamlit app
		st.plotly_chart(fig, use_container_width=True)

	# Conclusion with insights
	st.markdown(
		"""
		<div style='text-align: center'>
			<ul style='list-style-type: none; padding: 0;'>
				<li>🚗 <strong>Head-on Collisions:</strong> Once the most common type of accident in 2005, they have significantly reduced from 25% to 10% of accidents but still result in the most fatalities.</li>
				<li>🚙 <strong>Two-vehicle Side Impact:</strong> Currently the most frequent type of collision, with a tendency to occur more in dazzling and normal weather conditions. Over the years, the frequency of side impact and rear-end collisions has increased.</li>
				<li>🔗 <strong>Chain Collisions:</strong> Though less frequent, these collisions typically cause the least fatalities.</li>
				<li>🌦️ <strong>Weather Impact:</strong> Two-vehicle side impacts are more likely in dazzling and normal weather, whereas adverse weather conditions like heavy rain and fog tend to see more rear-end collisions.</li>
			</ul>
		</div>
		""",
		unsafe_allow_html=True
	)

def demographic_analysis(caracteristiques, usagers):
	# Merge the dataframes on the accident identifier
	merged_data = pd.merge(caracteristiques, usagers, on='num_acc', how='right')

	col1, col2 = st.columns(2)

	# Gender distribution in accidents
	with col1:
		center_h3("Gender Distribution in Accidents")
		gender_map = {1: 'Male', 2: 'Female'}
		merged_data['sexe'] = merged_data['sexe'].map(gender_map)

		fig_gender = px.pie(merged_data, names='sexe', title='Accidents by Gender',
							labels={'sexe': 'Gender'}, hole=0.4,
							color_discrete_sequence=px.colors.sequential.RdBu)
		st.plotly_chart(fig_gender, use_container_width=True)

	# Age distribution in accidents
	with col2:
		center_h3("Age Distribution in Accidents")
		# Ensure age data is cleaned and cast to appropriate type
		merged_data['age'] = pd.to_datetime('today').year - merged_data['an_nais']
		fig_age = px.histogram(merged_data, x='age', nbins=20,
							   title='',
							   labels={'age': 'Age'}, template='plotly_dark')
		fig_age.update_layout(xaxis_title='Age', yaxis_title='Count')
		st.plotly_chart(fig_age, use_container_width=True)

	# Severity of injuries by age
	with col1:
		center_h3("Severity of Injuries by Age")
		severity_map = {1: 'Unharmed', 2: 'Killed', 3: 'Hospitalized', 4: 'Light Injury'}
		merged_data['Severity'] = merged_data['grav'].map(severity_map)

		fig_severity_age = px.box(merged_data.sample(10000), x='Severity', y='age', color='Severity',
								title='',
								labels={'age': 'Age', 'Severity': 'Severity'})
		fig_severity_age.update_layout(xaxis_title='Severity', yaxis_title='Age')
		st.plotly_chart(fig_severity_age, use_container_width=True)

	# Severity of injuries by gender
	with col2:
		center_h3("Severity of Injuries by Gender")
		severity_gender_distribution = pd.crosstab(merged_data['sexe'], merged_data['Severity'], normalize='index') * 100
		fig_severity_gender = px.bar(severity_gender_distribution, barmode='group',
									title='',
									labels={'value': 'Percentage of Accidents', 'sexe': 'Gender', 'Severity': 'Severity'},
									template='plotly_dark')
		fig_severity_gender.update_layout(xaxis_title='Gender', yaxis=dict(ticksuffix='%'))
		st.plotly_chart(fig_severity_gender, use_container_width=True)

	center_h3("Collision Types by Gender")
	collision_map = {
		1: 'Two vehicles - head-on', 
		2: 'Two vehicles - rear-end', 
		3: 'Two vehicles - side impact', 
		4: 'Chain collision (3+ vehicles)', 
		5: 'Multiple collisions (3+ vehicles)', 
		6: 'Other collision', 
		7: 'No collision'
	}
	merged_data['Collision Type'] = merged_data['col'].map(collision_map)

	collision_gender_distribution = pd.crosstab(merged_data['Collision Type'], merged_data['sexe'], normalize='columns') * 100
	fig_collision_gender = px.bar(collision_gender_distribution, barmode='group',
									title='Collision Types by Gender (Normalized by Gender)',
									labels={'value': 'Percentage of Accidents', 'Collision Type': 'Collision Type'},
									template='plotly_dark')
	fig_collision_gender.update_layout(xaxis_tickangle=-45)
	st.plotly_chart(fig_collision_gender, use_container_width=True)

	# Conclusion with insights
	st.markdown(
		"""
		<div style='text-align: center'>
			<ul style='list-style-type: none; padding: 0;'>
				<li>👦👧 <strong>Gender Insights:</strong> Males are involved in more accidents than females, possibly reflecting higher exposure to driving or riskier driving behaviors.</li>
				<li>👴👵 <strong>Age Factors:</strong> Younger individuals tend to be involved in accidents more frequently, but severe outcomes like fatalities increase with age.</li>
				<li>🚑 <strong>Injury Severity:</strong> Older adults generally suffer more severe injuries in accidents, underscoring the need for targeted safety measures for this demographic.</li>
			</ul>
		</div>
		""",
		unsafe_allow_html=True
	)

def vehicle_positioning_analysis(caracteristiques, usagers):
	# Merge the dataframes on the accident identifier
	merged_data = pd.merge(caracteristiques, usagers, on='num_acc', how='left')

	# Mapping position in vehicle
	position_map = {
		1: 'Driver',
		2: 'Front Passenger',
		3: 'Rear Left',
		4: 'Rear Center',
		5: 'Rear Right',
		6: 'Middle Left',
		7: 'Middle Right',
		8: 'Other Position',
		9: 'Unspecified'
	}
	merged_data['Position in Vehicle'] = merged_data['place'].map(position_map)

	# Mapping severity
	severity_map = {1: 'Unharmed', 2: 'Killed', 3: 'Hospitalized', 4: 'Light Injury'}
	merged_data['Severity'] = merged_data['grav'].map(severity_map)

	col1, col2 = st.columns(2)

	# Distribution of Positions in Vehicle
	with col1:
		center_h3("Distribution of Positions in Vehicle")
		position_distribution = merged_data['Position in Vehicle'].value_counts(normalize=True) * 100
		fig_position = px.bar(position_distribution,
							  labels={'index': 'Position in Vehicle', 'value': 'Percentage'},
							  title='Positional Distribution of Occupants in Accidents')
		fig_position.update_layout(xaxis_title='Position in Vehicle', yaxis=dict(ticksuffix='%'))
		st.plotly_chart(fig_position, use_container_width=True)

	# Severity of Injuries by Position in Vehicle
	with col2:
		center_h3("Severity of Injuries by Position in Vehicle")
		severity_position_distribution = pd.crosstab(merged_data['Position in Vehicle'], merged_data['Severity'])
		severity_position_percentage = severity_position_distribution.div(severity_position_distribution.sum(axis=1), axis=0) * 100
		fig_severity_position = px.bar(severity_position_percentage.reset_index().melt(id_vars='Position in Vehicle'),
									   x='Position in Vehicle', y='value', color='Severity',
									   title='Severity of Injuries by Position in Vehicle',
									   barmode='group')
		fig_severity_position.update_layout(xaxis_tickangle=-45, yaxis=dict(ticksuffix='%'))
		st.plotly_chart(fig_severity_position, use_container_width=True)

	# Conclusion with insights
	st.markdown(
		"""
		<div style='text-align: center'>
			<ul style='list-style-type: none; padding: 0;'>
				<li>🚗 <strong>Driver:</strong> Drivers often have the highest involvement in accidents but tend to have better safety outcomes due to direct safety features like airbags.</li>
				<li>👥 <strong>Front Passenger:</strong> Front passengers are typically less protected compared to drivers, showing a higher incidence of severe injuries.</li>
				<li>👶 <strong>Rear Passengers:</strong> Children and other passengers in rear positions are generally safer in side-impact collisions but remain vulnerable in rear-end collisions.</li>
				<li>⚠️ <strong>Safety Recommendations:</strong> Enhancing vehicle safety measures for all seating positions can reduce the severity and frequency of injuries.</li>
			</ul>
		</div>
		""",
		unsafe_allow_html=True
	)

def trip_purpose_analysis(caracteristiques, usagers):
	# Merge the dataframes on the accident identifier
	merged_data = pd.merge(caracteristiques, usagers, on='num_acc', how='left')

	# Mapping trip purposes
	purpose_map = {
		1: 'Home to work',
		2: 'Home to school',
		3: 'Shopping',
		4: 'Professional',
		5: 'Leisure',
		6: 'Other',
		7: 'Unknown'
	}
	merged_data['Trip Purpose'] = merged_data['trajet'].map(purpose_map)

	# Mapping severity
	severity_map = {1: 'Unharmed', 2: 'Killed', 3: 'Hospitalized', 4: 'Light Injury'}
	merged_data['Severity'] = merged_data['grav'].map(severity_map)

	col1, col2 = st.columns(2)

	# Distribution of Trip Purposes
	with col1:
		center_h3("Distribution of Trip Purposes")
		purpose_distribution = merged_data['Trip Purpose'].value_counts(normalize=True) * 100
		fig_purpose = px.bar(purpose_distribution,
							 labels={'index': 'Trip Purpose', 'value': 'Percentage'},
							 title='Distribution of Trip Purposes in Accidents')
		fig_purpose.update_layout(xaxis_title='Trip Purpose', yaxis=dict(ticksuffix='%'))
		st.plotly_chart(fig_purpose, use_container_width=True)

	# Severity of Injuries by Trip Purpose
	with col2:
		center_h3("Severity of Injuries by Trip Purpose")
		severity_purpose_distribution = pd.crosstab(merged_data['Trip Purpose'], merged_data['Severity'])
		severity_purpose_percentage = severity_purpose_distribution.div(severity_purpose_distribution.sum(axis=1), axis=0) * 100
		fig_severity_purpose = px.bar(severity_purpose_percentage.reset_index().melt(id_vars='Trip Purpose'),
									  x='Trip Purpose', y='value', color='Severity',
									  title='Severity of Injuries by Trip Purpose',
									  barmode='group')
		fig_severity_purpose.update_layout(xaxis_tickangle=-45, yaxis=dict(ticksuffix='%'))
		st.plotly_chart(fig_severity_purpose, use_container_width=True)

	center_h3("Distribution of Trip Purposes by Gender")
	gender_map = {1:"Male", 2:"Female"}
	merged_data['Gender'] = merged_data['sexe'].map(gender_map)
	
	# Normalize by gender
	trip_gender_distribution = pd.crosstab(merged_data['Trip Purpose'], merged_data['Gender'], normalize='columns') * 100
	
	# Create the bar plot
	fig_trip_gender = px.bar(trip_gender_distribution.reset_index().melt(id_vars='Trip Purpose'),
							x='Trip Purpose', y='value', color='Gender',
							title='Distribution of Trip Purposes by Gender (Normalized by Gender)',
							labels={'value': 'Percentage', 'Gender': 'Gender'},
							barmode='group')
	fig_trip_gender.update_layout(xaxis_tickangle=-45, yaxis=dict(ticksuffix='%'))
	st.plotly_chart(fig_trip_gender, use_container_width=True)


	# Conclusion with insights
	st.markdown(
		"""
		<div style='text-align: center'>
			<ul style='list-style-type: none; padding: 0;'>
				<li>🏢 <strong>Home to Work:</strong> High volume of trips but relatively safer due to routine paths and timings.</li>
				<li>🏫 <strong>Home to School:</strong> Needs special attention for improving safety, especially during peak school hours.</li>
				<li>🛒 <strong>Shopping and Leisure:</strong> Varied risks, often influenced by time of day and week.</li>
				<li>🔧 <strong>Professional:</strong> Linked with higher speeds and therefore potentially more severe accidents.</li>
			</ul>
		</div>
		""",
		unsafe_allow_html=True
	)

def calculate_risk(hour, gender, department, urban_rural, weather, age, trip_reason, caracteristiques, usagers):
# Normalize each risk to be between 0 and 1

	# Hour risk
	hour = int(hour.split(":")[0]) if hour != "Any" else "Any"
	caracteristiques['hour'] = caracteristiques['hrmn'].apply(lambda x: int(str(x).split(":")[0]))
	grouped_hour = caracteristiques.groupby('hour')['num_acc'].count()
	grouped_hour = grouped_hour / grouped_hour.sum()
	hour_risk = (grouped_hour[hour] - grouped_hour.min()) / (grouped_hour.max() - grouped_hour.min()) if hour in grouped_hour.index else grouped_hour.mean()

	# Gender risk
	grouped_sexe = usagers.groupby('sexe')['num_acc'].count()
	grouped_sexe = grouped_sexe / grouped_sexe.sum()
	gender_risk = (grouped_sexe.iloc[1 if gender == "Male" else 2] - grouped_sexe.min()) / (grouped_sexe.max() - grouped_sexe.min()) if gender in ['Male', 'Female'] else grouped_sexe.mean()

	# Department risk
	grouped_department = caracteristiques.groupby('dep')['num_acc'].count()
	grouped_department = grouped_department / grouped_department.sum()
	department_risk = (grouped_department[int(department)] - grouped_department.min()) / (grouped_department.max() - grouped_department.min()) if department in grouped_department.index else grouped_department.mean()

	# Urban/Rural risk
	grouped_urban_rural = caracteristiques.groupby('agg')['num_acc'].count()
	grouped_urban_rural = grouped_urban_rural / grouped_urban_rural.sum()
	urban_rural_risk = (grouped_urban_rural[2 if urban_rural == "Urban" else 1] - grouped_urban_rural.min()) / (grouped_urban_rural.max() - grouped_urban_rural.min()) if urban_rural in ['Urban', 'Rural'] else grouped_urban_rural.mean()

	# Weather risk
	weather_map = {1: 'Normal', 2: 'Light Rain', 3: 'Heavy Rain', 4: 'Snow/Hail', 5: 'Fog/Smoke', 6: 'Strong Wind/Storm', 7: 'Dazzling', 8: 'Cloudy', 9: 'Other'}
	caracteristiques['Weather Condition'] = caracteristiques['atm'].map(weather_map)
	grouped_weather = caracteristiques.groupby('Weather Condition')['num_acc'].count()
	grouped_weather = grouped_weather / grouped_weather.sum()
	weather_risk = (grouped_weather[weather] - grouped_weather.min()) / (grouped_weather.max() - grouped_weather.min()) if weather in grouped_weather.index else grouped_weather.mean()

	# Age risk
	usagers['Age'] = pd.to_datetime('today').year - usagers['an_nais']
	usagers['Age Group'] = pd.cut(usagers['Age'], bins=[0, 14, 17, 24, 34, 44, 54, 64, 74, 100], labels=['0-14', '15-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+'])
	grouped_age = usagers.groupby('Age Group')['num_acc'].count()
	grouped_age = grouped_age / grouped_age.sum()
	age_risk = (grouped_age[age] - grouped_age.min()) / (grouped_age.max() - grouped_age.min()) if age in grouped_age.index else grouped_age.mean()

	# Trip Purpose risk
	trip_map = {1: 'Home to work', 2: 'Home to school', 3: 'Shopping', 4: 'Professional', 5: 'Leisure', 6: 'Other', 7: 'Unknown'}
	usagers['Trip Purpose'] = usagers['trajet'].map(trip_map)
	grouped_trip = usagers.groupby('Trip Purpose')['num_acc'].count()
	grouped_trip = grouped_trip / grouped_trip.sum()
	trip_risk = (grouped_trip[trip_reason] - grouped_trip.min()) / (grouped_trip.max() - grouped_trip.min()) if trip_reason in grouped_trip.index else grouped_trip.mean()

	# Calculate total risk score using a weighted sum to ensure the score is between 0 and 1
	total_risk = (0.15 * hour_risk + 0.15 * gender_risk + 0.15 * department_risk +
				  0.15 * urban_rural_risk + 0.15 * weather_risk + 0.15 * age_risk + 
				  0.1 * trip_risk)
	
	return (
		hour_risk,
		gender_risk,
		department_risk,
		urban_rural_risk,
		weather_risk,
		age_risk,
		trip_risk,
		total_risk
	)


def conclusion(caracteristiques, usagers):
		# Heading for the conclusion page
	center_h2("🚦 Final Takeaways for Safe Driving 🚗")
	# Beautifully structured conclusion text
	st.markdown("""
	<div style='text-align: center;'>
		<p><strong>🚗 Take particular caution when:</strong></p>
		<ul style='list-style-type: none; padding: 0;'>
			<li>📅 <strong>Driving on Fridays</strong>: Accidents peak as the week winds down.</li>
			<li>⏰ <strong>Driving between 17:00 and 19:00</strong>: Peak hours for accidents, likely due to rush hour.</li>
			<li>🌞 <strong>Driving in June and July</strong>: Holiday traffic and seasonal trends lead to more accidents.</li>
			<li>📍 <strong>Driving in the 75 (Paris) and the 13 (Marseille)</strong>: These departments show the highest number of accidents.</li>
			<li>🏙️ <strong>Driving in urban areas</strong>: Heavier traffic increases the chances of accidents.</li>
			<li>🌫️ <strong>Driving in fog, smoke, or storms</strong>: These weather conditions are the main causes of deadly accidents.</li>
			<li>🔄 <strong>Handling side impacts</strong>: Side impacts are the most common type of accident.</li>
			<li>🚧 <strong>Accidents without collisions</strong>: "Sortie de route" and similar incidents lead to the most deaths.</li>
		</ul>
		<p><strong>🧍 Personal risk factors:</strong></p>
		<ul style='list-style-type: none; padding: 0;'>
			<li>👨 <strong>If you are a man</strong>: Men face a higher risk of death in accidents.</li>
			<li>🎂 <strong>If you are between 30 and 40</strong>: More likely to be involved in an accident.</li>
			<li>👴 <strong>If you are over 40</strong>: Increased risk of death if involved in an accident.</li>
			<li>🛣️ <strong>If you are driving for leisure</strong>: Higher chance of both accidents and fatalities.</li>
		</ul>
	</div>
	""", unsafe_allow_html=True)

	center_h2("🚗 Driving Risk Calculator")
	# User inputs
	cols = st.columns(7)
	with cols[0]:
		hour = st.selectbox('What hour is it going to be?', ["Any"] + [f"{i}:00" for i in range(24)])
	with cols[1]:
		gender = st.selectbox('Select your gender', ["Any", 'Male', 'Female'])
	with cols[2]:
		department = st.selectbox('Enter your department number', ["Any"] + list(caracteristiques['dep'].unique()))
	with cols[3]:
		urban_rural = st.selectbox('Is it an urban or rural area?', ['Any', 'Urban', 'Rural'])
	with cols[4]:
		weather = st.selectbox('Select the weather conditions', ['Any', 'Normal', 'Light Rain', 'Heavy Rain', 'Snow/Hail', 'Fog/Smoke', 'Strong Wind/Storm', 'Dazzling', 'Cloudy', 'Other'])
	with cols[5]:
		age = st.selectbox('Enter your age', ['Any', '0-14','15-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+'])
	with cols[6]:
		trip_reason = st.selectbox('Reason for travelling', ["Any", 'Leisure', 'Work', 'Professional', 'Other'])

	# Calculate risk
	hour_risk, gender_risk, department_risk, urban_rural_risk, weather_risk, age_risk, trip_risk, total_risk = calculate_risk(hour, gender, department, urban_rural, weather, age, trip_reason, caracteristiques, usagers)

		# Function to format and color the risks
	def format_risk(risk_value):
		# Round to 3 digits
		risk_value = round(risk_value, 1)

		
		# Apply color based on risk level
		if risk_value < 33:
			color = 'green'
		elif risk_value < 55:
			color = 'orange'
		else:
			color = 'red'
		
		# Return the formatted string with color
		return f"<span style='color:{color}'>{risk_value}%</span>"
	
	# Display the risk scores in different columns with colors
	with cols[0]:
		st.markdown(f"**Hour Risk:** {format_risk(hour_risk*100)}", unsafe_allow_html=True)
	with cols[1]:
		st.markdown(f"**Gender Risk:** {format_risk(gender_risk*100)}", unsafe_allow_html=True)
	with cols[2]:
		st.markdown(f"**Department Risk:** {format_risk(department_risk*100)}", unsafe_allow_html=True)
	with cols[3]:
		st.markdown(f"**Urban/Rural Risk:** {format_risk(urban_rural_risk*100)}", unsafe_allow_html=True)
	with cols[4]:
		st.markdown(f"**Weather Risk:** {format_risk(weather_risk*100)}", unsafe_allow_html=True)
	with cols[5]:
		st.markdown(f"**Age Risk:** {format_risk(age_risk*100)}", unsafe_allow_html=True)
	with cols[6]:
		st.markdown(f"**Trip Purpose Risk:** {format_risk(trip_risk*100)}", unsafe_allow_html=True)
	



	# Output risk result
	center_h3("Total Risk Score : " +format_risk(total_risk*100) )

	"""# Customize result display
	if risk_percentage < 30:
		st.success("Low risk 🚗")
	elif 30 <= risk_percentage < 70:
		st.warning("Medium risk ⚠️")
	else:
		st.error("High risk 🚨")"""
	
	with st.expander("ℹ️ How is the risk calculated?"):
		st.write("""
		- **Hour Risk**: Compares the selected hour's accident frequency to the average.
		- **Gender Risk**: Compares the selected gender accident frequency to the average.
		- **Department Risk**: Compares the selected department's accident frequency to the average.
		- **Urban/Rural Risk**: Compares the selected area's accident frequency to the average.
		- **Weather Risk**: Compares the selected weather condition's accident frequency to the average.
		- **Age Risk**: Compares the selected age group's accident frequency to the average.
		- **Trip Purpose Risk**: Compares the selected trip purpose's accident frequency to the average.
		- **Total Risk**: Combines all individual risks to calculate the total risk score. The higher the score, the higher the risk. The score is then log-transformed for better interpretation.
		""")

# Create a dictionary to link titles to functions
analysis_parts = {
	"🕒 1. Time Frame Analysis": time_frame_analysis,
	"📍 2. Location-Based Analysis": location_based_analysis,
	"☔ 3. Weather Conditions Analysis": weather_conditions_analysis,
	"💥 4. Collision Analysis": collision_analysis,
	"👥 5. Demographic Analysis": demographic_analysis,
	"🛑 6. Vehicle and Occupant Positioning": vehicle_positioning_analysis,
	"🚗 7. Trip Purpose Analysis": trip_purpose_analysis,
	"🔚 8. Conclusion": conclusion
}



# Main Accident Page Function
def accidents():
	caracteristiques = get_accidents_caracteristiques()
	usagers = get_accidents_usagers()
	

	intro(caracteristiques, usagers)
	Summary_and_outline()
	selected_part = st.selectbox("Choose a section to explore:", list(analysis_parts.keys()))
	st.markdown('---')
	# Display the corresponding function based on the user's selection
	center_h1(selected_part)
	analysis_parts[selected_part](caracteristiques, usagers)
	