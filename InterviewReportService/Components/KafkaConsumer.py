"""
Documentation:
    VideoAudioSeperatorService Kafka Consumer Module.
    This module sets up a Kafka consumer to listen for messages on the
    'video_analysis_request' topic.

Returns:
    dict | None: The message data consumed from Kafka, or None on failure.
"""

# Import Headers
from kafka import KafkaConsumer
import dotenv
import os
import json
import time
import logging

# program configurations
dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
logger: logging = logging.getLogger("python")

# functions Portion's
def kafkaConsumer():
    """Create and return a Kafka consumer with error handling."""
    try:
        consumer = KafkaConsumer(
            'userAnswer',
            'userBehavioral',
            bootstrap_servers=os.getenv("KAFKA_BROKER_URL"),
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id='userAnswerGroup',
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        logger.info("Kafka Consumer connected successfully.")
        return consumer
    except Exception as e:
        logger.exception(f"Failed to create Kafka consumer: {e}")
        time.sleep(5)
    return None

def startConsumer(handleMessage):
    """Start the Kafka consumer and process messages using the provided event handler."""
    consumer = kafkaConsumer()
    logger.info("Kafka Consumer started waiting for messages.")
    for message in consumer:
        data = message.value
        handleMessage(topic=message.topic, message=data)
        consumer.commit()
    
# Example usage (remove in production)
# if __name__ == "__main__":
#     while True:
#         msg = startConsumer()
#         print(msg)