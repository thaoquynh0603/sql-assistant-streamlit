from model.retrieve_datainfo import data_info
import re

class prompt:
    def __init__(self, project_id, dataset_id, sql_system):
        self.project_id = project_id
        self.sql_system = sql_system
        self.dataset_id = dataset_id

    def get_data_info(self, tables, field):
        data = data_info(tables, field)
        #note retrieve_information get information from data_dictionary.csv
        data.retrieve_information(self.project_id, self.dataset_id) 
        self.data_props = data.data_props
        # self.relations = data.relations    
    
    def get_request(self, request):
        self.request = request

    def get_desire(self, output_columns=None):
        self.desire = output_columns

    def get_example(self, example=None):
        self.example = example

    def schema_info_prompt(self):
        self.prompt += f"""
        The dataset has field in tables as follows:
                {self.data_props}
        Avoid performing FULL JOIN and INNER JOIN
        """
         # The relations in tables that you should consider to do LEFT JOIN:
        #         {self.relations}

    def example_prompt(self):
        if self.example is None or self.example == "":
            pass
        else:
            self.prompt += f"""You should generated query that is similar to Reference Query:
                Request: {self.example['request']}
                Correct query: {self.example['response']}
            """

    def output_desire_prompt(self):
        if self.desire is None:
            pass
        else:
            self.prompt += f"""The expected output will contain {self.desire}
            """

    def base_prompt(self):
        self.prompt += f"""
            Given the data information above, generate a SQL query in {self.sql_system} only that: 
            {self.request}
        """

    def final_prompt(self):
        self.prompt = ""
        self.schema_info_prompt()
        self.output_desire_prompt()
        self.example_prompt()
        self.base_prompt()
        self.token = len(re.findall(r'\w+', self.prompt))

    def create_prompt(self, tables, fields, request, output_columns=None, example=None):
        self.get_data_info(tables, fields)
        self.get_request(request)
        self.get_desire(output_columns)
        self.get_example(example)
        self.final_prompt()
        print("The prompt has been generated!")

    def add_prompt(self, add_prompt):
        self.prompt += f"""
            {add_prompt}
        """

if __name__ == "__main__":
    project_id = 'skillful-cosine-417004'
    dataset_id = 'qn_dataset'
    sql_system = 'Google Big Query'
    p = prompt(project_id, dataset_id, sql_system)
    field = {'data_quiz': ['User_ID'], 'prod_pages': ['brand', 'anonymous_id']}
    tables = list(field.keys())   
    request = 'Select the first name of users and the user id of events'
    output_columns=None
    example=None
    p.create_prompt(tables, field, request)
    print(p.prompt)
    print(p.token)
