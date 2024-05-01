from model.extract_data import database_client, dataset_client, schema_client
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import pandas as pd 
import re
import json
import os
from dotenv import load_dotenv
import db_dtypes
load_dotenv()

#the dictionary is regenerated if requested only
class data_dict():
    def __init__(self, project_id, dataset_id, docs=None):
        self.project_id = project_id 
        self.dataset_id = dataset_id
        self.docs = docs
        self.dataset_client = dataset_client(project_id, dataset_id)
        self.tables = self.dataset_client.get_schema()
        self.tables_dict = {}
        
        self.safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        for table_id in self.tables:
            self.tables_dict[table_id] = schema_client(project_id, dataset_id, table_id)
       
        if docs != None:
            with open(docs, 'r') as file:
                file_content = file.read()
            docs_content = re.findall(r'{%\s*docs\s*(.*?)\s*%}\s*(.*?)\s*{%\s*enddocs\s*%}', file_content, re.DOTALL)
            self.doc_dict = {field: description for field, description in docs_content}
            self.doc_keys = self.doc_dict.keys()


    def ai_gen_setup(self):
        api_key = os.environ['GOOGLE_API_KEY']
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
        
        
        self.prompt = """Write a short sentence to describe about property: {} of table {} (value example is: {}, don't include any example in the description).
                 Example: The unique identifier of the user in the system
              """
        self.generate_token = 0

    def ai_description(self, field, table, example):
        self.prompt_input = self.prompt.format(field, table, example)
        description = self.llm.invoke(self.prompt_input, safety_settings=self.safety_settings)
        self.generate_token += len(self.prompt_input) + len(description.content)
        return description

    def generate_dictionary(self):
        self.ai_gen_setup()
        data_dictionary = {
                    'table':[]
                   ,'field':[]
                   ,'type':[]
                   ,'mode':[]
                   ,'description':[]
                   ,'source':[]
                   ,'ai_log':[]
                   }
        for table in self.tables:
            example = self.tables_dict[table].query_data(f'SELECT * FROM {self.project_id}.{self.dataset_id}.{table} LIMIT 2')
            for field in self.tables_dict[table].schema_dict:
                data_dictionary['table'].append(table)
                data_dictionary['field'].append(field['name'])
                data_dictionary['type'].append(field['type'])
                data_dictionary['mode'].append(field['mode'])
                #use ai to generate prompt
                example_field = ",".join(list(map(str,list(example[field['name']]))))
                if (self.docs != None) and (field['name'].lower() in self.doc_keys):
                    data_dictionary['description'].append(self.doc_dict[field['name'].lower()])
                    data_dictionary['source'].append('docs')
                    data_dictionary['ai_log'].append(None)
                else:
                    description = self.ai_description(table, field['name'], example_field)
                    data_dictionary['description'].append(description.content)
                    data_dictionary['source'].append('ai-generated')
                    data_dictionary['ai_log'].append(description.response_metadata)
        self.data_dictionary = data_dictionary
        self.data_df = pd.DataFrame(data_dictionary)
        self.data_df.to_csv("model/data_dictionary.csv")

if __name__ == "__main__":
    with open("model/setting.json", "r") as f:
        setting = json.load(f)

    project_id = setting['project_id']
    dataset_id = 'Public_Dataset'
    dictionary = data_dict(project_id, dataset_id)
    dictionary.generate_dictionary()
    print(dictionary.data_df)
