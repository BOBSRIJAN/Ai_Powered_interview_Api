"""

"""
# Import Headers
import mongoengine as me 
import dotenv
import os

# program configurations
dotenv.load_dotenv()

# function portion
def establishConnection() -> None:
    me.connect(
        db="InterviewService",
        host=os.getenv('MongoDbUrl'),
        alias="default"
    )
    print("Connection Establish with Atlas...")
    
def terminatedConnection() -> None: 
    me.disconnect(alias="default")
    print("Connection Terminated with Atlas...")