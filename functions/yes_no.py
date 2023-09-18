import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time
import pytz
from functions.change_colour import ChangeButtonColour
data = {'id': [], 'answer': [], 'feedback': [], 'date': [], 'time': []}
results = pd.DataFrame(data)

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

def yes_no_q(client):

    if 'feedback_given' not in st.session_state:
        st.session_state.feedback_given = False
    if 'waiting_for_feedback' not in st.session_state:
        st.session_state.waiting_for_feedback = False

    question_text = "Were you satisfied with your purchase today?"

    st.markdown(f"""
    <h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
    """, unsafe_allow_html=True)

    col1, yes_col, col3, no_col, col5 = st.columns(5)
    with col1:
        pass
    if yes_col.button("YES", use_container_width=True):
        # Save response
        createData(answer="Yes", text=None)
        st.session_state.feedback_given = True
        st.success("Thank you for your feedback!")
    ChangeButtonColour('YES', '#ffffff', '#4fbb6e')
    with col3:
        pass
    if no_col.button("NO", use_container_width=True):
        st.session_state.waiting_for_feedback = True
        st.session_state.feedback_given = False
    ChangeButtonColour('NO', '#ffffff', '#e24b4b') 
    with col5:
        pass
    if st.session_state.get('waiting_for_feedback', False):
        feedback = st.text_area("Please tell us why:")

        if st.button("SUBMIT", key="submit_yn") and not st.session_state.feedback_given:
            createData(answer="No", text=feedback)
            st.session_state.feedback_given = True
            st.session_state.waiting_for_feedback = False
            st.success("Thank you for your feedback!")
            
    results.to_csv('./results_yes_no.csv.gz', index=False, compression='gzip')
    client.tables.load(table_id='out.c-SatisfactionSurvey.results_yes_no', file_path='./results_yes_no.csv.gz', is_incremental=True)

    
    #timestamp = int(time.time())
    #file_name = 'results'
    #client.tables.delete('out.c-data.data_upated_plan')
    #client.tables.create(name=file_name, bucket_id='out.c-data', file_path='./updated_plan.csv.gz')
if __name__ == "__main__":
    yes_no_q()