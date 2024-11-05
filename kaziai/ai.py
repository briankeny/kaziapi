import json
import os
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
# from PIL import Image
# from io import BytesIO


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = GOOGLE_API_KEY)

class AI:
    # 
    def __init__(self,image=None,prompt=''):
        self.image = image
        self.prompt = prompt
        self.model_name = 'gemini-pro'
    
    def generateAIresponse(self):      
        content=[]
        if self.prompt:
             content.append(self.prompt)
        if self.image != None:
            self.model_name = 'gemini-pro-vision'        
            content.append(self.image)

        if len(content) > 0:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(content,stream=True)
            response.resolve()
            # my_json = self.to_markdown(response.text)
            # airesp= json.dumps(my_json)
            return response.text
        
    def to_markdown(self,text):
            text = text.replace('•', '  *')
            return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

