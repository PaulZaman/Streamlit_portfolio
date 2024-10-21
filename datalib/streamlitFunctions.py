#datalib/streamlitFunctions.py

import streamlit as st

def center_text(text):
    st.markdown(f'<p style="text-align:center;">{text}</p>', unsafe_allow_html=True)

def center_h1(text):
	escaped_text = text.replace("<", "&lt;").replace(">", "&gt;")
	st.markdown(f'<h1 style="text-align:center;">{escaped_text}</h1>', unsafe_allow_html=True)

def center_h2(text):
	st.markdown(f'<h2 style="text-align:center;">{text}</h2>', unsafe_allow_html=True)
      
def center_h3(text):
    st.markdown(f'<h3 style="text-align:center;">{text}</h3>', unsafe_allow_html=True)

# Function to display a clickable logo
def display_logo(image_path: str, link_url: str, width: int = 50, height: int = 50, align: str = 'left', margin_top: int = 0):
    """
    Displays a clickable logo in a Streamlit app with alignment and margin options.

    :param image_path: Path to the local image file.
    :param link_url: URL to link to when the logo is clicked.
    :param width: Width of the displayed logo in pixels.
    :param height: Height of the displayed logo in pixels.
    :param align: Alignment of the logo ('left', 'right', or 'center').
    :param margin_top: Top margin of the logo in pixels.
    """
    align_styles = {
        'left': 'text-align: left;',
        'right': 'text-align: right;',
        'center': 'text-align: center;'
    }
    
    align_style = align_styles.get(align, 'text-align: left;')  # Default to left alignment

    st.markdown(f"""
        <div style="{align_style} margin-top: {margin_top}px;">
            <a href="{link_url}" target="_blank">
                <img src="{image_path}" alt="Logo" style="width:{width}px; height:{height}px;"/>
            </a>
        </div>
    """, unsafe_allow_html=True)