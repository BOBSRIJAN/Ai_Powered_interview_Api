import mongoengine as me

# Create your models here.
class userQuestionMetaData(me.Document):
    userid = me.StringField(required=True)
    userquestion = me.StringField(required=True)
    createdAt = me.DateTimeField()

    def __str__(self):
        return f"User id; {self.userid}"