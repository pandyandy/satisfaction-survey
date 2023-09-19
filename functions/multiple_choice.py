import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time
import pytz

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

def multiplechoice_q(client):

    if 'chosen_label' not in st.session_state:
        st.session_state['chosen_label'] = None

    question_text = "What was the primary reason for your purchase today?"

    st.markdown(f"""
    <h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    button_labels_1 = ['Quality', 'Price', 'Convenience']
    button_labels_2 = ['Brand', 'Recommendation', 'Other']

    with col1: 
        for label in button_labels_1:
            if st.button(label, use_container_width=True):
                st.session_state['chosen_label'] = label
                createData(label)

    with col2:
        for label in button_labels_2:
            if st.button(label, use_container_width=True):
                st.session_state['chosen_label'] = label
                createData(label)
                
    if st.session_state['chosen_label']:
        results.to_csv('./results_multiple_choice.csv.gz', index=False, compression='gzip')
        client.tables.load(table_id='out.c-SatisfactionSurvey.results_multiple_choice', file_path='./results_multiple_choice.csv.gz', is_incremental=True)

        st.success(f"Thank you for your feedback!")


    #timestamp = int(time.time())
    #file_name = 'results'
    #client.tables.delete('out.c-data.data_upated_plan')
    #client.tables.create(name=file_name, bucket_id='out.c-data', file_path='./updated_plan.csv.gz')
if __name__ == "__main__":
    multiplechoice_q()