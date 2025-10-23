from django.urls import path
from . import views

urlpatterns = [
    path("videoandaudioseperator/taskHendelar/", views.taskHendelar, name="taskHendelar"),
]