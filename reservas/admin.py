from django.contrib import admin

from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'espaco', 'data', 'hora_inicio', 'hora_fim', 'status']
    list_filter = ['status', 'data']
    search_fields = ['usuario__username', 'espaco__nome']
