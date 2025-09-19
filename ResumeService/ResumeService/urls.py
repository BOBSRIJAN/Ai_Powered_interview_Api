from django.urls import path, include

urlpatterns = [
    path('resumeanalyzer/api/v1/', include('ResumeUploadServiceApi.urls')),
]
