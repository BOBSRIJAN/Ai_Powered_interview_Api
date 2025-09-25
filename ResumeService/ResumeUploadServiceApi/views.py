from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ResumeAnalyzeMetaData
from .serializers import ResumeSerializer, ResumeAnalyzeMetaDataSerializer
from .Components.LLM import gemini
from .Components.CvToText import CvToSimpleText
from .Components.StrToJsonAndJsonToStr import Converter
from datetime import datetime
import dotenv
import requests
import os

dotenv.load_dotenv()

@api_view(['GET'])
def User(request):
    if request.method == 'GET':
        Data = ResumeAnalyzeMetaData.objects.all()
        serializer = ResumeAnalyzeMetaDataSerializer(Data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def AnalyzeWithDocument(request):
    if request.method == 'POST':
        serializer = ResumeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save

        response = requests.get(url=serializer.data['url'], stream=True)
        with open("ResumeData/downloaded.pdf", "wb") as f:
            f.write(response.content)

        textData = CvToSimpleText.extractTextFromPdf("ResumeData/downloaded.pdf")
        textData += f"  {os.getenv('analyze')} this is the job Description{serializer.data['jobDescription']}"
        Feedback = gemini(textData)

        readyToSend = Converter.StrToJson(Feedback.replace("```", "").replace("json", ""))
        readyToSend['userid'] = serializer.data['userid']

        ResumeAnalyzeMetaData.objects(userid=readyToSend['userid']).update_one(
            set__Data=Converter.JsonToStr(readyToSend),
            set__createdAt=datetime.utcnow(),
            upsert=True
        )
        return Response(readyToSend, status=status.HTTP_200_OK)
    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def AnalyzeWithJson(request):
    if request.method == 'POST':
        resumeJsonStr = Converter.JsonToStr(request.data)
        resumeJsonStr += f"  {os.getenv('analyze')} this is the job Description {request.data['jobDescription']}"
        
        Feedback = gemini(resumeJsonStr)
        
        readyToSend = Converter.StrToJson(Feedback.replace("```", "").replace("json", ""))
        readyToSend['userid'] = request.data['userid']
        
        ResumeAnalyzeMetaData.objects(userid=readyToSend['userid']).update_one(
            set__Data=Converter.JsonToStr(readyToSend),
            set__createdAt=datetime.utcnow(),
            upsert=True
        )
        return Response(readyToSend, status=status.HTTP_200_OK)
    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
