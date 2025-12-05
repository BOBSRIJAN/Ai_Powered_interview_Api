"""Event Handler Module
    This module handles events related to video processing, including downloading videos,
    analyzing them for behavioral insights, saving results to a database and Kafka, and cleaning up downloaded files.
    Returns:    
        None: This function does not return any value.
    """
# Import Headers
from Components.DeleteDownloadData import delete_files_in_directory
from Components.videoAnalyze import analyze_candidate_video
from Components.sendTodbAndKafka import save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka
import requests

# functions Portion's
def eventHandler(data: str | None) -> None:
    """Handles the event of processing a video for behavioral analysis.
    Args:
        data (str | None): The input data containing video URL and user information.
    Returns:
        None: This function does not return any value.
    """
    save_path = "Video\\downloadedVideo.mp4"
    response = requests.get(data['videourl'], stream=True)

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