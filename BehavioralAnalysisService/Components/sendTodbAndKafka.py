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
def save_or_update_user_if_user_question_answer_session_is_done_send_to_kafka(data, topic_key):
    """ Saves or updates user behavioral analysis data in MongoDB. If the user has completed all questions, 
        sends the data to a specified Kafka topic.
    Args:   
        data (dict): A dictionary containing user behavioral analysis data.
        topic_key (str): The Kafka topic key to send data to if the session is complete.
    Returns:
        dict: A dictionary containing the status and message of the operation.
    """
    
    userid = data.get("userid")
    question = data.get("question")
    questionno = data.get("questionno")
    behavioral = data.get("behavioral")
    total = data.get("totalnumberofquestion")
 
    if not all([userid, question, questionno, behavioral, total]):
        return {"status": "error", "message": "Missing required fields"}

    user = UserQuestionBehavioralAnalysis.objects(userid=userid).first()

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