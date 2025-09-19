from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Resume, ResumeAnalyzeMetaData
from .serializers import ResumeSerializer
from .Components.LLM import gemini
import dotenv
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
        
        print(PostData['url'])
        
        return Response( status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
