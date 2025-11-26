from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .Components.DeleteDownloadData import delete_files_in_directory
from .Components.videoAnalyze import analyze_candidate_video
from .Components.sendTodbAndKafka import save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka
import requests

# Create your views here.
@api_view(['POST'])
def VideoAnalysis(request):
    data = request.data
    save_path = "ResponseEngine\\Video\\downloadedVideo.mp4"
    response = requests.get(data['Videourl'], stream=True)
    
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Video downloaded successfully!")
    else:
        print("Failed to download file. Status:", response.status_code)
    
    result = analyze_candidate_video(save_path)
    print(f"this was the responce:\n{result}")

    BehavioralFormat = {
        "userid":data['userid'],
        "question": data['question'],
        'behavioral': result,
        'questionno': data['questionno'],
        "totalnumberofquestion": data['totalnumberofquestion'],
    }
    data = save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka(data=BehavioralFormat, topic_key='userBehavioral')
    print(data['kafka_status'], data['status'], data['message'])
    delete_files_in_directory('ResponseEngine\\Video\\')
    return Response({"status": "Message processed"}, status=status.HTTP_201_CREATED)