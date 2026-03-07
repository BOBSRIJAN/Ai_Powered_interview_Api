
# Import Headers
from . SendToDbAndKafka import if_user_report_is_ready_send_to_kafka_and_db
from . LLM import geminiAi
import logging
import dotenv
import json
import os

# program configurations
dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
logger: logging = logging.getLogger("python")

# functions Portion's
def eventHandler(data1: dict, data2: dict) -> None:
    """
    Handles the event by processing input data, generating a user report using Gemini AI,
    and sending the report to Kafka and the database.
        Args:
            data1 (dict | None): The first input data dictionary.
            data2 (dict | None): The second input data dictionary.
        Returns:
            None
    """
    if not data1 and data2:
        logger.error("Both the parameter Data1 and Data2 are empty.")
        return None

    prompt = f"""{os.getenv('userReport')} Return ONLY valid JSON with double quotes. Input: data_1={data1} and data_2={data2}"""

    response = geminiAi(prompt)
    jsondata = None

    if response:
        try:
            clean = response.strip().removeprefix("```json").removesuffix("```").strip()
            jsondata = json.loads(clean)

            jsondata["userid"] = data1["userid"]
            jsondata["sessionid"] = data1["sessionid"]
            jsondata["Questions"] = data1["Questions"]

            actual_answers = jsondata.get("actualanswer", [])

            for i, q in enumerate(jsondata["Questions"]):
                if i < len(actual_answers):
                    q["actualquestionanswer"] = actual_answers[i]

            jsondata.pop("actualanswer", None)

        except Exception as e:
            logger.exception(f"Exception while parsing Gemini response: {e}")
            return None

    if jsondata:
        status = if_user_report_is_ready_send_to_kafka_and_db(UserData=jsondata)
        logger.info(status)

    return None