import mongoengine as me
import datetime

class Resume(me.Document):
    userid = me.StringField(required=True)
    url = me.StringField(required=True)
    jobDescription = me.StringField(required=True)
    createdAt = me.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return f"{self.userid}"

class ResumeAnalyzeMetaData(me.Document):
    userid = me.StringField(required=True, unique=True)
    Data = me.StringField(required=True)
    createdAt = me.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return f"{self.userid} → {self.Data[:50]}..." 
