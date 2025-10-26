import mongoengine as me  

class UserQuestion(me.Document):
    userid = me.StringField(required=True, unique=True)
    Questions = me.ListField(me.DictField())  # each dict: { "question": "...", "answer": "..." }
    totalnumberofquestion = me.IntField(default=0)
    tillQuestioncount = me.IntField(default=0)
