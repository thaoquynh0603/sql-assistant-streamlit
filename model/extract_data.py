from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd 
import json
import db_dtypes

class database_client:
    def __init__(self, project_id):
        #getting the credential from the setting.json file
        with open("model/input/setting.json", "r") as f:
            setting = json.load(f)
        credential_path = setting["gcp_service_account_path"]
        credentials = service_account.Credentials.from_service_account_file(credential_path)
        #setting the project id from input
        self.project_id = project_id
        self.client = bigquery.Client(credentials= credentials, project=project_id)
        datasets = self.client.list_datasets()
        print("Successfully get client with project_id", datasets)
        result = []
        for i in datasets:
            result.append(i.dataset_id)
        self.dataset_list = result

    def get_dataset(self):
        return self.dataset_list

    def query_data(self, query, folder="output", csv_export=False):
        query = query.replace("sql\n","").replace("```","")
        result = self.client.query(query).to_dataframe()
        if csv_export:
            result.to_csv(f"{folder}/query_result.csv", index=False)
            print("Data exported to csv")
        return result

class dataset_client(database_client):
    def __init__(self, project_id, dataset_id):
        super().__init__(project_id)
        self.dataset_id = dataset_id
        self.dataset_id = dataset_id
        dataset_ref = self.client.dataset(dataset_id)
        dataset = self.client.get_dataset(dataset_ref)
        print(dataset)
        table = self.client.list_tables(dataset)
        table = list(table)
        result = []
        for i in table:
            result.append(i.table_id)
        self.schema_list = result
        print("Get dataset client with dataset_id", self.schema_list)
    
    def get_schema(self):
        return self.schema_list
    
class schema_client(dataset_client):
    def __init__(self, project_id, dataset_id, table_id):
        super().__init__(project_id, dataset_id)
        self.table_id = table_id
        table_id = f"{self.project_id}.{self.dataset_id}.{table_id}"
        table = self.client.get_table(table_id)
        rows = table.num_rows 
        description = table.description
        schema_info = table.schema
        result_dict = []
        columns_list = [i.name for i in schema_info]
        for i in schema_info:
            info = {
                "name": i.name,
                "type": i.field_type,
                "mode": i.mode,
                "description": i.description
            }
            result_dict.append(info)
        self.num_rows = rows
        self.schema = schema_info
        self.schema_dict = result_dict
        self.columns = columns_list
        self.description = description


if __name__ == "__main__":
    db = schema_client("query-assistant", "Public_Dataset", "users")
    print(db.columns)
    query = "SELECT * FROM `query-assistant.Euc.data_quiz` LIMIT 10"
    print(db.query_data(query, folder="data"))