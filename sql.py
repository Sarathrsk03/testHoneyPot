from llmConnect import generateSqlTableSchema, generateSQlTableData , generateSQlTableToQuery, generateSQLDataToQuery
from json import loads 
import mysql.connector 
from os import environ
from dotenv import load_dotenv
import csv

fr = open("queries.csv","a")
writer = csv.writer(fr)

#load_dotenv()

try: 
        database = mysql.connector.connect(
            host=environ.get("MYSQL_HOST"),
            user=environ.get("MYSQL_USER"),
            password=environ.get("MYSQL_PASSWORD"),
            database=environ.get("MYSQL_DATABASE"),
            ssl_disabled=True
        )

        cursorObject = database.cursor()
        print(cursorObject)
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
    if "sql" in DDLquery:
        DDLquery = DDLquery.replace("```sql","")
        DDLquery = DDLquery.replace("```","")
    #print(DDLquery)
    #cursorObject.execute(DDLquery)
    return DDLquery


def addDataToSQLTable(data: list[list],schema:list[dict]):
    prompt = f"{str(data[1:])} to the table {str(schema)}"
    sqlQuery = generateSQLDataToQuery(prompt)
    if "sql" in sqlQuery:
        sqlQuery = sqlQuery.replace("```sql","")
        sqlQuery = sqlQuery.replace("```","")
    return sqlQuery
    

def createTableAndInsertData(prompt:str):
    schema = getPromptSchema(prompt)
    data = getPromptData(str(schema))
    query = getSQLQueryFromSchema(str(schema))
    dataQuery = addDataToSQLTable(data,schema)
    executableQuery = createSQLTable(query)
    print (executableQuery,"\n")
    print(dataQuery)
    writer.writerow([prompt,executableQuery,dataQuery])
    cursorObject.execute(executableQuery)
    cursorObject.execute(dataQuery)
    database.commit()


if __name__ == "__main__":
    try: 
        database = mysql.connector.connect(
            host=environ.get("MYSQL_HOST"),
            user=environ.get("MYSQL_USER"),
            password=environ.get("MYSQL_PASSWORD"),
            database=environ.get("MYSQL_DATABASE")
        )

        cursorObject = database.cursor()
        print(cursorObject)
    except Exception as e:
        print("Error connecting to database")
        print(e)
"""
    try:
        prompt = "Create a SQL table that showcases company product info. Company name: Sarath Industries,Industry: E Commerce"
        schema = getPromptSchema(prompt)
        data = getPromptData(str(schema))
        query = getSQLQueryFromSchema(str(schema))
        dataQuery = addDataToSQLTable(data,schema)
        #print(query)
        #print(schema)
        #print("\n")
        #print(data)
        #print("\n")
        #print(dataQuery)
    except Exception as e:
        print("Hit an exception")
        print(e)


    executableQuery = createSQLTable(query)
    print(executableQuery)
    print(dataQuery)
    cursorObject.execute(executableQuery)
    cursorObject.execute(dataQuery)
    database.commit()"""
