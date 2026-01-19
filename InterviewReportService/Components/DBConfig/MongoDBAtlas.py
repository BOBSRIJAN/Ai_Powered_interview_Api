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
class UserReport(me.Document):
    userid = me.StringField(required=True)
    sessionid = me.StringField(required=True, unique=True)
    questionandanswer = me.ListField(me.DictField())
    behavioralimprovement = me.StringField(required=True)
    improvementsuggestion = me.StringField(required=True)
    overallscore = me.IntField(min_value=1, max_value=100)
    createdAt = me.DateTimeField()
    
    def __str__(self):
        return UserReport.userid