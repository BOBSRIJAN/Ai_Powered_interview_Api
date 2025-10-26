from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .Components.DeleteDownloadData import delete_files_in_directory
from .Components.videoAnalyze import analyze_candidate_video

# Create your views here.
@api_view(['POST'])
def VideoAnalysis(request):
    data = request.data
    return Response({"status": "Message processed"}, status=status.HTTP_201_CREATED)