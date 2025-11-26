
from kafka import KafkaProducer
from django.conf import settings
import json

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(topic_key, data):
    topic = settings.KAFKA_TOPICS_4.get(topic_key)
    if not topic:
        raise ValueError(f"Kafka topic not found for key: {topic_key}")
    producer.send(topic, value=data)
    producer.flush()
