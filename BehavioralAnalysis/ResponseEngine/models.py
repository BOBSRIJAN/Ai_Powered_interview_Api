import mongoengine as me

# Create your models here.
class UserQuestionBehavioralAnalysis(me.Document):
    userid = me.StringField(required=True, unique=True)
    questions = me.ListField(me.DictField())
    behavioral = me.ListField()  
    totalnumberofquestion = me.IntField(default=0)
    tillQuestioncount = me.IntField(default=0)