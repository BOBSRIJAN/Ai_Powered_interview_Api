from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Resume
from .serializers import ResumeSerializer

@api_view(['GET'])
def UserList(request):
    if request.method == 'GET':
        snippets = Resume.objects.all()
        serializer = ResumeSerializer(snippets, many=True)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])    
def AddUser(request):
    if request.method == 'POST':
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)