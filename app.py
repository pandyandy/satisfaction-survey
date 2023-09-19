import streamlit as st
import base64
import os

from functions.multiple_choice import multiplechoice_q
from functions.yes_no import yes_no_q
from functions.text_input import open_q
from functions.scale import scale_q
from functions.rating import rating_q
from functions.emojis import emojis_q
#from tabs.x_likert import likert_q
#from tabs.x_ordinal_scale import ordinal_q

# from src.keboola_storage_api.connection import add_keboola_table_selection
# from src.keboola_storage_api.upload import main as upload_to_keboola

image_path = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Keboola Satisfaction Survey",
    page_icon=image_path+"/static/keboola.png",
    layout="wide"
    )

logo_image = image_path+"/static/keboola_logo.png"
logo_html = f'<div style="display: flex; justify-content: flex-end;"><img src="data:image/png;base64,{base64.b64encode(open(logo_image, "rb").read()).decode()}" style="width: 150px; margin-left: -10px;"></div>'
st.markdown(f"{logo_html}", unsafe_allow_html=True)

st.title('Satisfaction Survey')

def main():

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Emojis", "Yes/No Question", "Multiplechoice Question", "Scale 0 to 10", "Open Question", "Stars Rating"])

    with tab1:
        emojis_q()
        
    with tab2: 
        yes_no_q()

    with tab3:
        multiplechoice_q()

    with tab4:
        scale_q()

    with tab5:
        open_q()

    with tab6:
        rating_q()

    # Hide Made with streamlit from footer
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ == "__main__":
    main()