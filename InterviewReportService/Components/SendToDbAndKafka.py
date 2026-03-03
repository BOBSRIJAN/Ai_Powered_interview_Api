# Import Headers
from . DBConfig.MongoDBAtlas import UserReport
from . kafkaProducer import sendToKafka

# functions Portion's
def if_user_report_is_ready_send_to_kafka_and_db(UserData: dict, topic: str ="UserReport") -> dict[str,str] | None:
    User = UserReport.objects(sessionid=UserData["sessionid"]).first()
    
    if User: 
        try:
            raise Exception("Something Went Wrong! Session Id Already Exist In DataBase:(")
        except Exception as e:
            print("Exception:", e)       
    else:
        try:
            User = UserReport(
                userid = UserData["userid"],
                sessionid = UserData["sessionid"],
                questionandanswer = UserData["Questions"],
                behavioralimprovement = UserData["behavioralimprovement"],
                improvementsuggestion =UserData["improvementsuggestion"],
                overallscore = UserData["overallscore"],
            )
            User.save()
        except Exception as e:
            return {"Status": f"Error: Unable to store data in the database {e}"}
        
        try:
            sendToKafka(topic=topic, data=UserData)
        except Exception as e:
            return {"Status": f"Error: Failed to send the data to Kafka {e}"}
        
        return {"Status": "Success: User added to the database and message sent to Kafka"}
    return None