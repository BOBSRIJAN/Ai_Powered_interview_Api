import mongoengine as me

class Resume(me.Document):
    userId = me.StringField(required=True)
    url = me.StringField(required=True)
    jobDescription = me.StringField(required=True) 
    createdAt = me.DateTimeField()

    def __str__(self):
        return f"{self.userId}"


class ResumeAnalyzeMetaData(me.Document):
    userId = me.StringField(required=True)
    data = me.StringField(required=True)
    
    def __str__(self):
        return f"{self.userId}"