import pandas as pd
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.width', None)  # Display full width of the console
pd.set_option('display.max_colwidth', None) # Display full contents of each column

class data_info:
    def __init__(self, tables=None, fields=None, path='model/input/data_dictionary.csv'):
        self.data_dict = pd.read_csv(path)
        if tables != None:
            self.tables = tables
            self.data_table = self.data_dict[self.data_dict['table'].isin(self.tables)]
            if fields != None:
                fields = list(fields.values())
                self.fields = [item for sublist in fields for item in sublist]
                self.data_props = self.data_table[self.data_table['field'].isin(self.fields)]
            else:
                self.data_props = self.data_table
        else:
            self.data_table = self.data_dict
            self.data_props = self.data_dict
        #self.data_table is for further process
        #self.data_props will be used in the prompt


    def get_relation(self): #self.relation_list
        relation_set = self.data_props[~self.data_props['key'].isnull()]
        relation_set['fake_key'] = relation_set[['table','property']].apply(lambda row: self.fake_key(row['table'], row['property']), axis=1)
        relation_set = relation_set[relation_set['fake_key'].duplicated(keep=False)]
        relationship = 'the "{}" table with the key "{}" has a one-to-many relationship with the "{}" table with the key "{}"'
        self.relations_list = []
        primary_table = list(relation_set[relation_set['key']=='PM']['table'])
        foreign_table = list(relation_set[relation_set['key']=='FK']['table'])
        for a in primary_table:
            pm_key = relation_set[(relation_set['key']=='PM') & (relation_set['table']==a)]['property'].iloc[0]
            for b in foreign_table:
                if a != b:
                    fk_key = relation_set[(relation_set['key']=='FK') & (relation_set['table']==b)]['property'].iloc[0]
                    self.relations_list.append(relationship.format(a,pm_key, b, fk_key))
        self.relations = '\n'.join(list(set(self.relations_list)))
    
    def drop_columns(self, columns = ['mode', 'source','ai_log']): #self.psrops_drop_columns
        self.data_props = self.data_props.drop(columns, axis=1)

    def update_table_name(self, project_id, dataset_id):
        self.data_props['table'] = self.data_props['table'].apply(lambda x: f"{project_id}.{dataset_id}.{x}")

    def retrieve_information(self, project_id, dataset_id):
        # self.get_relation() 
        #I haven't have a clear solution on the relation of Euc dataset
        self.update_table_name(project_id, dataset_id)
        self.drop_columns()

if __name__=='__main__':                 
    field = {'data_quiz': ['User_ID'], 'prod_pages': ['brand', 'anonymous_id']}
    tables = list(field.keys())   
    datainfo = data_info(tables, field)
    project_id = "query-assistant"
    dataset_id = "Public_Dataset"
    datainfo.retrieve_information(project_id, dataset_id)
    print(datainfo.data_props)