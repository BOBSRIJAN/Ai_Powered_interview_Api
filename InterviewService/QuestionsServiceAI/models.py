import mongoengine as me

# Create your models here.
class StudentInterviewPerformanceData(me.Document):
    UserId = me.StringField(required=True)
    UserEmail = me.EmailField(required=True)
    UserResult = me.StringField(required=True)
    createdAt = me.DateTimeField()

    def __str__(self):
        return f"{self.UserId} - {self.UserEmail}"