from model.generate_dictionary import data_dict
import streamlit as st

def dictionary_update(project_id, dataset_id, docs):
    dict_update_check = False
    @st.cache_resource
    def dictionary_update():
        try:
            dictionary = data_dict(project_id, dataset_id, docs=docs)
            dictionary.generate_dictionary()
            dict_update_check = True
        except:
            print("Cannot update Dictionary")

    if st.button('Check availability'):
        dictionary_update()

    if dict_update_check:
        st.text("The dictionary is successfully update!")

    