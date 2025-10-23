from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import time

# Create your views here.
@api_view(['POST'])
def taskHendelar(request):
    data = request.data
    print(f"🎯 Processing received Kafka data: {data}")

    # Example business logic
    # Save to DB, forward to another API, run AI model, etc.
    time.sleep(12)

    return Response({"status": "Message processed"}, status=status.HTTP_201_CREATED)
