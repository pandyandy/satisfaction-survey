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
question_text = "What was the primary reason for your purchase today?"

st.markdown(f"""
<h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

button_labels_col1 = ['Quality', 'Price', 'Convenience']
button_labels_col2 = ['Brand', 'Recommendation', 'Other']

# Response
for label in button_labels_col1:
    if col1.button(label, use_container_width=True):
        get_data(label)
        st.success(f"You chose '{label}'. Thank you for your feedback!")


for label in button_labels_col2:
    if col2.button(label, use_container_width=True):
        get_data(label)
        st.success(f"You chose '{label}'. Thank you for your feedback!")

    #timestamp = int(time.time())
    #file_name = 'results'
    #client.tables.delete('out.c-data.data_upated_plan')
    #client.tables.create(name=file_name, bucket_id='out.c-data', file_path='./updated_plan.csv.gz')

# Load data into Keboola Storage
results.to_csv('./results_multiple_choice.csv.gz', index=False, compression='gzip')
client.tables.load(table_id='out.c-SatisfactionSurvey.results_multiple_choice', file_path='./results_multiple_choice.csv.gz', is_incremental=True)

# Hide made with Streamlit
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)