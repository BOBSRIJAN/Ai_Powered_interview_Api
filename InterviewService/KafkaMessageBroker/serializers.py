from rest_framework import serializers

class VideoAnalysisRequestSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    userid = serializers.CharField(required=True)
    question = serializers.CharField(required=True)
    videourl = serializers.CharField(required=True)
    totalnumberofquestion = serializers.IntegerField(required=True)