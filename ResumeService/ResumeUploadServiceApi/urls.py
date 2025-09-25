from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.User, name='User'),
    path('analyzewithdocument/', views.AnalyzeWithDocument, name='AnalyzeWithDocument'),
    path('analyzewithjson/', views.AnalyzeWithJson, name='AnalyzeWithJson')
]
