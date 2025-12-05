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

# program configurations
dotenv.load_dotenv()

# functions Portion's
def kafkaConsumer():
    """Create and return a Kafka consumer with error handling."""
    try:
        consumer = KafkaConsumer(
            'userAnswer',
            'userBehavioral',
            bootstrap_servers=os.getenv("KAFKA_BROKER_URL", "localhost:9092"),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='userAnswerGroup',
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        print("Kafka Consumer connected successfully.")
        return consumer
    except Exception as e:
        print(f"Failed to create Kafka consumer: {e}")
        time.sleep(5)
    return None

def startConsumer(handleMessage):
    """Start the Kafka consumer and process messages using the provided event handler."""
    consumer = kafkaConsumer()
    print("Kafka Consumer started... \nwaiting for messages....")
    for message in consumer:
        data = message.value
        handleMessage(topic=message.topic, message=data)
        consumer.commit()
    
# Example usage (remove in production)
# if __name__ == "__main__":
#     while True:
#         msg = startConsumer()
#         print(msg)