from app.Model.models import UserQuestionHistory
from . LLM import geminiAi
from . StrToJsonAndJsonToStr import Converter
import os
import logging
import dotenv

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

def eventHandler(Data: dict) -> None:
    logger.info("Data resaved in event handler......")
    User = UserQuestionHistory.objects(userid=Data['userid'], sessionid=Data['sessionid']).first()
    if User is None:
        return
    QuestionsDict = Data['Questions']
    query = f"Data: {QuestionsDict}\n{os.getenv('remanningInterviewQuestions')} {User.remanning}"
    response = geminiAi(query)
    readyToSend = Converter.StrToJson(response.replace("```", "").replace("json", ""))
    User.slottwoquestions = readyToSend
    User.remanning = 0
    User.save()
    logger.info("slot two questions generations done......")