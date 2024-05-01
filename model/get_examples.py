import pandas as pd
from transformers.utils import logging
from sentence_transformers import SentenceTransformer
from sentence_transformers import util
from torch import tensor
logging.set_verbosity_error()

class vector_search:
    def __init__(self, file_path='model/input/example.csv'):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
    def example_vector(self):   
        self.data['question_vectors'] = self.data['Question'].apply(lambda x: self.model.encode(x))
        self.data.to_csv(self.file_path, index=False)

    def compute_search(self, prompt, n=10):
        self.example_vector()
        input_vector = self.model.encode(prompt)
        similarities = self.data['question_vectors'].apply(lambda x: util.cos_sim(tensor(input_vector),tensor(x))[0][0].item()).reset_index(drop=True)
        similarities = similarities[similarities > 0.5]
        top_indices = similarities.nlargest(n).index
        top_problems = self.data.iloc[top_indices]['Question']
        top_solutions = self.data.iloc[top_indices]['SQL']
        return top_problems, top_solutions

if __name__ == "__main__":
    prompt = "get the retention rate"
    search = vector_search()
    top_problems, top_solutions = search.compute_search(prompt, 5)
