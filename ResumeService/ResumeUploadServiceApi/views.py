from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Resume, ResumeAnalyzeMetaData
from .serializers import ResumeSerializer
from .Components.LLM import gemini
from .Components.CvToText import CvToSimpleText
from .Components.StrToJsonAndJsonToStr import Converter
from datetime import datetime
import dotenv
import requests
import os

dotenv.load_dotenv()

@api_view(['GET'])
def UserList(request):
    if request.method == 'GET':
        snippets = Resume.objects.all()
        serializer = ResumeSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def Analyze(request):
    if request.method == 'POST':
        PostData = request.data
        serializer = ResumeSerializer(data=PostData)
        
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(url=PostData['url'], stream=True)
        with open("ResumeData/downloaded.pdf", "wb") as f:
            f.write(response.content)

        textData = CvToSimpleText.extractTextFromPdf("ResumeData/downloaded.pdf")
        textData += os.getenv('analyze')
        Feedback = gemini(textData)

        FinalData = Feedback.replace("```", "").replace("json", "")
        readyToSend = Converter.StrToJson(FinalData)
        readyToSend['userid'] = PostData['userid']

        ResumeAnalyzeMetaData.objects(userid=readyToSend['userid']).update_one(
            set__Data=Converter.JsonToStr(readyToSend),
            set__createdAt=datetime.utcnow(),
            upsert=True
        )
        return Response(readyToSend, status=status.HTTP_201_CREATED)
    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)