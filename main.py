# main.py
# streamlit run --server.fileWatcherType="poll"

import streamlit as st
from config import PAGE_TITLE, TAB_TITLE, FAVICON_LOGO
from streamlit_option_menu import option_menu
from datalib.streamlitFunctions import center_h1, center_text, center_h3
from pages.aboutme import aboutme
from pages.uberdata import uberdata
from pages.accidents import accidents
import warnings
warnings.filterwarnings("ignore")

# set the title of the page
st.set_page_config(
    page_title=TAB_TITLE, 
    page_icon=FAVICON_LOGO,
    layout="wide", 
    initial_sidebar_state="collapsed",
    # set to light mode
    theme="light"
)



# Pages
# Define the pages
PAGES = [
	{"name": "About Me", "function": aboutme, "icon": "file-earmark-person"},
	{"name": "Streamlit exploration", "function": uberdata, "icon": "graph-up"},
	{"name": "How to avoid an accident", "function": accidents, "icon": "car-front"},
]

# Title
center_h1(PAGE_TITLE)

# Display option menu
selection = option_menu(
	None, 
	[page['name'] for page in PAGES], 
	icons=[page['icon'] for page in PAGES], 
	menu_icon="cast", 
	default_index=0, 
	orientation="horizontal"
)

# Get and display the selected page
selected_page = [page for page in PAGES if page['name'] == selection]
if len(selected_page) > 0 and selected_page[0]['function'] is not None:
    selected_page[0]['function']()

_ = [center_text("") for _ in range(5)]
st.markdown("""
    <div style='text-align: center; color: grey;'>
        Made with ❤️ by Paul Zamanian<br>
        © 2024 Paul Zamanian. All rights reserved.<br>
        Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

