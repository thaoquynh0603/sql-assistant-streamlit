from model.generate_prompt import prompt
import streamlit as st
 
def generate_prompt(project_id, dataset_id, table_options, table_schema, request, expected_fields=None, example=None):
    project_id = project_id
    dataset_id = dataset_id
    sql_system = 'Google Big Query'
    @st.cache_data
    def generate_prompt(project_id, dataset_id, table_options, table_schema, request, output_columns=None, example=None):
        #any change in the prompt and model will rerun these two
        if 'generate_query' in st.session_state:
            del st.session_state['generate_query']
        if 'run_query' in st.session_state:
            del st.session_state['run_query']
        if 'run_duplicate_?' in st.session_state:
            del st.session_state['run_duplicate_?'] 
        if 'run_null_?' in st.session_state:
            del st.session_state['run_null_?']
        if 'run_value_?' in st.session_state:
            del st.session_state['run_value_?']
        input_prompt = prompt(project_id, dataset_id, sql_system)
        input_prompt.create_prompt(table_options, table_schema, request, example=example) #example and desired output
        with open('output/prompt.txt', 'w') as f:
            f.write(input_prompt.prompt)
        return input_prompt
    input_prompt = generate_prompt(project_id, dataset_id, table_options, table_schema, request, expected_fields, example)
    return input_prompt