import mongoengine as me

class Resume(me.Document):
    name = me.StringField(required=True, max_length=100)
    email = me.EmailField(required=True)
    resumeMetaData = me.StringField(required=True) 
    createdAt = me.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.email}"
