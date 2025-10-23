from kafka import KafkaConsumer
from django.conf import settings
import requests, json, logging, time, threading

logger = logging.getLogger(__name__)
_started = False  # Prevent multiple threads

def start_kafka_consumer():
    """
    Starts Kafka consumer in a background thread
    """
    global _started
    if _started:
        logger.info("Kafka consumer already running, skipping re-start.")
        return
    _started = True

    thread = threading.Thread(target=_consume_loop, daemon=True)
    thread.start()
    logger.info("✅ Kafka background consumer thread started.")


def _consume_loop():
    """
    Background Kafka consumer loop
    """
    try:
        consumer = KafkaConsumer(
            settings.KAFKA_TOPICS['video_analysis_request'],
            bootstrap_servers=settings.KAFKA_BROKER_URL,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id=settings.KAFKA_CONSUMER_GROUP,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )

        api_url = f"http://127.0.0.1:{settings.APP_PORT}/interviewservice/api/v1/videoandaudioseperator/taskHendelar/"

        logger.info("🎧 Listening to Kafka topic in background...")

        for message in consumer:
            data = message.value
            logger.info(f"📩 Received message: {data}")

            try:
                response = requests.post(api_url, json=data)
                if response.status_code == 201:
                    logger.info("✅ Data processed successfully.")
                else:
                    logger.error(f"❌ Failed: {response.status_code}, retrying...")
                    time.sleep(5)

            except Exception as e:
                logger.error(f"⚠️ Error sending data: {e}")
                time.sleep(5)

    except Exception as e:
        logger.critical(f"🔥 Kafka consumer crashed: {e}")
