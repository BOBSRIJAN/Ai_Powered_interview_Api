from fastapi import (
    APIRouter, 
        HTTPException, 
    status,
)
from app.Model.models import UserQuestionHistory
from app.Schemas.RequestModel import (
    InitializeInterviewRequest,
        InterviewSlotTwoQuestionsRequest,
            UserSlotOneQuestionsPostRequestResponse,
            UserSlotTwoQuestionsPostRequestResponse,
        UserQuestionHistoryRequest,
    UserQuestionHistoryResponse,
)
from . Components.StrToJsonAndJsonToStr import Converter
from . Components.CvToText import CvToSimpleText
from . Components.LLM import geminiAi
from . Components.RandomSessionIdGenerate import generateSessionId
from . Components.FileDownloader import downloadFile
from . Components.DeleteDownloadData import deleteFilesInDirectory
import logging
import dotenv
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")
dotenv.load_dotenv()
router = APIRouter(prefix="/interviewservice/api/v1/initializeinterview", tags=["initializeinterview"])

@router.post("/getfirstslotquestion", response_model=UserSlotOneQuestionsPostRequestResponse, status_code=status.HTTP_201_CREATED)
async def getFirstSlotQuestion(payload: InitializeInterviewRequest) -> UserSlotOneQuestionsPostRequestResponse:
    if payload.specificquestionrequirement == True:
        query = f"{os.getenv('initializeInterviewQuestionsjson')}topic: {payload.subjectortopic}no of question: {payload.numberofquestions / 2}lavel: {payload.level}"

        response = geminiAi(query)
        if response is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Gemini not sending the response")
        logger.info("Question generated successfully.")

        readyToSend = Converter.StrToJson(response.replace("```", "").replace("json", ""))
        readyToSend['userid'] = payload.userid
        readyToSend['sessionid'] = generateSessionId()

        UserQuestionHistory(
            userid=payload.userid,
                sessionid=readyToSend['sessionid'],
                    slotonequestions=readyToSend['slotonequestions'],
                        slottwoquestions=None,
                            remanning= payload.numberofquestions / 2,
                                numberofquestions=payload.numberofquestions
        ).save()

    else:
        downloadFile(payload.resumeurl)
        textData = CvToSimpleText.extractTextFromPdf("pdf\\pdf.pdf")
        query = f"resume data: {textData}, {os.getenv('initializeInterviewQuestionspdf')} no of question: {payload.numberofquestions / 2}lavel: {payload.level}"
        deleteFilesInDirectory("pdf")

        response = geminiAi(query)
        if response is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Gemini not sending the response")
        logger.info("Question generated successfully.")

        readyToSend = Converter.StrToJson(response.replace("```", "").replace("json", ""))
        readyToSend['userid'] = payload.userid
        readyToSend['sessionid'] = generateSessionId()

        UserQuestionHistory(
            userid=payload.userid,
                sessionid=readyToSend['sessionid'],
                    slotonequestions=readyToSend['slotonequestions'],
                        slottwoquestions=None,
                            remanning= payload.numberofquestions / 2,
                                numberofquestions=payload.numberofquestions
        ).save()
        
    return UserSlotOneQuestionsPostRequestResponse(
        userid=readyToSend['userid'],
            sessionid=readyToSend['sessionid'],
                slotonequestions=readyToSend['slotonequestions'],
                    remanning= payload.numberofquestions / 2, 
                        numberofquestions=payload.numberofquestions
    )


@router.post("/getsecondslotquestion", response_model=UserSlotTwoQuestionsPostRequestResponse, status_code=status.HTTP_201_CREATED)
async def getSecondSlotQuestion(paylode: InterviewSlotTwoQuestionsRequest):
    user = UserQuestionHistory.objects(userid=paylode.userid, sessionid=paylode.sessionid).first()
    if user and user.slottwoquestions:
        return UserSlotTwoQuestionsPostRequestResponse(
            userid=paylode.userid,
                sessionid=paylode.sessionid,
                    slottwoquestions=user.slottwoquestions
        )
    else:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Data is not ready yet, Still processing...")


@router.post("/getuserquestionhistory", response_model=UserQuestionHistoryResponse, status_code=status.HTTP_200_OK)
async def getUserQuestionHistory(paylode: UserQuestionHistoryRequest):
    user = UserQuestionHistory.objects(userid=paylode.userid, sessionid=paylode.sessionid).first()
    if user:
        return UserQuestionHistoryResponse(
            userid=paylode.userid,
                sessionid=paylode.sessionid,
                    slotonequestions=user.slotonequestions,
                        slottwoquestions=user.slottwoquestions,
                            remanning=user.remanning,
                                numberofquestions=user.numberofquestions
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for the given user id and session id, please check and try again.")