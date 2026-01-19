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
class UserQuestionBehavioralAnalysis(me.Document):
    userid = me.StringField(required=True)
    sessionid = me.StringField(required=True, unique=True)
    questions = me.ListField(me.DictField())
    behavioral = me.ListField()  
    totalnumberofquestion = me.IntField(default=0)
    tillQuestioncount = me.IntField(default=0)
    
    def __str__(self):
        return self.userid