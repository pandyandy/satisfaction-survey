import streamlit as st
import pandas as pd
import random
import os 
import pytz
import base64

from datetime import datetime
from streamlit_star_rating import st_star_rating
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
data = {'id': [], 'option_1': [], 'option_2': [], 'option_3': [], 'date': [], 'time': []}
results = pd.DataFrame(data)

def get_data(opt_1, opt_2, opt_3):
    random_number = random.randint(1000, 9999)
    # Prague Timezone
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

# Create Q&A
question_text = "Rank these aspects of your experience from 1 (bad) to 5 (amazing):"

st.markdown(f"""
<h2 style='text-align: center; margin-bottom: 4%'>{question_text}</h2>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
placeholder = st.empty()
option_1 = "Ordering process"
col1.markdown(f"""
<h3 style='text-align: right; margin-bottom: '>{option_1}</h3>
""", unsafe_allow_html=True)

option_2 = "Product quality"
col1.markdown(f"""
<h3 style='text-align: right; margin-bottom: '>{option_2}</h3>
""", unsafe_allow_html=True)

option_3 = "Customer service"
col1.markdown(f"""
<h3 style='text-align: right; margin-bottom: '>{option_3}</h3>
""", unsafe_allow_html=True)
        
with col2:
    stars_1 = st_star_rating("", maxValue= 5, defaultValue=0, key="rating1", size=30)
    stars_2 = st_star_rating("", maxValue= 5, defaultValue=0, key="rating2", size=30)
    stars_3 = st_star_rating("", maxValue= 5, defaultValue=0, key="rating3", size=30)

# Response
    if st.button("SUBMIT", key="submit_rating"):
        get_data(opt_1=stars_1, opt_2=stars_2, opt_3=stars_3)
        placeholder.success(f"You chose '{option_1}: {stars_1}', '{option_2}: {stars_2}', '{option_3}: {stars_3}'. Thank you for your feedback!")
            
#timestamp = int(time.time())
#file_name = 'results'
#client.tables.delete('out.c-data.data_upated_plan')
#client.tables.create(name=file_name, bucket_id='out.c-data', file_path='./updated_plan.csv.gz')

# Load data into Keboola Storage
results.to_csv('./results_rating.csv.gz', index=False, compression='gzip')
client.tables.load(table_id='out.c-SatisfactionSurvey.results_rating', file_path='./results_rating.csv.gz', is_incremental=True)

# Hide made with Streamlit
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)