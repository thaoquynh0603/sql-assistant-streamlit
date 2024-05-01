import streamlit as st

def run_query(db, sql_query, button_field):
    @st.cache_data
    def reset(sql_query):
        if 'run_query' in st.session_state:
            st.session_state['run_query'] = False
    reset(sql_query)

    is_run_completed = False
    result = None

    if 'run_query' not in st.session_state:
        st.session_state['run_query'] = False

    def run_query():
        if 'generate_query' not in st.session_state:
            st.session_state['generate_query'] = True
        st.session_state['run_query'] = True

    button_field.button('EXECUTE', on_click=run_query)
    if st.session_state['run_query']:
        print("Run query")
        print(sql_query)
        @st.cache_resource
        def execute_query(sql_query):
            result = db.query_data(sql_query, folder="output", csv_export=True)
            is_run_completed = True
            return result, is_run_completed
        result, is_run_completed = execute_query(sql_query)
        st.write(result.head(10))
        with open('query_result.csv', 'rb') as data_file:
            btn = st.download_button(
                    label='Download this data',
                    data=data_file,
                    file_name="data.csv"
                    )
    return result, is_run_completed

            