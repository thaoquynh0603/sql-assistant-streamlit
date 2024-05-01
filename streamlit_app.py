from model.extract_data import database_client
import streamlit as st
import json 
from PIL import Image
from components.sidebar.datainput import data_input
from components.sidebar.dictionary_update import dictionary_update
from components.sidebar.set_model import set_model
from components.main_page.example_input import example_input
from components.main_page.request_input import request_input, expected_field_input
from components.main_page.prompt_generation import generate_prompt
from components.main_page.sql_output import sql_output
from components.main_page.run_query import run_query
from components.main_page.unit_test import unit_test


#----SETUP------------------------------------------------------------------------------------------
im = Image.open("favicon.png")
st.set_page_config(
        page_title="Quynh's Query Assistant",
        page_icon=im,
        layout="wide",
    )

with open("model/input/setting.json", "r") as f:
    setting = json.load(f)
        
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("streamlit_style.css")

project_id = setting["project_id"]
docs = setting["docs"]
db = database_client(project_id)


#SIDEBAR---------------------------------------------------------------------------
with st.sidebar:
    #authentication
    
    #Choose dataset
    dataset_id, table_schema, table_options = data_input(db, project_id)
    #regenerate_dictionary
    # dictionary_update(project_id, dataset_id, docs)
    #set_model
    chosen_model, temperature, max_token = set_model()


#MAIN_PAGE--------------------------------------------------------------------------------

request = request_input()
example_list = example_input(request)
# expected_fields = expected_field_input()
input_prompt = generate_prompt(project_id, dataset_id, table_options, table_schema, request, expected_fields=None, example=example_list)
button_column = st.columns(2)
sql_query, pricing_details, is_sql_generated = sql_output(input_prompt, chosen_model, temperature, max_token, button_column[0])
if is_sql_generated:
    result, is_run_completed = run_query(db, sql_query, button_column[1])
    if is_run_completed:
        unit_test(result)


        
    
              
        
            