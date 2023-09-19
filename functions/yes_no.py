import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time
import pytz
from functions.change_colour import ChangeButtonColour
from kbcstorage.client import Client

if 'feedback_given' not in st.session_state:
    st.session_state['feedback_given'] = False
if 'waiting_for_feedback' not in st.session_state:
    st.session_state['waiting_for_feedback'] = False

data = {'id': [], 'answer': [], 'feedback': [], 'date': [], 'time': []}
results = pd.DataFrame(data)

client = Client(st.secrets.kbc_url, st.secrets.kbc_token)

def createData(answer, text):
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
        'feedback': text,
        'date': date,
        'time': time
    }
    results.loc[len(results)] = data

def save_results_to_csv(results):
    try:
        results.to_csv('./results_yes_no.csv.gz', index=False, compression='gzip')
        client.tables.load(table_id='out.c-SatisfactionSurvey.results_yes_no', file_path='./results_yes_no.csv.gz', is_incremental=True)
        st.session_state['feedback_given'] = False
        st.session_state['waiting_for_feedback'] = False
    except Exception as e:
        print(f"An error occurred while saving the results: {e}")

def yes_no_q():
    
    question_text = "Were you satisfied with your purchase today?"

    st.markdown(f"""
    <h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
    """, unsafe_allow_html=True)

    col1, yes_col, col3, no_col, col5 = st.columns(5)
    with col1:
        pass
    with yes_col:
        yes = st.button("YES", use_container_width=True)
    with col3:
        pass    
    with no_col:
        no = st.button("NO", use_container_width=True)
    with col5:
        pass

    if yes: 
        st.session_state['feedback_given'] = True
        createData(answer="Yes", text=None)
        st.success("Thank you for your feedback!")
        save_results_to_csv(results)        
    ChangeButtonColour('YES', '#ffffff', '#4fbb6e')
    
    if no:    
        st.session_state.waiting_for_feedback = True
        st.session_state.feedback_given = False
    ChangeButtonColour('NO', '#ffffff', '#e24b4b') 

    if st.session_state.get('waiting_for_feedback', False):
        feedback = st.text_area("Please tell us why:", key="text_yn")
        
        if st.button("SUBMIT", key="submit_yn") and not st.session_state['feedback_given']:
            st.session_state['feedback_given'] = True
            st.session_state['waiting_for_feedback'] = False
            createData(answer="No", text=feedback)
            save_results_to_csv(results) 
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please provide your feedback before submitting.")

    #timestamp = int(time.time())
    #file_name = 'results'
    #client.tables.delete('out.c-data.data_upated_plan')
    #client.tables.create(name=file_name, bucket_id='out.c-data', file_path='./updated_plan.csv.gz')
if __name__ == "__main__":
    yes_no_q()