from django.apps import AppConfig
from . import PingTest

class ResumeuploadserviceapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ResumeUploadServiceApi'

    def ready(self):
        PingTest.start()