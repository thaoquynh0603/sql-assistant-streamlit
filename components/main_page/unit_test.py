
from model.unit_test import UnitTest
import streamlit as st

def unit_test(result):
    @st.cache_resource
    def reset(result):
        if 'run_duplicate_?' in st.session_state:
            st.session_state['run_duplicate_?'] = False
        if 'run_null_?' in st.session_state:
            st.session_state['run_null_?'] = False
        if 'run_value_?' in st.session_state:
            st.session_state['run_value_?'] = False
    reset(result)

    unit_test = UnitTest(result)
    columns_list = unit_test.columns_choice
    columns = st.columns([0.25, 0.75])
    columns_choice = []
    for i in range(len(columns_list)):
        check = columns[0].checkbox(columns_list[i])
        if check:
            columns_choice.append(columns_list[i])
    if 'All' in columns_choice:
        columns_choice = columns_list[1:]

    sub_columns = columns[1].columns(3)
    if columns_choice != []:
        if 'run_duplicate_?' not in st.session_state:
            st.session_state['run_duplicate_?'] = False
        if 'run_null_?' not in st.session_state:
            st.session_state['run_null_?'] = False
        if 'run_value_?' not in st.session_state:
            st.session_state['run_value_?'] = False


        def run_duplicate_test():
            print("Duplicate test run")
            st.session_state['run_duplicate_?'] = True
            st.session_state['run_null_?'] = False
            st.session_state['run_value_?'] = False
        
        def run_null_test():
            print("Null test run")
            st.session_state['run_duplicate_?'] = False
            st.session_state['run_null_?'] = True
            st.session_state['run_value_?'] = False

        def run_value_test():
            print("Value range test run")
            st.session_state['run_duplicate_?'] = False
            st.session_state['run_null_?'] = False
            st.session_state['run_value_?'] = True


        sub_columns[0].button('Duplicate Check', on_click=run_duplicate_test)
        sub_columns[1].button('Null Value Check', on_click=run_null_test)
        sub_columns[2].button('Value Range Check', on_click=run_value_test)

        if st.session_state['run_duplicate_?']:
            print("Duplicate test run")
            @st.cache_data
            def cache_duplicate_test(columns_choice):
                unit_test.duplicate_test(columns_choice)
                return unit_test.duplicated_rows, unit_test.duplicated_info
            duplicated_rows, duplicated_info = cache_duplicate_test(columns_choice)
            if duplicated_rows.empty:
                columns[1].write("✅ No duplicated rows")
            else:
                columns[1].write(duplicated_rows)
                columns[1].write(duplicated_info)
        
            
            
        if st.session_state['run_null_?']:
            print("Null test run")
            @st.cache_data
            def cache_null_test(columns_choice):
                unit_test.null_test(columns_choice)
                return unit_test.null_rows
            null_rows = cache_null_test(columns_choice)
            if null_rows.empty:
                columns[1].write("✅ No missing values")
            else:
                columns[1].write(null_rows)
    


        if st.session_state['run_value_?']:
            @st.cache_data
            def cache_value_test(columns_choice):
                unit_test.value_test(columns_choice)
                return unit_test
                
            unit_test = cache_value_test(columns_choice)
            
            if len(unit_test.categorical_columns) == 0:
                pass
            else:
                columns[1].markdown("<b style='font-size: 18px;'>Categorical Values</b>", unsafe_allow_html=True)
                for i in unit_test.categorical_columns:
                    columns[1].write(f"{i}")
                    columns[1].write(unit_test.categorical_columns_value[i])
            
            if len(unit_test.numeric_columns) == 0:
                pass
            else:
                columns[1].markdown("<b style='font-size: 18px;'>Numerical Values</b>", unsafe_allow_html=True)
                columns[1].write(unit_test.numeric_columns_value)