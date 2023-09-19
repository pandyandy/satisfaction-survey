import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time
import pytz
from functions.change_colour import ChangeButtonColour
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

def scale_q():
    if 'chosen_value' not in st.session_state:
        st.session_state['chosen_value'] = None

    question_text = "How likely are you to recommend us to a friend or colleague?"

    st.markdown(f"""
    <h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
    """, unsafe_allow_html=True)

    colours=['#d44948', '#dc6545', '#e17642', '#efa73e', '#f3b83c', '#fbd538', '#d8ce43', '#c0ca4b', '#87c15b', '#6fbc62', '#4cb76d']

    columns = st.columns(11) # Create 11 columns for each button
    message_area = st.empty()


    for idx, value in enumerate(range(11)): # Loop from 0 to 10
        with columns[idx]:
            if st.button(str(value), use_container_width=True):
                st.session_state['chosen_value'] = str(value)
                createData(value)
            ChangeButtonColour(str(value), '#ffffff', background_color=colours[idx])
            
    if st.session_state['chosen_value']:
        results.to_csv('./results_scale.csv.gz', index=False, compression='gzip')
        client.tables.load(table_id='out.c-SatisfactionSurvey.results_scale', file_path='./results_scale.csv.gz', is_incremental=True)

        message_area.success(f"You chose '{st.session_state['chosen_value']}'. Thank you for your feedback!")
             
    #timestamp = int(time.time())
    #file_name = 'results'
    #client.tables.delete('out.c-data.data_upated_plan')
    #client.tables.create(name=file_name, bucket_id='out.c-data', file_path='./updated_plan.csv.gz')
if __name__ == "__main__":
    scale_q()