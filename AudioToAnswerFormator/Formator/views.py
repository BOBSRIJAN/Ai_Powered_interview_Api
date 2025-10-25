from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['POST'])
def AudioToText(request):
    data = request.data
    print(data)
    return Response({"status": "Message processed"}, status=status.HTTP_201_CREATED)
