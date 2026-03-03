"""
    Redis Cache Component for Interview Report Service This component handles storing and matching user data 
    from two topics: 'userAnswer' and 'userBehavioral' using Redis.
    When data from both topics with the same session ID is available, 
    it triggers the eventHandler for further processing.
"""
# Import Headers
from redis import Redis
from . EventHandler import eventHandler
import os
import dotenv
import json
import time
import logging

# program configurations
dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
logger: logging = logging.getLogger("python")

redis_client = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0, decode_responses=True)

TOPIC1_PREFIX = "userAnswer:"
TOPIC2_PREFIX = "userBehavioral:"
WAIT_TIME = 3

# functions Portion's
def processMatchedData(data1: dict | None, data2: dict | None) -> None:
    """ Process matched data from both topics.
        Args:
            data1 (dict): Data from topic 'userAnswer'.
            data2 (dict): Data from topic 'userBehavioral'.
            Returns:
            None
    """
    logger.info("Data send to eventHandler successfully.")
    eventHandler(data1=data1, data2=data2)
    

def saveToRedis(topic: str, sessionid: str, data: dict) -> None:
    """ Save data to Redis with expiration.
        Args:
            topic (str): Topic name.
            sessionid (str): Session ID.
            data (dict): Data to be stored. 
        Returns:
            None
    """
    if topic == "userAnswer":
        redis_client.setex(f"{TOPIC1_PREFIX}{sessionid}", 60*10, json.dumps(data)) 
    else:
        redis_client.setex(f"{TOPIC2_PREFIX}{sessionid}", 60*10, json.dumps(data))

def checkMatch(sessionid: str) -> bool:
    """ Check if data from both topics with the same session ID is available in Redis.
        Args:
            sessionid (str): Session ID.
        Returns:
            bool: True if matched data is found and processed, False otherwise.
    """
    data1 = redis_client.get(f"{TOPIC1_PREFIX}{sessionid}")
    data2 = redis_client.get(f"{TOPIC2_PREFIX}{sessionid}")

    if data1 and data2:
        redis_client.delete(f"{TOPIC1_PREFIX}{sessionid}")
        redis_client.delete(f"{TOPIC2_PREFIX}{sessionid}")
        processMatchedData(json.loads(data1), json.loads(data2))
        return True
    return False

def tryMatchAnyUser() -> None:
    """ Try to find any matching user data from both topics in Redis.
        Returns:
            bool: True if a match is found and processed, False otherwise.
    """
    keys_topic1 = redis_client.keys(f"{TOPIC1_PREFIX}*")

    for key in keys_topic1:
        sessionid = key.split(":")[1]
        if checkMatch(sessionid):
            return True
    return False

def handleMessage(topic: str, message: dict) -> None:
    """ Handle incoming messages by saving them to Redis and attempting to match data from both topics.
        Args:
            topic (str): Topic name.
            message (dict): Incoming message data.
        Returns:
            None
    """
    sessionid = message["sessionid"]
    saveToRedis(topic, sessionid, message)
    if checkMatch(sessionid):
        return
    logger.info(f"Waiting {WAIT_TIME}s for matching userId={sessionid}.")
    time.sleep(WAIT_TIME)

    if checkMatch(sessionid):
        return
    logger.info("Trying any user for sessionid matching.")
    tryMatchAnyUser()