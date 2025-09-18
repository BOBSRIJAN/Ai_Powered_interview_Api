from django.urls import path, include

urlpatterns = [
    path('ResumeUploadService/api/V1/', include('ResumeUploadServiceApi.urls')),
]
