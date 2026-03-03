"""
    Event Handler for Audio Answer Converter Service.
    This module handles the processing of audio answers by downloading the audio file,
    converting it to text, and saving or updating the user's question-answer session in the database.
"""
# Import Headers
from Components.VoiceTotext import WhisperAudioToText
from Components.sendTodbAndKafka import save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
import logging

# program configurations
logging.basicConfig(level=logging.INFO)
logger: logging = logging.getLogger("python")

# functions Portion's
def safeDownloadBytes(url: str) -> bytes | None:
    """ Download audio file from the given URL with retry logic. 
        Args:
            url (str): URL of the audio file to download.
        Returns:
            bytes | None: The content of the audio file as bytes, or None if download fails
    """
    try:
        logger.info("Trying to downlode the audio file from Cloudinary.")
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        response = session.get(url, timeout=10)
        response.raise_for_status()
        logger.info("Audiio data downloded Successfully.")
        return response.content

    except Exception as e:
        logger.info("Audiio data download failed: ", e)
        return None

def eventHandler(data: dict) -> None:
    """ Handle the event of receiving audio answer data.
        Args:
            data (dict): A dictionary containing the audio URL and metadata.
    """
    logger.info("Audio data recive at event handler.")
    audio_bytes = safeDownloadBytes(data['audiourl'])

    if not audio_bytes:
        logger.info("Skipping processing due to download failure.")
        return
    logger.info("Audio data going to whisper for transformation.")
    answerText = WhisperAudioToText(audio_bytes)

    AnswerFormat = {
        "userid": data.get('userid'),
        "sessionid": data.get('sessionid'),
        "question": data.get('question'),
        "questionno": data.get('questionno'),
        "answer": str(answerText),
        "totalnumberofquestion": data.get('totalnumberofquestion'),
    }
    logger.info("Trying to store the processed data in to the Kafka and data")
    response = save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka(
        data=AnswerFormat, 
        topic_1='userAnswer', 
        topic_2='contradictQuestions'
    )
    
    logger.info(f'Kafka status: {response.get('kafka_status')} massage status: {response.get('status')} massage: {response.get('message')}')

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