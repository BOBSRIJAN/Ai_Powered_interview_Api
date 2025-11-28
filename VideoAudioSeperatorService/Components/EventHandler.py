"""
Documentation:
    VideoAudioSeperatorService Event Handler Module. This module handles events triggered by messages 
    consumed from Kafka.

    Returns:
        None: This function processes the event and does not return any value.
"""
# Import Headers
from Components.VideoToMp3AndVideoConf import video_to_audio_and_video_conversion
from Components.uplodeToCloudinary import uplodeAudioAndVideo
from Components.kafkaProducer import sendToKafka
from Components.DeleteDownloadData import delete_files_in_directory
import requests

# functions Portion's
def eventHandler(data: dict) -> None:
    """
    Handle events triggered by Kafka messages.
        Args:
            data (dict): The data received from Kafka message.
        Returns:
            None
    """
    print("Event Handler triggered with data:")
    save_path = "Video\\downloaded_video.mp4"
    response = requests.get(data['videourl'], stream=True)
    print(f"Downloading video from URL:")
    
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Video downloaded successfully!")
    else:
        print("Failed to download file. Status:", response.status_code)

    video_to_audio_and_video_conversion(FilePath=save_path, Filename=data['userid'])
    VideoFileName = f"Video\\{data['userid']}Video.mp4"
    AudioFileName = f"Audio\\{data['userid']}Audio.wav"
    links = uplodeAudioAndVideo(VideoFileName=VideoFileName, AudioFileName=AudioFileName)

    if not links:
        print("Failed to upload files to Cloudinary.")

    links.update({
            'userid': data['userid'],
            'question': data['question'],
            'questionno': data['questionno'],
            'totalnumberofquestion': data['totalnumberofquestion']
        })

    print("Links obtained from Cloudinary:")
    sendToKafka(data=links)
    print("Links sent to Kafka successfully!")
    delete_files_in_directory("Audio")
    delete_files_in_directory("Video")
    return None

# Example usage (remove in production)
# if __name__ == "__main__":
#     eventHandler()