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
import urllib.request

# functions Portion's
def VideoDownloader(url: str, filename:str) -> None:
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')

        with urllib.request.urlopen(req, timeout=30) as response:
            with open(filename, 'wb') as out_file:
                chunk_size = 1024 * 1024
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
                    
    except Exception as e:
        print(f"An error occurred: {e}")
        
def eventHandler(data: dict) -> None:
    """
    Handle events triggered by Kafka messages.
        Args:
            data (dict): The data received from Kafka message.
        Returns:
            None
    """
    print("Event Handler triggered with data:")
    savePath = "Video\\downloaded_video.mp4"
    AudioFileName = f"Audio\\{data["userid"]}Audio.wav"

    print(f"Downloading video from URL:")
    VideoDownloader(url=data['videourl'], filename=savePath)
    
    videoToAudioConverter(video_path=savePath, audio_path=AudioFileName)
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