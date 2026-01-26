
# Import Headers
from fastapi import APIRouter, HTTPException, status
from app.Model.models import ResumeAnalyzeMetaData
from app.Routers.Components.FileDownloader import downloadFile
from app.Routers.Components.Converter import StrToJson, JsonToStr
from app.Routers.Components.ExtractResumeText import extractTextFromDocx, extractTextFromPdf
from app.Routers.Components.LLM import geminiAi
from app.Schemas.ExchangeModel import (
    AnalyzeWithDocumentRequest, AnalyzeWithDocumentResponse,
    AnalyzeWithJsonRequest, AnalyzeWithJsonResponse
)
import logging
import dotenv
import os

# program configurations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")
dotenv.load_dotenv()
router = APIRouter(prefix="/resumeanalyzer/api/v1", tags=["JavaServise's"])

# function and route portion
@router.get("/healthcheck", status_code=status.HTTP_200_OK)
def healthCheck():
    """
        Health Check Endpoint
            Returns:  
                dict: Health Check Response
    """
    logger.info("Resume Service Health is Normal!")
    return{"details": "Resume Service Health is Normal!"}

@router.post("/analyzewithdocument", response_model=AnalyzeWithDocumentResponse, status_code=status.HTTP_200_OK)
async def analyzeWithDocument(paylode: AnalyzeWithDocumentRequest) -> AnalyzeWithDocumentResponse:
    """
    Analyze Resume With Document Url Endpoint
        Args:
            paylode (AnalyzeWithDocumentRequest): Analyze With Document Request Model
        Returns:
            AnalyzeWithDocumentResponse: Analyze With Document Response Model
    """
    logger.info("Request Receive Analyze With Document Function Ststus: Processing...")
    if paylode.url.endswith('.pdf') or paylode.url.endswith('.PDF'):
        downloadFile(paylode.url)
        textData: str = extractTextFromPdf('downloads/file.pdf')
        textData += f"  {os.getenv('analyzefordoc')} this is the job Description{paylode.jobDescription}"
        Feedback: str = geminiAi(textData)
        readyToSend: dict = StrToJson(Feedback.replace("```", "").replace("json", ""))
    elif paylode.url.endswith('.docx') or paylode.url.endswith('.DOCX'):
        downloadFile(paylode.url)
        textData: str = extractTextFromDocx('downloads/file.pdf')
        textData += f"  {os.getenv('analyzefordoc')} this is the job Description{paylode.jobDescription}"
        Feedback: str = geminiAi(textData)
        readyToSend: dict = StrToJson(Feedback.replace("```", "").replace("json", ""))
    else:
        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='Exception: Url file must be a pdf or docx')

    ResumeAnalyzeMetaData(
        userid=paylode.userid,
        score=readyToSend.get('score'),
        atsCompatibility=readyToSend.get('atsCompatibility'),
        strengths=readyToSend.get('strengths'),
        improvements=readyToSend.get('improvements'),
        keywords=readyToSend.get('keywords'),
        suggestions=readyToSend.get('suggestions')
    ).save()

    return AnalyzeWithDocumentResponse(
        userid=paylode.userid,
        score=readyToSend.get('score'),
        atsCompatibility=readyToSend.get('atsCompatibility'),
        strengths=readyToSend.get('strengths'),
        improvements=readyToSend.get('improvements'),
        keywords=readyToSend.get('keywords'),
        suggestions=readyToSend.get('suggestions')
    )

@router.post("/analyzewithjson", response_model=AnalyzeWithJsonResponse, status_code=status.HTTP_200_OK)
async def analyzeWithJson(paylode: AnalyzeWithJsonRequest) -> AnalyzeWithJsonResponse:
    """
    Analyze Resume With Json Endpoint
        Args:
            paylode (AnalyzeWithJsonRequest): Analyze With Json Request Model
        Returns:
            AnalyzeWithJsonResponse: Analyze With Json Response Model
    """
    logger.info("Request Receive Analyze With Json Function Ststus: Processing...")
    resumeData: str = JsonToStr(paylode.resume)
    resumeData += f"  {os.getenv('analyzefordoc')} this is the job Description{paylode.jobDescription}"
    Feedback: str = geminiAi(resumeData)
    readyToSend: dict = StrToJson(Feedback.replace("```", "").replace("json", ""))
    
    ResumeAnalyzeMetaData(
        userid=paylode.userid,
        score=readyToSend.get('score'),
        atsCompatibility=readyToSend.get('atsCompatibility'),
        strengths=readyToSend.get('strengths'),
        improvements=readyToSend.get('improvements'),
        keywords=readyToSend.get('keywords'),
        suggestions=readyToSend.get('suggestions')
    ).save()

    return AnalyzeWithDocumentResponse(
        userid=paylode.userid,
        score=readyToSend.get('score'),
        atsCompatibility=readyToSend.get('atsCompatibility'),
        strengths=readyToSend.get('strengths'),
        improvements=readyToSend.get('improvements'),
        keywords=readyToSend.get('keywords'),
        suggestions=readyToSend.get('suggestions')
    )