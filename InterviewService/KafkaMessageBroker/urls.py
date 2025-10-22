from django.urls import path
from . import views
urlpatterns = [
    path('videoanalysisrequest/', views.videoAnalysisRequest, name='videoAnalysisRequest')
]