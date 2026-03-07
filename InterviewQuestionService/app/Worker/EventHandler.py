from app.Model.models import UserQuestionHistory
from . LLM import geminiAi
import os
import logging
import dotenv
import json

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

def eventHandler(Data: dict) -> None:
    logger.info("Data resaved at event handler.")
    if Data is None:
        logger.info("Event handler resaved data is None.")
        return None
    
    try:
        User: UserQuestionHistory = UserQuestionHistory.objects(userid=Data['userid'], sessionid=Data['sessionid']).first()
    except Exception as e:
        logger.exception(f"During user question history getting time an unaccepted Exception: {e}")
        
    if User is None:
        logger.info("User question history not found.")
        return

    QuestionsDict = Data.get('Questions')
    query = f"Data: {QuestionsDict}\n{os.getenv('remanningInterviewQuestions')} {User.remanning}"
    
    response = geminiAi(query)
    cleanData = response.strip().removeprefix("```json").removesuffix("```").strip()
    readyToSend = json.loads(cleanData)
    
    User.slottwoquestions = readyToSend
    User.remanning = 0
    
    try:
        User.save()
    except Exception as e: 
        logger.info(f"During record saving time Exception: {e}")
        
    logger.info("Slot two question generate Successfully.")