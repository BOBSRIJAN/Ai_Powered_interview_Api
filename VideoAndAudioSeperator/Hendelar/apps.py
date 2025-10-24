from django.apps import AppConfig
from .Components.KafkaConsumer import start_kafka_consumer

class HendelarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Hendelar'
    def ready(self):
        """
        Run background Kafka consumer when Django starts
        """
        try:
            start_kafka_consumer()
        except Exception as e:
            print(f"Failed to start Kafka consumer: {e}")