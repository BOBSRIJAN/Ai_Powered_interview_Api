from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VideoAnalysisRequestSerializer
from .Components.kafkaProducer import send_to_kafka

@api_view(['POST'])
def videoAnalysisRequest(request):
    if request.method == 'POST':
        serializer = VideoAnalysisRequestSerializer(data=request.data)
    if serializer.is_valid():
        send_to_kafka("video_analysis_request", serializer.validated_data)
        return Response({'status': 'Data sent to Kafka'}, status=status.HTTP_201_CREATED)
    return Response({"error": "Invalid request method or Incomplete request data"}, status=status.HTTP_400_BAD_REQUEST)
