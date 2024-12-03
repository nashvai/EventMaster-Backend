from django.apps import AppConfig


class EventmasterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Eventmaster"


    def ready(self):
        import Eventmaster.signals
