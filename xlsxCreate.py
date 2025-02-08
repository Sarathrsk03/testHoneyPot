import xlsxwriter
from json import loads
from llmConnect import generateXLSX

def createTest():
    workbook = xlsxwriter.Workbook('test.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'Hello')
    worksheet.write('A2', 'World')

    workbook.close()

def createXLSXFromDict(xlsxNestedList: list[list], file_name="testDataFromLLM.xlsx"):
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    for row_idx, row in enumerate(xlsxNestedList):
        for col_idx, value in enumerate(row):
            worksheet.write(row_idx, col_idx, value)

    workbook.close()

if __name__ == "__main__":
    try:
        prompt = "Create a CSV file that showcases company employee info. Company name: Sarath Industries,Industry: E Commerce"
        xlsxDict = loads(generateXLSX(prompt))
        print(xlsxDict)
        print(type(xlsxDict))
    except Exception as e:
        print("Hit an exception")
        print(e)
   
    createXLSXFromDict(xlsxDict)
