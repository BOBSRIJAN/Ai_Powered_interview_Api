"""Module to save or update user question-answer data in MongoDB and send to Kafka topics based on progress."""
# Import Headers
from .kafkaProducer import sendToKafka
from .DBConfig.MongoDBAtlas import UserQuestionAnswer
import json

# functions Portion's


def save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka(data, topic_1, topic_2):
    """_Saves or updates the user's question-answer session in MongoDB. If the session is complete or halfway through,
        sends the data to specified Kafka topics.   
    Args:
        data (dict): A dictionary containing the following
            keys:
                - 'userid' (str): Unique identifier for the user.
                - 'sessionid' (str): Unique identifier for every Interview session.
                - 'question' (str): The question asked to the user.
                - 'questionno' (int): The question number in the session.
                - 'answer' (str): The answer provided by the user.
                - 'totalnumberofquestion' (int): Total number of questions in the session.
        topic_1 (str): Kafka topic to send data when the session is complete.
        topic_2 (str): Kafka topic to send data when halfway through the session.
    Returns:
        dict: A dictionary containing the status of the operation and Kafka sending status.
    """

    if not isinstance(data, dict):
        return {
            "status": "error",
            "message": "Invalid data format",
            "kafka_status": None
        }

    userid = data.get("userid")
    sessionid = data.get("sessionid")
    question = data.get("question")
    questionno = data.get("questionno")
    answer = data.get("answer")
    total = data.get("totalnumberofquestion")

    if not all([userid, question, questionno, answer, total]):
        return {
            "status": "error",
            "message": "Missing required fields",
            "kafka_status": None
        }

    user = UserQuestionAnswer.objects(
        userid=userid, sessionid=sessionid).first()

    if user:
        user.Questions.append({
            "questionno": questionno,
            "question": question,
            "answer": answer
        })
        user.tillQuestioncount += 1
        user.totalnumberofquestion = total
        
        try:
            user.save()
        except Exception as e:
            return {
                "status": "error",
                "message": f"Database error: {str(e)}",
                "kafka_status": None
            }

        response = {
            "status": "updated",
            "message": f"Added question {user.tillQuestioncount}/{user.totalnumberofquestion}",
            "kafka_status": None
        }

        half = total // 2

        if user.tillQuestioncount == half - 2:
            try:
                payload = json.loads(user.to_json())
                sendToKafka(topic_2, data=payload)
                response["kafka_status"] = f"Sent to Kafka topic '{topic_2}'"
            except Exception as e:
                response["kafka_status"] = f"Failed to send to Kafka 2: {str(e)}"

        if user.tillQuestioncount >= total:
            try:
                payload = json.loads(user.to_json())
                sendToKafka(topic_1, data=payload)
                response["kafka_status"] = f"Sent to Kafka topic '{topic_1}'"
            except Exception as e:
                response["kafka_status"] = f"Failed to send to Kafka 1: {str(e)}"

        return response

    else:
        user = UserQuestionAnswer(
            userid=userid,
            sessionid=sessionid,
            Questions=[{
                "questionno": questionno,
                "question": question,
                "answer": answer
            }],
            totalnumberofquestion=total,
            tillQuestioncount=1
        )
        
        try:
            user.save()
        except Exception as e:
            return {
                "status": "error",
                "message": f"Database error: {str(e)}",
                "kafka_status": None
            }

        response = {
            "status": "created",
            "message": "New user record created",
            "kafka_status": None
        }

        half = total // 2

        if user.tillQuestioncount == half - 2:
            try:
                payload = json.loads(user.to_json())
                sendToKafka(topic_2, data=payload)
                response["kafka_status"] = f"Sent to Kafka topic '{topic_2}'"
            except Exception as e:
                response["kafka_status"] = f"Failed to send to Kafka 2: {str(e)}"

        if user.tillQuestioncount >= total:
            try:
                payload = json.loads(user.to_json())
                sendToKafka(topic_1, data=payload)
                response["kafka_status"] = f"Sent to Kafka topic '{topic_1}'"
            except Exception as e:
                response["kafka_status"] = f"Failed to send to Kafka 1: {str(e)}"
        return response