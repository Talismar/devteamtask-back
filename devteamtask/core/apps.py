from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devteamtask.core'

    def ready(self) -> None:
        import devteamtask.core.signals
