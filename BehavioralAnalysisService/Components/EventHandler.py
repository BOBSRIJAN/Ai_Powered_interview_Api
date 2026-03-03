"""Event Handler Module
    This module handles events related to video processing, including downloading videos,
    analyzing them for behavioral insights, saving results to a database and Kafka, and cleaning up downloaded files.
    Returns:    
        None: This function does not return any value.
    """
# Import Headers
from Components.videoAnalyze import analyzeCandidateVideo
from Components.sendTodbAndKafka import save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka
import urllib.request
from pathlib import Path
import uuid
import logging

# program configurations
logging.basicConfig(level=logging.INFO)
logger: logging = logging.getLogger("python")

BASE_DIR = Path.cwd()
VIDEO_DIR = BASE_DIR / "Video"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

# functions Portion's
def VideoDownloader(url: str, filename:str) -> None:
    """
    Downloads a video from the specified URL and saves it to the given filename.
        Args:
            url (str): The URL of the video to download.
            filename (str): The path where the downloaded video will be saved.
        Returns:
            None: This function does not return any value.
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
        logger.info(f"An error occurred: {e}")

def eventHandler(data: dict | None) -> None:
    """Handles the event of processing a video for behavioral analysis.
    Args:
        data (str | None): The input data containing video URL and user information.
    Returns:
        None: This function does not return any value.
    """
    logger.info("Data Received At Event Handler.")
    video_filename = (f"{data.get('userid')}_" f"{data.get('sessionid')}_" f"q{data.get('questionno')}_" f"{uuid.uuid4().hex}.mp4")
    savePath = VIDEO_DIR / video_filename

    try:
        VideoDownloader(url=data.get('videourl'), filename=str(savePath))
        result = analyzeCandidateVideo(str(savePath))
        logger.info(f"Analyze Done:\n{result}")
    except Exception as e:
        logger.exception("Analyze failed:", e)
        result = {
            "noOfHuman": 0,
            "posture": "unknown",
            "eye_contact_score": 0,
            "emotion": [],
            "overallBehavioralScore": 0
        }
    finally:
        if savePath.exists():
            savePath.unlink()
            logger.info(f"Deleted: {savePath}")

    BehavioralFormat = {
        "userid": data.get('userid'),
        "sessionid": data.get('sessionid'),
        "question": data.get('question'),
        "behavioral": result,
        "questionno": data.get('questionno'),
        "totalnumberofquestion": data.get('totalnumberofquestion'),
    }

    response = save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka(data=BehavioralFormat, topic_key='userBehavioral')
    logger.info(f'Kafka status: {response.get('kafka_status')} massage status: {response.get('status')} massage: {response.get('message')}')
    return None