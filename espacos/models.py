from django.db import models


class Espaco(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    capacidade = models.PositiveIntegerField()
    recursos = models.TextField(blank=True)
    localizacao = models.CharField(max_length=200)
    def __str__(self):
        return self.nome