from django import forms
from .models import Espaco


class EspacoForm(forms.ModelForm):

    class Meta:
        model = Espaco
        fields = ['nome', 'tipo', 'capacidade', 'recursos', 'localizacao']
        labels = {
            'nome': 'Nome',
            'tipo': 'Tipo',
            'capacidade': 'Capacidade',
            'recursos': 'Recursos',
            'localizacao': 'Localização',
        }