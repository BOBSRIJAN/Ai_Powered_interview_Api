from Components.RedisCache import handleMessage
from Components.KafkaConsumer import startConsumer

if __name__ == "__main__":
     startConsumer(handleMessage)