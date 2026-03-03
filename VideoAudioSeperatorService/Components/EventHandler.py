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
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger: logging = logging.getLogger("python")

# functions Portion's
def VideoDownloader(url: str, filename:str) -> None:
    """
    Download video from the given URL and save it to the specified filename.
    Args:
        url (str): The URL of the video to download.
        filename (str): The path where the downloaded video will be saved.
    Returns:
        None
    """
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
        logger.exception(f"An error occurred: {e}")

def eventHandler(data: dict) -> None:
    """
    Handle events triggered by Kafka messages.
        Args:
            data (dict): The data received from Kafka message.
        Returns:
            None
    """
    logger.info("Event Handler triggered with data")
    # savePath = "Video\\downloaded_video.mp4"
    # AudioFileName = f"Audio\\{data["userid"]}Audio.wav"
    BASE_DIR = Path.cwd()

    video_dir = BASE_DIR / "Video"
    audio_dir = BASE_DIR / "Audio"

    video_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)

    savePath = video_dir / "downloaded_video.mp4"
    AudioFileName = audio_dir / f"{data.get('userid')}Audio.wav"

    logger.info(f"Downloading video from URL:")
    VideoDownloader(url=data.get('videourl'), filename=savePath)
    
    videoToAudioConverter(video_path=savePath, audio_path=AudioFileName)
    links: dict = uplodeAudioAndVideo(AudioFileName=AudioFileName)

    if not links:
        logger.error("Failed to upload files to Cloudinary.")

    links.update({
            "userid": data.get('userid'),
            "sessionid": data.get('sessionid'),
            "question": data.get('question'),
            "questionno": data.get('questionno'),
            "videourl" : data.get('videourl'),
            "totalnumberofquestion": data.get('totalnumberofquestion')
        })
    logger.info("Links obtained from Cloudinary:")
    
    sendToKafka(data=links)
    logger.info("Links sent to Kafka successfully.")
    
    deleteFilesInDirectory("Audio")
    deleteFilesInDirectory("Video")
    return None

# Example usage (remove in production)
# if __name__ == "__main__":
#     eventHandler()