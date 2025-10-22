from django.urls import path, include

urlpatterns = [
    path('interviewservice/api/v1/', include('QuestionsServiceAI.urls')),
    path('interviewservice/api/v1/', include('KafkaMessageBroker.urls'))
]