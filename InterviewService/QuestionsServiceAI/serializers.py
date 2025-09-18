from rest_framework import serializers
from .models import StudentInterviewPerformanceData

class StudentInterviewPerformanceDataSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    UserId = serializers.CharField(required=True)
    UserEmail = serializers.EmailField(required=True)
    UserResult = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return StudentInterviewPerformanceData(**validated_data).save()

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    class Meta:
        model = StudentInterviewPerformanceData
        fields = "__all__"