from google import genai 
from google.genai import types 
from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel
from typing import Dict


def readSystemInstruction(type:str ):
    if type == "pptx":
        with open("systemInstructions/pptx.txt", "r") as f:
            return f.read()
    elif type == "docx":
        with open("systemInstructions/docx.txt", "r") as f:
            return f.read()

load_dotenv()


class SlideConfig(BaseModel):
    slide_layouts: int
    title: str
    subtitle: str

   

class PresentationConfig(BaseModel):
    RootModel: Dict[str, SlideConfig]

    



client = genai.Client(api_key=getenv("geminiAPI"))


def testWorking():
    response = client.models.generate_content(
    model='gemini-2.0-flash-exp', contents='What is your name?'
)
    print(response.text)

#testWorking()

def generatePPT(prompt: str):
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=prompt,
        config=types.GenerateContentConfig(system_instruction=readSystemInstruction("pptx"),response_mime_type='application/json',temperature=0)
    )
    #print(response.text)

    return response.text


def generateDocx(prompt: str):
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=prompt,
        config=types.GenerateContentConfig(system_instruction=readSystemInstruction("docx"),response_mime_type='application/json',temperature=0)
    )
    #print(response.text)

    return response.text

#generatePPT()
#generateDocx()

if __name__ == "__main__":
    prompt = "Create a Word Document which showcases the company goals for the upcoming year. Comapny name is XYZ, it is an IT service company"
    #generatePPT()
    print(generateDocx(prompt))