from sql import createTableAndInsertData
from llmConnect import generateSQLPrompts
from json import loads
from time import sleep

import os 
industry = os.getenv("industry") 
companyName = os.getenv("companyName") 

def createSQlPrompts(companyName:str, industry:str):
    prompt = f"Company name: {companyName}, Industry: {industry}"
    print(prompt)
    return prompt

if __name__ == "__main__":
    try:
        prompt = createSQlPrompts(companyName,industry)
        prompts = loads(generateSQLPrompts(prompt))
        print(prompts)
        for i in prompts[:5]:
            sleep(5)
            try: 
                print(i,"\n")
                createTableAndInsertData(i)
                print("-"*100,"\n")
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        print("Hit an exception")
        print(e)

