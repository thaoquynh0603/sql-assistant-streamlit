import streamlit as st

def request_input():
    request = st.text_area("Enter the request","", height=20) 
    return request

def expected_field_input():
    output_columns = st.text_input('What columns to include in the output?', '')
    if output_columns == '':
        output_columns = None
    else:
        output_columns = output_columns.split(',')
    return output_columns