"""Documentation:
        VideoAudioSeperatorService Kafka Producer Module. This module sets up a Kafka producer to send messages to the
        'AudioVideoRequestTopic' topic. 
    Returns:
        dict | None: The message data sent to Kafka, or None on failure.
"""
# Import Headers
from kafka import KafkaProducer
import dotenv
import os
import json

# program configurations
dotenv.load_dotenv()
producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BROKER_URL"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# functions Portion's
def sendToKafka(data: dict) -> None:
    """
    Send data to Kafka topic.
        Args:
            data (dict): The data to be sent to Kafka.
        Returns:
            None
    """
    topic = 'AudioVideoRequestTopic'
    if not topic:
        raise ValueError(f"Kafka topic not found")
    producer.send(topic, value=data)
    producer.flush()

# Example usage (remove in production)
# if __name__ == "__main__":
#     sendToKafka()