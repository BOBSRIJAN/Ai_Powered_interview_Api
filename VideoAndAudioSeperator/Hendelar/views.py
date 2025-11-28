from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .Components.VideoToMp3AndVideoConf import video_to_audio_and_video_conversion
from .Components.uplodeToCloudinary import uplodeAudioAndVideo
from .Components.kafkaProducer import send_to_kafka
from .Components.DeleteDownloadData import delete_files_in_directory
import requests

# Create your views here.
@api_view(['POST'])
def taskHendelar(request) -> Response:
    data = request.data
    save_path = "Hendelar\\Video\\downloaded_video.mp4"
    response = requests.get(data['videourl'], stream=True)
    
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Video downloaded successfully!")
    else:
        print("Failed to download file. Status:", response.status_code)
        
    video_to_audio_and_video_conversion(FilePath=save_path, Filename=data['userid'])
    VideoFileName = f"Hendelar\\Video\\{data['userid']}_Video.mp4"
    AudioFileName = f"Hendelar\\Audio\\{data['userid']}_Audio.wav"
    links = uplodeAudioAndVideo(VideoFileName=VideoFileName, AudioFileName=AudioFileName)

    if not links:
        print("Failed to upload files to Cloudinary.")

    links.update(
        {
            'userid': data['userid'],
            'question': data['question'],
            'questionno': data['questionno'],
            'totalnumberofquestion': data['totalnumberofquestion']
        }
    )

    print("Links obtained from Cloudinary:")
    send_to_kafka(topic_key="AudioAndVideoRequest", data=links)
    print("Links sent to Kafka successfully!")
    delete_files_in_directory("Hendelar/Audio")
    delete_files_in_directory("Hendelar/Video")
    return Response({"status": "Message processed"}, status=status.HTTP_201_CREATED)
