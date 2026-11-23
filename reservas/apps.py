from django.apps import AppConfig


class ReservasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservas'

    def ready(self):
        # SCRUM-32: ativa a aprovação automática de reservas de professores
        from . import signals  # noqa: F401
