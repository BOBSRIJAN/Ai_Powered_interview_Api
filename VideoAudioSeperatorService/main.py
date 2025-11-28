"""Documentation:
        VideoAudioSeperatorService Main Module. This module serves as the entry point for the 
        Video Audio Seperator Service.It initializes the Kafka consumer and starts 
        processing messages using the event handler.
    Returns:
        None: This function does not return any value.
    
"""
# Import Headers
from Components.EventHandler import eventHandler
from Components.KafkaConsumer import startConsumer

# # Entry point of Video Audio Seperator Service
if __name__ == "__main__":
    startConsumer(eventHandler)