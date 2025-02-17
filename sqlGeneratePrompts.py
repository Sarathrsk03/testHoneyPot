from sql import createTableAndInsertData
from llmConnect import generateSQLPrompts
from json import loads
def createSQlPrompts(companyName:str, industry:str):
    prompt = f"Company name: {companyName}, Industry: {industry}"
    return prompt

if __name__ == "__main__":
    try:
        prompt = createSQlPrompts("Divij Industries","Textiles")
        prompts = loads(generateSQLPrompts(prompt))
        #print(prompts)
        for i in prompts:
            print(i,"\n")
            createTableAndInsertData(i)
            print("-"*100,"\n")
    except Exception as e:
        print("Hit an exception")
        print(e)

