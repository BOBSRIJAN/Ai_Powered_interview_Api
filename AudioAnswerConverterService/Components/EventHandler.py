"""
    Event Handler for Audio Answer Converter Service.
    This module handles the processing of audio answers by downloading the audio file,
    converting it to text, and saving or updating the user's question-answer session in the database.
"""
# Import Headers
from Components.VoiceTotext import ListenAudioFromFile
from Components.sendTodbAndKafka import save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka
from Components.DeleteDownloadData import delete_files_in_directory
import requests
import os 

# functions Portion's
def eventHandler(data: dict) -> None:
    """
    Handles the event of processing an audio answer.
    Downloads the audio file from the provided URL, converts it to text,
    and saves or updates the user's question-answer session in the database.
    Args:
        data (dict): A dictionary containing the following
            keys:
                - 'audiourl' (str): URL of the audio file to be processed.
                - 'userid' (str): Unique identifier for the user.
                - 'question' (str): The question asked to the user.
                - 'questionno' (int): The question number in the session.
                - 'totalnumberofquestion' (int): Total number of questions in the session.
    Returns:
            None
    """
    
    url = data['audiourl']
    save_dir = "Audio"
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
        'questionno': data['questionno'],
        'answer': answerText,
        "totalnumberofquestion": data['totalnumberofquestion'],
    }
    
    response = save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka(data=AnswerFormat, topic_1='userAnswer', topic_2='contradictQuestions')
    print(response['kafka_status'], response['status'], response['message'])
    delete_files_in_directory(save_dir)
    return None

# Example usage (remove in production)
# if __name__ == "__main__":
#     sample_data = {
#         'audiourl': 'https://example.com/path/to/audio.wav',
#         'userid': 'user123',
#         'question': 'What is your favorite color?',
#         'questionno': 1,
#         'totalnumberofquestion': 5
#     }
#     eventHandler(sample_data)