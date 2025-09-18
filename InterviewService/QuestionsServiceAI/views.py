from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudentInterviewPerformanceDataSerializer

@api_view(['GET'])
def isActive(request):
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def PostVideoData(request):
    if request.method == 'POST':
        ResponseData = request.data
        ResponseData['status_code'] = '201 added'
        return Response(ResponseData, status=status.HTTP_201_CREATED)
    return Response(ResponseData, status=status.HTTP_400_BAD_REQUEST)