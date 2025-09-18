from django.apps import AppConfig
from . import PingTest

class QuestionsserviceaiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'QuestionsServiceAI'

    def ready(self):
        PingTest.start()