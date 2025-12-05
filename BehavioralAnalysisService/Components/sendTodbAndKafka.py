""" Module to save or update user behavioral analysis data to MongoDB and send to Kafka if session is complete.
    Documentation:
        This module provides functionality to save or update user behavioral analysis data in MongoDB. 
        If the user has completed all questions,the data is sent to a specified Kafka topic. 
"""
# Import Headers
from . kafkaProducer import sendToKafka
from . DBConfig.MongoDBAtlas import UserQuestionBehavioralAnalysis
import json

# functions Portion's
def save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka(data: dict | None, topic_key: str | None) -> dict[str, str] | dict[str,]:
    """ 
    Saves or updates the user's behavioral analysis session in MongoDB. If the session is complete,
    sends the data to a specified Kafka topic.
    Args:
        data (dict): A dictionary containing the following
            keys:
                - 'userid' (str): Unique identifier for the user.
                - 'question' (str): The question asked to the user.
                - 'questionno' (int): The question number in the session.
                - 'behavioral' (str): The behavioral analysis provided by the user.
                - 'totalnumberofquestion' (int): Total number of questions in the session.
        topic_key (str): Kafka topic to send data when the session is complete.
    Returns:
        dict: A dictionary containing the status of the operation and Kafka sending status.
    """
    
    userid = data.get("userid")
    sessionid = data.get("sessionid")
    question = data.get("question")
    questionno = data.get("questionno")
    behavioral = data.get("behavioral")
    total = data.get("totalnumberofquestion")
 
    if not all([userid, question, questionno, behavioral, total]):
        return {"status": "error", "message": "Missing required fields"}

    user = UserQuestionBehavioralAnalysis.objects(userid=userid, sessionid=sessionid).first()

    if user:
        user.questions.append({
            "questionno": questionno,
            "question": question
        })
        user.behavioral.append(behavioral)
        user.tillQuestioncount += 1
        user.totalnumberofquestion = total
        user.save()

        response = {
            "status": "updated",
            "message": f"Added question {user.tillQuestioncount}/{user.totalnumberofquestion}",
            "data": json.loads(user.to_json()),
            "kafka_status" : None
        }

        if user.tillQuestioncount >= user.totalnumberofquestion:
            if topic_key:
                try:
                    kafka_data = response["data"]
                    sendToKafka(topic_key, data=kafka_data)
                    response["kafka_status"] = f"Data sent to Kafka topic '{topic_key}'"
                except Exception as e:
                    response["kafka_status"] = f"Failed to send to Kafka: {str(e)}"
        return response
    else:
        user = UserQuestionBehavioralAnalysis(
            userid=userid,
            sessionid=sessionid,
            questions=[{
                "questionno": questionno,
                "question": question
            }],
            behavioral=[behavioral],
            totalnumberofquestion=total,
            tillQuestioncount=1
        )
        user.save()

        response = {
            "status": "created",
            "message": "New user record created",
            "data": json.loads(user.to_json()),
            "kafka_status" : None
        }

        if user.tillQuestioncount >= user.totalnumberofquestion:
            if topic_key:
                try:
                    sendToKafka(topic_key, user.to_mongo().to_dict())
                    response["kafka_status"] = f"Data sent to Kafka topic '{topic_key}'"
                except Exception as e:
                    response["kafka_status"] = f"Failed to send to Kafka: {str(e)}"
        return response