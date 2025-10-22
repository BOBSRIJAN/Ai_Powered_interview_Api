from rest_framework import serializers
from .models import userQuestionMetaData

class userQuestionMetaDataSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    userid = serializers.CharField(required=True)
    userquestion = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(required=False)

    class Meta:
        model = userQuestionMetaData
        fields = "__all__"
        
class requestDateSerializer(serializers.Serializer):
    userid = serializers.CharField(required=True)
    resumeurl = serializers.CharField(required=False)
    specificquestionrequirement = serializers.BooleanField(default = False)
    subjectortopic = serializers.ListField(
        child=serializers.CharField(), required=False, default=[]
    )
    numberofquestiion = serializers.IntegerField(required = True)
    level = serializers.CharField(required=True)

class questionHistorySerializer(serializers.Serializer):
    userid = serializers.CharField(required=True)