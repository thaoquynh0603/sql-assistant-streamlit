import pandas as pd 

class UnitTest:
    def __init__(self, df):
        for col in df.columns:
            if 'id' in col:
                df[col] = df[col].astype(str)
        self.df = df
        self.columns_choice = ['All']
        self.columns_choice.extend(list(self.df.columns))
    
    def duplicate_test(self, choice_input):
        self.duplicated_rows = self.df[self.df.duplicated(subset=choice_input)].sort_values(by=choice_input)
        self.duplicated_info = self.df.groupby(choice_input).size().reset_index(name='count').sort_values(by='count', ascending=False)
        
    def null_test(self, choice_input):
        self.null_rows = self.df[self.df[choice_input].isnull().any(axis=1)]
   

    def value_test(self, choice_input):
        #categorical value
        df_temp = self.df[choice_input]
        self.categorical_columns = df_temp.select_dtypes(include=['object']).columns
        self.categorical_columns = [col for col in self.categorical_columns if 'id' not in col]
        self.categorical_columns_value = {}
        if len(self.categorical_columns) > 0:
            for column in self.categorical_columns:
                self.categorical_columns_value[column] = pd.DataFrame(df_temp[column].value_counts()).transpose()
        
        #numeric value
        self.numeric_columns = df_temp.select_dtypes(include=['float64', 'int64']).columns
        if len(self.numeric_columns) > 0:
            self.numeric_columns_value = df_temp[self.numeric_columns].describe()

if __name__=='__main__':
    df = pd.read_csv('/workspaces/query-assistant/prototype/output/distribution_centers.csv')
    unit_test = UnitTest(df)
    print(unit_test.columns_choice)
    choice_input = ['id', 'name', 'longitude']
    unit_test.duplicate_test(choice_input)
    unit_test.null_test(choice_input)
    unit_test.value_test(choice_input)
    print(unit_test.duplicated_rows)
    print(unit_test.duplicated_info)
    print(unit_test.null_rows)
    print(unit_test.categorical_columns_value)
    print(unit_test.numeric_columns_value)