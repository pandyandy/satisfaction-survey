import streamlit as st
import pandas as pd
import random
import os
import pytz
import base64

from datetime import datetime
from st_clickable_images import clickable_images 
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

# Load data into Keboola Storage
def load_data():
    results.to_csv('./results_likert.csv.gz', index=False, compression='gzip')
    client.tables.load(table_id='out.c-SatisfactionSurvey.results_likert', file_path='./results_likert.csv.gz', is_incremental=True)

# Create Q&A
question_text = "How likely are you to use our service again?"

st.markdown(f"""
<h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
""", unsafe_allow_html=True)

# Likert scale labels
LIKERT = {0: "not likely", 1: "unlikely", 2: "neutral", 3: "likely", 4: "very likely"}
LIKERT_TITLES = ["not likely", "unlikely", "neutral", "likely", "very likely"]


image_files = [static_directory+"/not_likely.png", static_directory+"/unlikely.png", static_directory+"/neutral.png", static_directory+"/likely.png", static_directory+"/very_likely.png"]
images = []

for file in image_files:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        images.append(f"data:image/png;base64,{encoded}")
        
clicked = clickable_images(
images,
div_style={"display": "flex", "justify-content": "center"},
img_style={"margin": "7%", "height": "30px"},
)

# Response
if clicked in LIKERT:
    get_data(LIKERT[clicked])
    st.success(f"You chose '{LIKERT[clicked]}'. Thank you for your feedback!") 
    load_data()

# Hide made with Streamlit
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)