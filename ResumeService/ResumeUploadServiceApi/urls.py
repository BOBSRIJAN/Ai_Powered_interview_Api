from django.urls import path 
from . import views 

urlpatterns = [
    path('userlist/',views.UserList, name='UserList'),
    path('analyze/', views.Analyze, name='Analyze'),
]