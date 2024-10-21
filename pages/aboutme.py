#pages/aboutme.py
import streamlit as st
from data.timelinedata import timeline_data
import pandas as pd
import plotly.express as px
from datalib.streamlitFunctions import center_text, center_h2, display_logo, center_h3
from config import GITHUB_LOGO, LINKEDIN_LOGO

globalpresentation = """
<div style="width: 100%; margin: 0; display: flex; justify-content: center; align-items: center;">
    <div style="text-align: center; width: 90%; background-color: #fff; padding: 30px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); border-radius: 10px;">
        <h1 style="font-size: 2.5em; margin-bottom: 0px;">👋 Hi, I'm Paul Zamanian 👋</h1>
        <p style="font-size: 1.2em; margin-bottom: 15px;">🇫🇷 A Passionate French computer science student</p>
        <p style="font-size: 1.2em; margin-bottom: 10px;">I have a strong interest in <strong>mathematics</strong>, <strong>statistics</strong>, and <strong>quantitative finance</strong>. 📊💡</p>
        <p style="font-size: 1.2em; margin-bottom: 10px;">I thrive on solving complex problems and making <strong>data-driven decisions</strong>.</p>
        <p style="font-size: 1.2em; margin-bottom: 10px;">🚀 My GitHub projects include:</p>
        <ul style="list-style: none; padding: 0; font-size: 1.2em; margin-bottom: 10px;">
            <li>🎮 <strong>Python games</strong></li>
            <li>📈🧠 <strong>Mathematical algorithms</strong> (graph theory, algorithmic trading)</li>
            <li>🌐 <strong>Full-stack websites</strong></li>
            <li>📊 <strong>Data analysis</strong></li>
            <li>🤖 <strong>Machine learning</strong></li>
        </ul>
        <p style="font-size: 1.2em; margin-bottom: 10px;">Some projects are private 🔒 as they were developed for companies.</p>
        <p style="font-size: 1.2em; margin-bottom: 10px;">👨‍💻✨ Check out my public work and passion on my <strong>GitHub</strong>! ✨👨‍💻</p>
    </div>
</div>
"""


# Define a function to create the timeline
def get_timeline():
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(timeline_data)

    # Create the timeline using Plotly Express
    fig = px.timeline(
        df, 
        x_start="Start", 
        x_end="End", 
        y="Task", 
        hover_data=["Description"],  # Show descriptions on hover
    )

    # Update the hovertemplate to show more personalized information
    fig.update_traces(
        hovertemplate=
        "<b style='font-size: 16px; color: blue;'>%{y}</b><br>" +  # Task name with blue color
        "<i>%{x|%Y-%m-%d}</i><br>" +  # Start date (formatted)
        "<br><span style='font-size: 12px;'>Description: %{customdata[0]}</span><br>"  # Description with specific font size
    )

    # Update the layout for better readability and larger fonts
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Experience",
        showlegend=False,
        height=600,
        xaxis_title_font_size=24,  # Font size for the x-axis title
        yaxis_title_font_size=24,  # Font size for the y-axis title
        xaxis_tickfont_size=18,  # Font size for x-axis ticks
        yaxis_tickfont_size=18,  # Font size for y-axis ticks
        margin=dict(l=50, r=50, t=80, b=50)  # Margins for better spacing
    )

    # Return the figure
    return fig

# Define a function to display the logos and connect with me
def connect_with_me():
    # Add centered section header
    center_h2("Connect with me:")

    # Display clickable logos
    col1, col2 = st.columns(2)
    with col1:
        display_logo(GITHUB_LOGO, "https://github.com/PaulZaman/", align='right', margin_top=10)
    with col2:
        display_logo(LINKEDIN_LOGO, "https://www.linkedin.com/in/paul-zamanian-data-finance/", align='left', width=70, height=70)

# About Me Page
def aboutme():
    # Add centered personal information
    st.markdown(globalpresentation, unsafe_allow_html=True)

    # Connect with me section
    connect_with_me()


    # Resume Section
    center_h2('Resume')
    center_text(
        """
        I have had the opportunity to engage in numerous experiences that merge my passion for computer science with my interest in financial markets. Throughout these experiences, I have developed a wide range of skills that I am eager to share. My journey has been one of continuous learning and application, and I look forward to further opportunities to grow and contribute.
        """
    )



    # Get the timeline figure and display it
    fig = get_timeline()
    st.plotly_chart(fig, use_container_width=True)

