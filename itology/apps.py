from django.apps import AppConfig


class ItologyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'itology'

    def ready(self):
        import itology.signals.create_profile  # noqa
