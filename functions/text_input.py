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

def open_q(client):

    if 'feedback' not in st.session_state:
        st.session_state['feedback'] = None

    question_text = "Was there anything about this checkout process we could improve?"

    st.markdown(f"""
    <h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
    """, unsafe_allow_html=True)

    feedback = st.text_area("Your answer:")

    if st.button("SUBMIT", key="submit_text"):
        if feedback:
            st.session_state['feedback'] = feedback
            createData(feedback)
            st.success("Thank you for your feedback!")
        
        if st.session_state['feedback']:
            st.success(f"Thank you for your feedback!")
        else:
            st.warning("Please provide your feedback before submitting.")

    results.to_csv('./results_text_input.csv.gz', index=False, compression='gzip')
    client.tables.load(table_id='out.c-SatisfactionSurvey.results_text_input', file_path='./results_text_input.csv.gz', is_incremental=True)
    #timestamp = int(time.time())
    #file_name = 'results'
    #client.tables.delete('out.c-data.data_upated_plan')
    #client.tables.create(name=file_name, bucket_id='out.c-data', file_path='./updated_plan.csv.gz')

if __name__ == "__main__":
    open_q()