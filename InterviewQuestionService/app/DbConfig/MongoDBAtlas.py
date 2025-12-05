"""

"""
# Import Headers
import mongoengine as me 
import dotenv
import os

# program configurations
dotenv.load_dotenv()

# function portion
def establishConnection():
    me.connect(
        db="InterviewService",
        host=os.getenv('MongoDbUrl'),
    )