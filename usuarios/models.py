from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Usuário do sistema de reservas, com perfil de acesso (SCRUM-20)."""

    class Perfil(models.TextChoices):
        ALUNO = 'ALUNO', 'Aluno'
        PROFESSOR = 'PROFESSOR', 'Professor'
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'

    perfil = models.CharField(
        max_length=20,
        choices=Perfil.choices,
        default=Perfil.ALUNO,
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def is_aluno(self):
        return self.perfil == self.Perfil.ALUNO

    def is_professor(self):
        return self.perfil == self.Perfil.PROFESSOR

    def is_administrador(self):
        return self.perfil == self.Perfil.ADMINISTRADOR

    def __str__(self):
        return self.username
