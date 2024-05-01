from langchain_openai import ChatOpenAI
from vertexai.language_models import CodeGenerationModel
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv
import os
import json 
load_dotenv()

def read_setting(json_file):
    with open(json_file, "r") as file:
        data = file.read()
    return json.loads(data)

class model:
    def __init__(self, temperature=None, max_token=None):
        self.setting = read_setting("model/input/setting.json")
        if temperature == None or max_token == None:
            setting = self.setting['llm_configuration']
        if temperature == None:
            self.temperature = setting["temperature"]
        else:
            self.temperature = temperature
        if max_token == None:
            self.max_token = setting["max_token"]
        else:
            self.max_token = max_token
       

    def set_Codey(self):
        parameters = {
            "candidate_count": 1,
            "max_output_tokens": self.max_token,
            "temperature": self.temperature
        }
        print("Codey is run!")
        self.model = CodeGenerationModel.from_pretrained("code-bison@002")
        self.response = self.model.predict(prefix = self.prompt_text, **parameters)
        self.input_token = self.response._prediction_response.metadata['tokenMetadata']['inputTokenCount']['totalTokens']
        self.output_token = self.response._prediction_response.metadata['tokenMetadata']['outputTokenCount']['totalTokens'] 
        self.output = self.response.text
    
    def set_Gemini(self):
        parameters = {
            "candidate_count": 1,
            "max_output_tokens": self.max_token,
            "temperature": self.temperature
        }
        print("Gemini is run!")
        self.model = GenerativeModel("gemini-1.0-pro-002")
        chat = self.model.start_chat()
        self.response = chat.send_message([self.prompt_text], generation_config=parameters)
        self.input_token = self.response._raw_response.usage_metadata.prompt_token_count
        self.output_token = self.response._raw_response.usage_metadata.total_token_count
        self.output = self.response.text
        
    def set_chatGPT(self, model):
        api_key = os.environ['OPENAI_API_KEY']
        self.model = ChatOpenAI(model=model, temperature=self.temperature, max_tokens=self.max_token, openai_api_key=api_key)
        self.response = self.model.invoke(self.prompt_text)
        self.output = self.response.content
        print(self.response)
        self.input_token = self.response.response_metadata['token_usage']['prompt_tokens']
        self.output_token = self.response.response_metadata['token_usage']['completion_tokens']

    def run(self, chosen_model, prompt_text):
        self.prompt_text = prompt_text

        if chosen_model == "Gemini-Pro" :
            self.set_Gemini()
        elif chosen_model == "GCP Codey":
            self.set_Codey()  
        elif chosen_model == "ChatGPT3-Turbo":
            self.set_chatGPT("gpt-3.5-turbo")
        elif chosen_model == "ChatGPT4":
            self.set_chatGPT("gpt-4")

        print(self.input_token, self.output_token)
        self.token_details = {"input":self.input_token, "output":self.output_token, "total": self.input_token + self.output_token}
    
if __name__ == "__main__":
    model = model()
    prompt = 'Query the user from table A'
    model.run("Gemini-Pro", prompt)
    print(model.output)
    