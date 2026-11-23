from django.contrib import admin

from .models import Espaco


@admin.register(Espaco)
class EspacoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'capacidade', 'localizacao']
    search_fields = ['nome', 'tipo', 'localizacao']
