from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .Components.VoiceTotext import ListenAudioFromFile
from .Components.sendTodbAndKafka import save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka
from .Components.DeleteDownloadData import delete_files_in_directory
import requests
import os 

# Create your views here.
@api_view(['POST'])
def AudioToText(request):
    data = request.data
    url = data['Audiourl']

    save_dir = "Formator\\Audio"
    os.makedirs(save_dir, exist_ok=True)

    filename = f"{data['userid']}.wav"
    file_path = os.path.join(save_dir, filename)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File downloaded successfully at: {file_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
    
    answerText = ListenAudioFromFile(f"{save_dir}\\{filename}")
    
    AnswerFormat = {
        "userid":data['userid'],
        "question": data['question'],
        'answer': answerText,
        "totalnumberofquestion": data['totalnumberofquestion'],
    }
    response = save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka(data=AnswerFormat, topic_key='userAnswer')
    print(response['kafka_status'], response['status'], response['message'])
    delete_files_in_directory(save_dir)
    return Response({"status": "Message processed"}, status=status.HTTP_201_CREATED)