"""
    MongoDB Atlas Configuration and Document Definition for Audio Answer Converter Service.
    This module sets up the connection to MongoDB Atlas using environment variables
    and defines the UserQuestionAnswer document schema.
"""
# Import Headers
import mongoengine as me 
import dotenv
import os

# program configurations
dotenv.load_dotenv()
me.connect(
    db="InterviewService",
    host=os.getenv('MongoDbUrl'),
)

# class Portion's
class UserQuestionAnswer(me.Document):
    """ 
    MongoDB Document for storing user questions and answers.
        Fields:
            userid (str): Unique identifier for the user.
            Questions (list): List of dictionaries containing questions and answers.
            totalnumberofquestion (int): Total number of questions for the user.
            tillQuestioncount (int): Count of questions processed so far.
    """
    userid = me.StringField(required=True, unique=True)
    Questions = me.ListField(me.DictField())
    totalnumberofquestion = me.IntField(default=0)
    tillQuestioncount = me.IntField(default=0)
    
    def __str__(self):
        return UserQuestionAnswer.userid