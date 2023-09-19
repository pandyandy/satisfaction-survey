import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time
import pytz
from streamlit_star_rating import st_star_rating
from kbcstorage.client import Client
client = Client(st.secrets.kbc_url, st.secrets.kbc_token)

data = {'id': [], 'option_1': [], 'option_2': [], 'option_3': [], 'date': [], 'time': []}
results = pd.DataFrame(data)

def createData(opt_1, opt_2, opt_3):
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
        'option_1': opt_1,
        'option_2': opt_2,
        'option_3': opt_3,
        'date': date,
        'time': time
    }
    results.loc[len(results)] = data

def rating_q():
    
    if 'option_1_value' not in st.session_state:
        st.session_state['option_1_value'] = None
    if 'option_2_value' not in st.session_state:
        st.session_state['option_2_value'] = None    
    if 'option_3_value' not in st.session_state:
        st.session_state['option_3_value'] = None 
    
    question_text = "Rank these aspects of your experience from 1 (bad) to 5 (amazing):"

    st.markdown(f"""
    <h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    message_area = st.empty()

    with col1:
        option_1 = "Ordering process"
        st.markdown(f"""
        <h3 style='text-align: right; margin-bottom: '>{option_1}</h3>
        """, unsafe_allow_html=True)
        
        option_2 = "Product quality"
        st.markdown(f"""
        <h3 style='text-align: right; margin-bottom: '>{option_2}</h3>
        """, unsafe_allow_html=True)
        
        option_3 = "Customer service"
        st.markdown(f"""
        <h3 style='text-align: right; margin-bottom: '>{option_3}</h3>
        """, unsafe_allow_html=True)
        
    with col2:
        stars1 = st_star_rating("", maxValue= 5, defaultValue=0, key="rating1", size=30)
        stars2 = st_star_rating("", maxValue= 5, defaultValue=0, key="rating2", size=30)
        stars3 = st_star_rating("", maxValue= 5, defaultValue=0, key="rating3", size=30)

        if st.button("SUBMIT", key="submit_rating"):

            st.session_state['option_1_value'] = stars1
            st.session_state['option_2_value'] = stars2
            st.session_state['option_3_value'] = stars3 

            createData(opt_1=st.session_state['option_1_value'], opt_2=st.session_state['option_2_value'], opt_3=st.session_state['option_3_value'])
            
            results.to_csv('./results_rating.csv.gz', index=False, compression='gzip')
            client.tables.load(table_id='out.c-SatisfactionSurvey.results_rating', file_path='./results_rating.csv.gz', is_incremental=True)
   
            message_area.success(f"You chose '{option_1}: {st.session_state['option_1_value']}', '{option_2}: {st.session_state['option_2_value']}', '{option_3}: {st.session_state['option_3_value']}'. Thank you for your feedback!")

    #timestamp = int(time.time())
    #file_name = 'results'
    #client.tables.delete('out.c-data.data_upated_plan')
    #client.tables.create(name=file_name, bucket_id='out.c-data', file_path='./updated_plan.csv.gz')
if __name__ == "__main__":
    rating_q()