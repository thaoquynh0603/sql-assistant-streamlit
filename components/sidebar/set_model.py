import streamlit as st


def  set_model():
    available_models = ['Gemini-Pro', 'GCP Codey', 'ChatGPT3-Turbo','ChatGPT4']
    # available_caption = ["Well, it's free :)))", 'Designed for Code Generation']
    st.header("Model Setting")
    chosen_model = st.radio('Choose the model:', available_models, label_visibility='collapsed')
    print("chosen model is ", chosen_model)
    with st.expander("Advanced Setting"):
        temperature = st.slider('Temperature', 0.0, 1.0, value=0.5, step=0.1)
        max_token = st.slider('Max-Token', 100, 2000, value=1000, step=100)
    return chosen_model, temperature, max_token
    