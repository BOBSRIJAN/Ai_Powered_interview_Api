
from django.urls import path
from .import views
urlpatterns = [
    path("AudioToAnswerFormator/AudioToText/", views.AudioToText, name="AudioToText")
]
