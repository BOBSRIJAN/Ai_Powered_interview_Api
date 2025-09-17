from django.urls import path 
from . import views 

urlpatterns = [
    path('UserList/',views.UserList, name='UserList'),
    path('AddUser/', views.AddUser, name='AddUser'),
]