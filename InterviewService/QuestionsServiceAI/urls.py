from django.urls import path
from . import views 

urlpatterns = [
    path('isActive/', views.isActive, name='isActive'),
    path('PostVideos/', views.PostVideoData, name='PostVideoData'),
]