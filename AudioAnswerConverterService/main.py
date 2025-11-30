"""Main module to start the Audio Answer Converter Service by initializing the Kafka consumer with the event handler."""
# Import Headers
from Components.EventHandler import eventHandler
from Components.KafkaConsumer import startConsumer

# # Entry point of Audio To Answer Converter Service
if __name__ == "__main__": 
    startConsumer(eventHandler)