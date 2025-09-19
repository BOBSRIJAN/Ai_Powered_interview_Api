from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    userId = serializers.CharField(required=True)
    url = serializers.CharField(required=True)
    jobDescription = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Resume(**validated_data).save()

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    class Meta:
        model = Resume
        fields = "__all__"