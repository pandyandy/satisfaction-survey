import streamlit as st
import pandas as pd
import random
import os
import pytz
import base64

from datetime import datetime
from functions.change_colour import ChangeButtonColour
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
question_text = "How likely are you to recommend us to a friend or colleague?"

st.markdown(f"""
<h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
""", unsafe_allow_html=True)

colours=['#d44948', '#dc6545', '#e17642', '#efa73e', '#f3b83c', '#fbd538', '#d8ce43', '#c0ca4b', '#87c15b', '#6fbc62', '#4cb76d'] # Button colours

columns = st.columns(11) # Create 11 columns for each button
placeholder = st.empty()

for idx, value in enumerate(range(11)): # Loop from 0 to 10
    if columns[idx].button(str(value), use_container_width=True):
        get_data(value)
        placeholder.success(f"You chose '{value}'. Thank you for your feedback!")
    ChangeButtonColour(str(value), '#ffffff', background_color=colours[idx])
         
    #timestamp = int(time.time())
    #file_name = 'results'
    #client.tables.delete('out.c-data.data_upated_plan')
    #client.tables.create(name=file_name, bucket_id='out.c-data', file_path='./updated_plan.csv.gz')

# Load data into Keboola Storage
results.to_csv('./results_scale.csv.gz', index=False, compression='gzip')
client.tables.load(table_id='out.c-SatisfactionSurvey.results_scale', file_path='./results_scale.csv.gz', is_incremental=True)

# Hide made with Streamlit
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)