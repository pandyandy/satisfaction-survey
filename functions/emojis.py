import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime
import time
import base64
import pytz
from st_clickable_images import clickable_images 
from kbcstorage.client import Client
client = Client(st.secrets.kbc_url, st.secrets.kbc_token)

data = {'id': [], 'answer': [], 'date': [], 'time': []}
results = pd.DataFrame(data)

def createData(answer):
    current_datetime = datetime.now()
    random_number = random.randint(1000, 9999)
    # PRAGUE TIMEZONE
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

def emojis_q():
    if 'chosen_image' not in st.session_state:
        st.session_state['chosen_image'] = None

    question_text = "How satisfied were you with your purchase experience today?"

    st.markdown(f"""
    <h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
    """, unsafe_allow_html=True)

    EXPERIENCES = {0:"unhappy", 1: "neutral", 2: "happy"}

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    image_folder = os.path.join(repo_dir, "static")
    image_files = ["angry.png", "neutral.png", "happy.png"]

    images = []

    for file in image_files:
        image_path = os.path.join(image_folder, file)
        with open(image_path, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/png;base64,{encoded}")
    
    notes = ["happy","neutral","unhappy"]            
    
    clicked = clickable_images(
    images,
    titles=[f"{str(note)}" for note in notes],
    div_style={"display": "flex", "justify-content": "center"},
    img_style={"margin": "5%", "height": "200px"},
)
    if clicked in EXPERIENCES:
        createData(EXPERIENCES[clicked])
        st.session_state['chosen_image'] = EXPERIENCES[clicked]

    if st.session_state['chosen_image']:
        results.to_csv('./results_emojis.csv.gz', index=False, compression='gzip')
        client.tables.load(table_id='out.c-SatisfactionSurvey.results_emojis', file_path='./results_emojis.csv.gz', is_incremental=True)
        st.success(f"You chose '{st.session_state['chosen_image']}'. Thank you for your feedback!")
       

    #timestamp = int(time.time())
    #file_name = 'results'
    #client.tables.delete('out.c-data.data_upated_plan')
    #client.tables.create(name=file_name, bucket_id='out.c-data', file_path='./updated_plan.csv.gz')

if __name__ == "__main__":
    emojis_q()