"""Event Handler Module
    This module handles events related to video processing, including downloading videos,
    analyzing them for behavioral insights, saving results to a database and Kafka, and cleaning up downloaded files.
    Returns:    
        None: This function does not return any value.
    """
# Import Headers
from Components.DeleteDownloadData import delete_files_in_directory
from Components.videoAnalyze import analyzeCandidateVideo
from Components.sendTodbAndKafka import save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka
import urllib.request
from pathlib import Path
import uuid

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
        print(f"An error occurred: {e}")

def eventHandler(data: dict | None) -> None:
    """Handles the event of processing a video for behavioral analysis.
    Args:
        data (str | None): The input data containing video URL and user information.
    Returns:
        None: This function does not return any value.
    """
    print("Data Received At Event Handler....")
    video_filename = (f"{data['userid']}_" f"{data['sessionid']}_" f"q{data['questionno']}_" f"{uuid.uuid4().hex}.mp4")
    savePath = VIDEO_DIR / video_filename

    try:
        VideoDownloader(url=data['videourl'], filename=str(savePath))
        result = analyzeCandidateVideo(str(savePath))
        print(f"Analyze Done:\n{result}")
    except Exception as e:
        print("Analyze failed:", e)
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
            print(f"Deleted: {savePath}")

    BehavioralFormat = {
        "userid": data["userid"],
        "sessionid": data["sessionid"],
        "question": data["question"],
        "behavioral": result,
        "questionno": data["questionno"],
        "totalnumberofquestion": data["totalnumberofquestion"],
    }

    kafka_data = save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka(data=BehavioralFormat, topic_key='userBehavioral')
    print(kafka_data['kafka_status'], kafka_data['status'], kafka_data['message'])
    return None