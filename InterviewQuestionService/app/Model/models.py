import mongoengine as me

class UserQuestionHistory(me.Document):
    userid: str = me.StringField(required=True, unique=False)
    sessionid: str = me.StringField(required=True, unique=True)
    slotonequestions: list = me.ListField(required=True)
    slottwoquestions: list = me.ListField()
    remanning: int = me.IntField(default=0)
    numberofquestions: int = me.IntField(default=0)
    createdAt = me.DateTimeField()
    
    def __str__(self):
        return f"user id{self.userid} and session was {self.sessionid}"