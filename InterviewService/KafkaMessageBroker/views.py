from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VideoAnalysisRequestSerializer
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@api_view(['POST'])
def videoAnalysisRequest(request):
    if request.method == 'POST':
        serializer = VideoAnalysisRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        producer.send('videoAnalysisRequest', value=serializer.data)
        producer.flush()
        producer.close()
        return Response({'status':'Response recorded'}, status=status.HTTP_201_CREATED)
    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
