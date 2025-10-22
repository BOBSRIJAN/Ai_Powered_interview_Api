from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import(
userQuestionMetaDataSerializer,
requestDateSerializer,
questionHistorySerializer)
from .models import userQuestionMetaData
from .Components.LLM import geminiAi
from .Components.StrToJsonAndJsonToStr import Converter
import dotenv
from datetime import datetime
import os

dotenv.load_dotenv()

@api_view(['GET'])
def isActive(request):
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def questionHistory(request):
    if request.method == 'GET':
        data = userQuestionMetaData.objects.all()
        serializer = userQuestionMetaDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if not questionHistorySerializer(data=request.data).is_valid():
            return Response({'error': 'userid is required'}, status=status.HTTP_400_BAD_REQUEST)
        userid = request.data.get('userid')
        data = userQuestionMetaData.objects(userid=userid)
        if not data:
            return Response({'message': 'No records found for this userid'}, status=status.HTTP_404_NOT_FOUND)
        serializer = userQuestionMetaDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def getInterviewQuestions(request):
    if request.method == 'POST':
        serializer = requestDateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer['specificquestionrequirement'].value == True:
            query = f"{os.getenv('getQuestions')} topic: {request.data['subjectortopic']} no of question: {request.data['numberofquestiion']} lavel: {request.data['level']}"
            response = geminiAi(query)
            readyToSend = Converter.StrToJson(response.replace("```", "").replace("json", ""))
            readyToSend['userid'] = serializer.data['userid']
            userQuestionMetaData.objects(userid=readyToSend['userid']).update_one(
                set__userquestion=Converter.JsonToStr(readyToSend),
                set__createdAt=datetime.utcnow(),
                upsert=True
            )
            return Response(readyToSend, status=status.HTTP_200_OK)
        else:
            # later
            return Response({'status': 'wait bro'}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)