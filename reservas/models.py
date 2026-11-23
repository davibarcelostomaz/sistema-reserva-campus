from django.conf import settings
from django.db import models


class Reserva(models.Model):
    """Reserva de um espaço no campus por um usuário em um período determinado."""

    class Status(models.TextChoices):
        CONFIRMADA = 'CONFIRMADA', 'Confirmada'
        PENDENTE = 'PENDENTE', 'Pendente'
        CANCELADA = 'CANCELADA', 'Cancelada'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservas',
    )
    espaco = models.ForeignKey(
        'espacos.Espaco',
        on_delete=models.CASCADE,
        related_name='reservas',
    )
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-data', 'hora_inicio']

    def __str__(self):
        return f"{self.usuario} - {self.espaco} ({self.data})"
