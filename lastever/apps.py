from django.apps import AppConfig


class LasteverConfig(AppConfig):
    name = 'lastever'

    def ready(self):
        import lastever.signals
