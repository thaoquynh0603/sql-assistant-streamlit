from model.extract_data import dataset_client, schema_client
import streamlit as st

def data_input(db, project_id):
    st.header("Data Input")
    @st.cache_resource
    def collect_data_input():
        print('run1')
        datasets = db.get_dataset()
        return datasets
    datasets = collect_data_input()
    dataset_id = st.selectbox('Choose the dataset:', datasets)

    print(project_id, dataset_id)
    #Choose Table

    choose_table = st.toggle('Choose Tables?')
    if choose_table:
        @st.cache_resource
        def collect_table_input(project_id, dataset_id):
            print('run2')
            table = dataset_client(project_id, dataset_id)
            table_list = table.get_schema()
            return table_list
        table_list = collect_table_input(project_id, dataset_id)
        table_options = st.multiselect('What tables?', table_list)
        print("Table option is:", table_options)
        if table_options == []: 
            table_options = None
    else:
        table_options = None

    #Choose field
    option = []
    if table_options != None:
        for table in table_options:
            choose_table = st.toggle(f'Choose Fields for {table}?')
            option.append(choose_table)
        
        table_schema = {}
        for i in range(len(table_options)):
            table_id = table_options[i]
            @st.cache_resource
            def collect_schema_input(project_id, dataset_id, table_id):
                print('run3')
                props = schema_client(project_id, dataset_id, table_id) #Use schema_client
                table_list = props.columns
                return table_list
            table_list = collect_schema_input(project_id, dataset_id, table_id)
            table_schema[table_id] = table_list
            if option[i]:
                label = f'Choose Inputs for table {table_options[i]}'
                options = st.multiselect(label, table_list)
                if options == []:
                    options = table_list
                table_schema[table_id] = options
                print(table_schema)
    else:
        table_schema = None

    return dataset_id, table_schema, table_options

    