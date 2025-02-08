from llmConnect import generatePrompt,generatePPT,generateDocx, generateXLSX
from json import loads
from docxCreate import generateDocxFromDict
from pptCreate import generatePPTFromDict
from xlsxCreate import createXLSXFromDict
from time import sleep

import os 
industry = os.getenv("industtry") 
companyName = os.getenv("companyName") 
role = os.getenv("role")

desktop = os.path.join(os.path.expanduser("~"), "Desktop")

def createPrompts(companyName: str, industry: str, role: str) -> list:
    prompt = f"Company Name: {companyName}\nIndustry: {industry}\nRole: {role}\n\n"
    
    try :
        responseStr= generatePrompt(prompt)
    except:
        print("Error in generating prompts")
    
    return loads(responseStr)

if __name__ == "__main__":
    prompts = createPrompts("VIT University","Education","University")
    sleep(15)
    #print(ans)
    #print(type(ans))

    for filePrompt in prompts: 
        fileName = filePrompt["file_name"]
        fileType = filePrompt["file_type"]
        contentPrompt = filePrompt["prompt"]

        fileName = os.path.join(desktop,fileName)
        
        print(f"File Name: {fileName}\nFile Type: {fileType}\nContent Prompt: {contentPrompt}\n\n")

        if fileType == "pptx":
            pptDict = loads(generatePPT(contentPrompt))
            #print(pptDict)
            generatePPTFromDict(pptDict,fileName)
            print("PPTX file generated")
            
        
        elif fileType == "docx":
            docxDict = loads(generateDocx(contentPrompt))
            generateDocxFromDict(docxDict,fileName)
            print("DOCX file generated")
        
        elif fileType == "xlsx":
            xlsxNested = loads(generateXLSX(contentPrompt))
            createXLSXFromDict(xlsxNested,fileName)
            #print(xlsxNested)
            print("XLSX file generated")

        sleep(5)
        








