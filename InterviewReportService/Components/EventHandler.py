from . SendToDbAndKafka import if_user_report_is_ready_send_to_kafka_and_db
from . LLM import geminiAi
import dotenv
import os
import json

dotenv.load_dotenv()
def eventHandler(data1: dict | None, data2: dict | None) -> None:
    """
    Handles the event by processing input data, generating a user report using Gemini AI,
    and sending the report to Kafka and the database.
        Args:
            data1 (dict | None): The first input data dictionary.
            data2 (dict | None): The second input data dictionary.
        Returns:
            None
    """
    prompt = f""" {os.getenv('userReport')} Return ONLY valid JSON with double quotes. Input: data_1={data1} and data_2={data2} """
    response = geminiAi(prompt)
    
    if response: 
        try: 
            clean = (response.replace("```", "").replace("json", "").strip())
            jsondata = json.loads(clean)
            jsondata["userid"] = data1["userid"]
            jsondata["sessionid"] = data1["sessionid"]
            jsondata["Questions"] = data1["Questions"]

            actual_answers = jsondata["actualanswer"]   
            for i, q in enumerate(jsondata["Questions"]):
                q["actualquestionanswer"] = actual_answers[i]
            del jsondata["actualanswer"]
        except Exception as e:
            print(f"Exception: {e}")

    status = if_user_report_is_ready_send_to_kafka_and_db(UserData=jsondata)
    print(status)
    return None