"""
    MongoDB Atlas Configuration File for Interview Question Service 
"""
# Import Headers
import mongoengine as me 
import dotenv
import logging
import os

# program configurations
dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

# function portion
def establishConnection() -> None:
    """ Establish Connection with MongoDB Atlas """
    me.connect(
        db="ResumeService",
        host=os.getenv('MongoDbUrl'),
        alias="default"
    )
    logger.info("MongoDB Atlas connection established successfully.")
    
def terminatedConnection() -> None: 
    """ Terminate Connection with MongoDB Atlas """
    me.disconnect(alias="default")
    logger.info("MongoDB Atlas Connection Terminated with Atlas.")