from llmConnect import generateSqlTableSchema, generateSQlTableData , generateSQlTableToQuery
from json import loads 
import mysql.connector 
from os import environ

try: 
    database = mysql.connector.connect(
        host=environ.get("MYSQL_HOST"),
        user=environ.get("MYSQL_USER"),
        password=environ.get("MYSQL_PASSWORD"),
        database=environ.get("MYSQL_DATABASE")
    )

    cursorObject = database.cursor()

except Exception as e:
    print("Error connecting to database")
    print(e)



def getPromptSchema(prompt: str):
    return loads(generateSqlTableSchema(prompt))

def getPromptData(tableStructure: str):
    return loads(generateSQlTableData(tableStructure))

def getSQLQueryFromSchema(schema: str):
    return generateSQlTableToQuery(schema)


def createSQLTable(DDLquery: str):
    cursorObject.execute(DDLquery)
    return True

def addDataToSQLTable(data: list[list]):
    pass


if __name__ == "__main__":
    try:
        prompt = "Create a SQL table that showcases company product info. Company name: Sarath Industries,Industry: E Commerce"
        schema = getPromptSchema(prompt)
        data = getPromptData(str(schema))
        query = getSQLQueryFromSchema(str(schema))
        print(query)
        #print(schema)
        #print(data)
    except Exception as e:
        print("Hit an exception")
        print(e)
    
    #createSQLTable(schema)
    #addDataToSQLTable(data)