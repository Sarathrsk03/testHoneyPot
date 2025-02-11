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
    elif type == "prompt":
        with open("systemInstructions/promptCreate.txt", "r") as f:
            return f.read()
    elif type == "xlsx":    
        with open("systemInstructions/xlsx.txt", "r") as f:
            return f.read() 
    elif type == "sqlTable":
        with open("systemInstructions/sqlTable.txt","r") as f:
            return f.read()
    elif type == "sqlData":
        with open("systemInstructions/sqlData.txt","r") as f:
            return f.read()
    elif type == "schemaToQuery":
        with open("systemInstructions/schemaToQuery.txt","r") as f:
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

def generatePrompt(prompt: str):
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=prompt,
        config=types.GenerateContentConfig(system_instruction=readSystemInstruction("prompt"),response_mime_type='application/json',temperature=0)
    )
    return response.text


def generateXLSX(prompt: str):
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=prompt,
        config=types.GenerateContentConfig(system_instruction=readSystemInstruction("xlsx"),response_mime_type='application/json',temperature=0)
    )
    return response.text

def generateSqlTableSchema(prompt: str):
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=prompt,
        config=types.GenerateContentConfig(system_instruction=readSystemInstruction("sqlTable"),response_mime_type='application/json',temperature=0)
    )
    return response.text

def generateSQlTableData(prompt: str):
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=prompt,
        config=types.GenerateContentConfig(system_instruction=readSystemInstruction("sqlData"),response_mime_type='application/json',temperature=0)
    )
    return response.text

def generateSQlTableToQuery(schema: str):
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=schema,
        config=types.GenerateContentConfig(system_instruction=readSystemInstruction("schemaToQuery"),temperature=0)
    )
    return response.text



#generatePPT()
#generateDocx()

if __name__ == "__main__":
    #prompt = "Company name: Apple, Role: COO, Industry: Technology"
    #generatePPT()
    #print(generateDocx(prompt))
    #print(generatePrompt(prompt))
    prompt = "Create a sql table which showcases all the customer details"
    resposnse = generateSqlTableSchema(prompt)
    print(generateSQlTableData(resposnse))
    
