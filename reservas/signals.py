from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Reserva


@receiver(pre_save, sender=Reserva)
def aprovar_reserva_de_professor(sender, instance, **kwargs):
    """SCRUM-32: reservas feitas por professores já entram confirmadas."""
    eh_nova = instance._state.adding
    if eh_nova and instance.status == Reserva.Status.PENDENTE and instance.usuario.is_professor():
        instance.status = Reserva.Status.CONFIRMADA
