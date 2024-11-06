import json
import os
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from PIL import Image
from io import BytesIO


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = GOOGLE_API_KEY)

class AI:
    # 
    def __init__(self,
                 image=None,
                 context='You are a Kazi Mtaani AI,an API embedded assistant to help recruiters and job seekers connect. You help the api in candidate sourcing by awarding scores to applicants, providing user Support and replying to away messages and enquiries',
                 prompt ='',
                 model ='gemini-1.5-flash'
                 ):
        self.image = image
        self.prompt = prompt
        self.model_name = model
        self.context = context
    
    def generateAIresponse(self):      
        content=[]
        if self.prompt:
             content.append(self.prompt)

        if self.image != None:
            self.model_name = 'gemini-pro-vision'        
            content.append(self.image)

        if len(content) > 0:
            
            model = genai.GenerativeModel(self.model_name,system_instruction=self.context,
                                          safety_settings=None , )
            response = model.generate_content(content,stream=True)
            response.resolve()
            # my_json = self.to_markdown(response.text)
            # airesp= json.dumps(my_json)
            return response.text
        
    def to_markdown(self,text):
            text = text.replace('•', '  *')
            return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

