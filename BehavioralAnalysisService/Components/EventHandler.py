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

def eventHandler(data: str | None) -> None:
    """Handles the event of processing a video for behavioral analysis.
    Args:
        data (str | None): The input data containing video URL and user information.
    Returns:
        None: This function does not return any value.
    """
    print("Data Received At Event Handler....")
    savePath = "Video\\downloadedVideo.mp4"
    VideoDownloader(url=data['videourl'], filename=savePath)
    result = analyzeCandidateVideo(savePath)
    print(f"Analyze's Done This Was The Responce:\n{result}")

    BehavioralFormat = {
        "userid":data["userid"],
        "sessionid": data["sessionid"],
        "question": data["question"],
        "behavioral": result,
        "questionno": data["questionno"],
        "totalnumberofquestion": data["totalnumberofquestion"],
    }

    data = save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka(data=BehavioralFormat, topic_key='userBehavioral')
    print(data['kafka_status'], data['status'], data['message'])
    delete_files_in_directory('Video')
    return None