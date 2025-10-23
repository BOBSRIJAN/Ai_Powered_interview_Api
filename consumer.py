from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'videoAnalysisRequest',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='kraft-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("🚀 Listening for messages...\n")
for message in consumer:
    print(f"📥 Received: {message.value}")
