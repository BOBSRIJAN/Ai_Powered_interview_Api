""" 
    Main Module for Behavioral Analysis Service
    This module serves as the entry point for the Behavioral Analysis Service.
    It starts the Kafka consumer to listen for video processing events.
"""
# Import Headers
from Components.EventHandler import eventHandler
from Components.KafkaConsumer import startConsumer

# # Entry point of Video Audio Seperator Service
if __name__ == "__main__":
    startConsumer(eventHandler)