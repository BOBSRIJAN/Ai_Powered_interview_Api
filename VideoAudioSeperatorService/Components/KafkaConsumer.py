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
            'video_analysis_request',
            bootstrap_servers=os.getenv("KAFKA_BROKER_URL"),
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id='VideoAudioSeperatorGroup',
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000,
            max_poll_interval_ms=600000,  
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        print("Kafka Consumer connected successfully.")
        return consumer
    except Exception as e:
        print(f"Failed to create Kafka consumer: {e}")
        time.sleep(5)
    return None

  
def startConsumer(eventHandler):
    """Start the Kafka consumer and process messages using the provided event handler.
    Args:
        eventHandler (function): A function to handle each consumed message.
    Returns:
        None
    """
    consumer = kafkaConsumer()
    print("Kafka Consumer started... \nwaiting for messages....")

    while True:
        records = consumer.poll(timeout_ms=2000)
        if not records:
            continue
        
        for tp, msgs in records.items():
            for msg in msgs:

                data = msg.value

                try:
                    eventHandler(data)
                except Exception as e:
                    print(f"Error while processing message: {e}")
                    continue
                try:
                    consumer.commit()
                    print("Message processed & committed.")
                except Exception as e:
                    print(f"CommitError: {e}")

# Example usage (remove in production)
# if __name__ == "__main__":
#     while True:
#         msg = startConsumer()
#         print(msg)