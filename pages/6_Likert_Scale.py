import streamlit as st
import pandas as pd
import random
import os
import pytz
import base64

from datetime import datetime
from kbcstorage.client import Client

# Set page layout
st.set_page_config(layout="wide")

static_directory = os.path.join(os.path.dirname(__file__), "..", "static")
logo_image = os.path.join(static_directory, "keboola_logo.png")
logo_html = f'<div style="display: flex; justify-content: flex-end;"><img src="data:image/png;base64,{base64.b64encode(open(logo_image, "rb").read()).decode()}" style="width: 150px; margin-left: -10px;"></div>'

st.markdown(f"{logo_html}", unsafe_allow_html=True)
st.markdown(" ")

# Use client secrets
client = Client(st.secrets.kbc_url, st.secrets.kbc_token)

# Get data
data = {'id': [], 'answer': [], 'date': [], 'time': []}
results = pd.DataFrame(data)

def get_data(answer):    
    random_number = random.randint(1000, 9999)
    # Prague Timezone
    current_datetime_utc = datetime.utcnow()
    prague_timezone = pytz.timezone('Europe/Prague')
    current_datetime_prague = current_datetime_utc.astimezone(prague_timezone)
    
    formatted_datetime = current_datetime_prague.strftime("%Y-%m-%d %H:%M:%S")
    date, time = formatted_datetime.split(' ')
    data = {
        'id': f"{current_datetime_prague}_{random_number}",
        'answer': answer,
        'date': date,
        'time': time
    }
    results.loc[len(results)] = data

# Create Q&A
question_text = "How likely are you to use our service again?"

st.markdown(f"""
<h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
""", unsafe_allow_html=True)

# Dot colours 
colors = ['#d44948', '#efa73e', '#fbd538', '#c0ca4b', '#4cb76d'] 

# Likert scale labels
LIKERT = {0: "Not Likely", 1: "Unlikely", 2: "Neutral", 3: "Likely", 4: "Very Likely"}

# Define the CSS styles for the circle
circle_css = """
<style>
.circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin: 0 50px;  /* Adjust the margin for spacing */
  cursor: pointer;
  transition: background-color 0.3s ease;
}
</style>
"""

# Display the CSS styles
st.markdown(circle_css, unsafe_allow_html=True)

# Create a container with 5 columns
col1, col2, col3, col4, col5 = st.columns(5)

# Create clickable circles (dots) in each column with different colors
clicked = (
col1.markdown(f'<div class="circle" style="background-color:{colors[0]};"></div>', unsafe_allow_html=True),
col2.markdown(f'<div class="circle" style="background-color:{colors[1]};"></div>', unsafe_allow_html=True),
col3.markdown(f'<div class="circle" style="background-color:{colors[2]};"></div>', unsafe_allow_html=True),
col4.markdown(f'<div class="circle" style="background-color:{colors[3]};"></div>', unsafe_allow_html=True),
col5.markdown(f'<div class="circle" style="background-color:{colors[4]};"></div>', unsafe_allow_html=True)
)

if clicked in LIKERT:
    get_data(LIKERT[clicked])
    st.success(f"You chose '{LIKERT[clicked]}'. Thank you for your feedback!") 
    