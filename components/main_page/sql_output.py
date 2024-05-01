from model.generate_query import model
from vertexai.generative_models import GenerativeModel
import vertexai
import streamlit as st


def sql_output(input_prompt, chosen_model, temperature, max_token, button_field):
    @st.cache_resource
    def reset_the_prompt(input_prompt, chosen_model, temperature, max_token):
        if 'generate_query' in st.session_state:
            st.session_state['generate_query'] = False
    reset_the_prompt(input_prompt.prompt, chosen_model, temperature, max_token)

    if 'generate_query' not in st.session_state:
        st.session_state['generate_query'] = False
    def review_button():
        st.session_state['generate_query'] = True
    button_field.button('REVIEW', on_click=review_button)
    
    vertexai.init(project="query-assistant", location="us-central1")

    @st.cache_resource
    def predict_token(text_prompt):
        model = GenerativeModel("gemini-1.0-pro-002")
        result = model.count_tokens(text_prompt)
        return result.total_tokens
    predicted_token = predict_token(input_prompt.prompt)
    print(predict_token)
    st.markdown(
    f"<span style='font-size: smaller; opacity: 0.7;'>_The predicted number of tokens is: {predicted_token}_</span>",
    unsafe_allow_html=True  
    )

    is_sql_generated = False
    sql_query = ''
    token_details = 0
    if st.session_state['generate_query']:
        print("the session state runnings")
        @st.cache_resource
        def generate_query(text_prompt, chosen_model, temperature, max_token):
            llm = model(temperature, max_token)
            llm.run(chosen_model, text_prompt)
            sql_query = llm.output
            token_details = llm.token_details
        
            return sql_query, token_details
        print(input_prompt.prompt)
        sql_query, token_details = generate_query(input_prompt.prompt, chosen_model, temperature, max_token)
        is_sql_generated = True
        st.write(sql_query)
        st.markdown(
        "<span style='font-size: smaller; opacity: 0.7;'>_This request takes {} tokens for the prompt and {} tokens for the response._</span>"\
            .format(token_details["input"],token_details["output"]),
            unsafe_allow_html=True  
        )
        return sql_query, token_details, is_sql_generated
    return sql_query, token_details, is_sql_generated