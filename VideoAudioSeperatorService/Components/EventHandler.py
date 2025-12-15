"""
Documentation:
    VideoAudioSeperatorService Event Handler Module. This module handles events triggered by messages 
    consumed from Kafka.

    Returns:
        None: This function processes the event and does not return any value.
"""
# Import Headers
from . VideoToMp3AndVideoConf import videoToAudioConverter
from . uplodeToCloudinary import uplodeAudioAndVideo
from . kafkaProducer import sendToKafka
from . DeleteDownloadData import deleteFilesInDirectory
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
    AudioFileName = f"Audio\\{data["userid"]}Audio.wav"

    print(f"Downloading video from URL:")
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Video downloaded successfully!")
    else:
        print("Failed to download file. Status:", response.status_code)

    videoToAudioConverter(video_path=save_path, audio_path=AudioFileName)
    links = uplodeAudioAndVideo(AudioFileName=AudioFileName)

    if not links:
        print("Failed to upload files to Cloudinary.")

    links.update({
            "userid": data["userid"],
            "sessionid": data["sessionid"],
            "question": data["question"],
            "questionno": data["questionno"],
            "videourl" : data["videourl"],
            "totalnumberofquestion": data["totalnumberofquestion"]
        })
    print("Links obtained from Cloudinary:")
    
    sendToKafka(data=links)
    print("Links sent to Kafka successfully!")
    
    deleteFilesInDirectory("Audio")
    deleteFilesInDirectory("Video")
    return None

# Example usage (remove in production)
# if __name__ == "__main__":
#     eventHandler()