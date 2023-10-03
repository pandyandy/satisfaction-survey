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
image_path = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Keboola Satisfaction Survey",
    page_icon=image_path+"/static/keboola.png",
    layout="wide"
    )

logo_image = image_path+"/static/keboola_logo.png"
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
    results.to_csv('./results_emojis.csv.gz', index=False, compression='gzip')
    client.tables.load(table_id='out.c-SatisfactionSurvey.results_emojis', file_path='./results_emojis.csv.gz', is_incremental=True)

# Create Q&A
question_text = "How satisfied were you with your purchase experience today?"

st.markdown(f"""
<h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
""", unsafe_allow_html=True)

EXPERIENCES = {0:"unhappy", 1: "neutral", 2: "happy"}

image_files = [image_path+"/static/angry.png", image_path+"/static/neutral.png", image_path+"/static/happy.png"]
images = []

for file in image_files:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        images.append(f"data:image/png;base64,{encoded}")
        
clicked = clickable_images(
images,
div_style={"display": "flex", "justify-content": "center"},
img_style={"margin": "5%", "height": "200px"},
)

# Response
if clicked in EXPERIENCES:
    get_data(EXPERIENCES[clicked])
    st.success(f"You chose '{EXPERIENCES[clicked]}'. Thank you for your feedback!") 
    load_data()

#timestamp = int(time.time())
#file_name = 'results'
#client.tables.delete('out.c-data.data_upated_plan')
#client.tables.create(name=file_name, bucket_id='out.c-data', file_path='./updated_plan.csv.gz')

# Hide made with Streamlit
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)