from django.apps import AppConfig


class SignalsDemoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signals_demo'

    def ready(self):
        # Import signals so the receivers are registered when Django starts
        import signals_demo.signals  # noqa: F401
