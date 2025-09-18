from django.urls import path, include

urlpatterns = [
    path('InterviewService/V1/', include('QuestionsServiceAI.urls'))
]