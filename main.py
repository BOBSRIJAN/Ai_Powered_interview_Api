from Components import CvToText
from Components import geminiAi
import dotenv
import os

dotenv.load_dotenv()

''' This is the main entry point of all the components '''
if __name__=="__main__":
  cvText = CvToText.CvToSimpleText.extractTextFromPdf(f'Components\\demoData\\srijanraycv.pdf')
  cvText += os.getenv('JsonDataFormat')

  data = geminiAi.Era_assistant(cvText)

  print(data.replace("```", "").replace("json", ""))

  # we will save the json data later!