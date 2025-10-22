from django.urls import path
from . import views 

urlpatterns = [
    path('isActive/', views.isActive, name='isActive'),
    path("questionhistory/", views.questionHistory, name="questionHistory"),
    path("getinterviewquestions/", views.getInterviewQuestions, name="getInterviewQuestions"),
]