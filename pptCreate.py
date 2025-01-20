from pptx import Presentation
from llmConnect import generatePPT
from json import loads
import os 

industry = os.getenv("industry")
companyName = os.getenv("companyName") 
role = os.getenv("role")


def generateSamplePPT():
    # Create a presentation object
    prs = Presentation()    

    slider = prs.slides.add_slide(prs.slide_layouts[0])
    title = slider.shapes.title
    subtitle = slider.placeholders[1]

    title.text = "Hello, World!"
    subtitle.text = "This is a subtitle"

    # Save the presentation
    prs.save("test.pptx")


try:
    prompt = f"Create a powerpoint which showcases the company financials Comapny name is {companyName}, it is an {industry} company"
    pptDict = loads(generatePPT(prompt))
    print(pptDict)
    print(type(pptDict))
except Exception as e:
    print("Hit an exception")
    print(e)
    

def generatePPTFromDict(pptDict):
    # Create a presentation object
    prs = Presentation()    

    for slide in pptDict:
         for slide_number, slide_details in slide.items():
            slider = prs.slides.add_slide(prs.slide_layouts[slide_details["slide_layouts"]])

            title = slider.shapes.title
            title.text = slide_details["title"]

            if slide_details["slide_layouts"] == 0:
                subtitle = slider.placeholders[1]
                subtitle.text = slide_details["subtitle"]
            elif slide_details["slide_layouts"] == 1:
                content = slider.placeholders[1]
                content.text = slide_details["subtitle"]

    # Save the presentation
    prs.save("./Desktop/testDataFromLLM.pptx")
        
generatePPTFromDict(pptDict)




